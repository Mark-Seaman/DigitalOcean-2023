from os import system
from pathlib import Path

from django.template.loader import render_to_string
from django.utils.timezone import localdate
from publish.files import read_file, write_file

from publish.models import Content
from publish.slides import create_slides, markdown, plant, write_workshop
from publish.text import text_lines
from workshop.management.commands.edit import edit_file

from .pub import get_pub, show_pub_summaries, show_pub_words
from .seamanslog import create_toot_file, random_article


def write_blog(args=[]):
    # print(f"write blog {args}")
    if not args:
        return '''usage: write [options]
            
            options:
                green - show the Greenhouse for Ideas
                plant topic - create Markdown for the selected idea
                markdown doc - conver the Markdown to HTML
                masto - select an article, review it, and create a posting
                render source dest script template - create a post file
                slides - create a slide show from an outline
                seamanslog - edit the blog post for today
                spiritual - edit the blog post for today
                words - summary of word count

        '''
    elif args[0] == 'blogcast':
        write_blogcast(args[1:])
    elif args[0] == 'green':
        greenhouse()
    elif args[0] == 'plant':
        edit_file(plant(args[1:]))
    elif args[0] == 'markdown':
        markdown(args[1:])
    elif args[0] == 'masto':
        write_masto()
    elif args[0] == 'render':
        return write_render(args[1:])
    elif args[0] == 'slides':
        return create_slides(args[1:])
    elif args[0] == 'spiritual':
        today = localdate().strftime("%m/%d") + ".md"
        args[0] = f"Documents/spiritual-things.org/daily/{today}"
        edit_file(args)
    elif args[0] == 'seamanslog':
        today = localdate().strftime("%m/%d") + ".md"
        args[0] = f"Documents/seamanslog.com/sampler/{today}"
        edit_file(args)
    elif args[0] == 'sw':
        print('Shrinking World')
        system('open https://the-shrinking-world.ghost.io/ghost/#/site')
        edit_file('Documents/shrinking-world.io')
    elif args[0] == 'words':
        write_words(args[1:])
    elif args[0] == 'workshop':
        write_workshop(args[1:])
    else:
        write_pub(args)


def write_blogcast(args=[]):
    print(f'write blogcast {args[0]+".ol"} {args[0]+".md"}')
    text = ''
    d = args[0]
    f = args[1]
    lines = text_lines(read_file(f'{d}/{f}.ol'))
    for line in lines:
        if not line:
            text += '\n'
        elif not line.startswith('    '):
            text += f'# {line}\n\n'
        elif not line.startswith('        '):
            text += f'\n## {line.strip()}\n\n'
        elif line:
            text += f'* {line.strip()}\n'
    f = f'{d}/{f}.md'
    write_file(f, text)
    print(text)


def greenhouse():
    edit_file(['Documents/shrinking-world.com/greenhouse',
               'Documents/shrinking-world.com/greenhouse/Content.ol',
               'Documents/shrinking-world.com/greenhouse'])


def render_document(**kwargs):

    def read_source(source):
        if source:
            path = Path(source)
            if path.exists():
                text = path.read_text()
            else:
                text = f'\n**** BAD FILE **** {path}\n'
        return text

    def apply_script(script, text):
        if script:
            if script == 'upcase':
                text = text.upper()
            elif script == 'review':
                text = random_article()['text']
            else:
                text += f'\n**** BAD SCRIPT **** {script}\n'
        return text

    def render_template(template, text):
        if template:
            if template == 'blog':
                text = render_to_string('pub/blog.md', dict(text=text))
            elif template == 'message':
                text = render_to_string(
                    'pub/message.md', dict(text=text[:500]))
            else:
                text += f'\n**** BAD TEMPLATE **** {template}\n'
        return text

    def write_dest(dest, text):
        if dest:
            path = Path(dest)
            path.write_text(text)

    source = kwargs.get('source')
    dest = kwargs.get('dest')
    script = kwargs.get('script')
    template = kwargs.get('template')
    text = read_source(source)
    text = apply_script(script, text)
    text = render_template(template, text)
    write_dest(dest, text)
    return text


def write_masto(args=[]):
    print(f"write masto {args}")
    edit_file(create_toot_file())


def write_pub(args):
    if args[0] == 'pub':
        pub = None
    else:
        pub = get_pub(args[0])
    print(f'WRITE {pub} {args}')
    if args[1:]:
        c = Content.objects.filter(blog=pub, path__endswith=args[1])
        if c:
            args = [c[0].path]
    else:
        article = random_article(pub)
        args[0] = article["doc"]
        print(f'SELECT {args}')
    if Path(args[0]).exists() and Path(args[0]).is_file():
        edit_file(args)


def write_render(args):
    # print(f"write render {args}")
    if not args[3:]:
        return 'usage: write render source dest script template'
    text = render_document(source=args[0], dest=args[1],
                           script=args[2], template=args[3])
    return text


def write_words(args=[]):
    print(f"write words {args}")
    if not args:
        print(show_pub_summaries())
    for pub in args:
        pub = get_pub(pub)
        print(show_pub_words(pub))
        # edit_file(f"Documents/markseaman.info/words/{args[0]}")
    edit_file(f"Documents/markseaman.info/words")
