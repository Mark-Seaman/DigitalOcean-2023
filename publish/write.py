from django.utils.timezone import localdate
from django.template.loader import render_to_string
from pathlib import Path
from publish.document import title
from publish.files import read_file, write_file
from re import findall, search, sub
from shutil import copyfile

from publish.models import Content
from publish.text import text_lines, text_replace

from .pub import get_pub, list_content, show_pub_summaries, show_pub_words
from .seamanslog import create_toot_file, random_article, review_file
from workshop.management.commands.edit import edit_file


def write_blog(args=[]):
    # print(f"write blog {args}")
    if not args:
        return 'usage: write [green|plant|markdown|masto|render|pub|spiritual|seamanslog|words]'
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
    elif args[0] == 'spiritual':
        today = localdate().strftime("%m/%d") + ".md"
        args[0] = f"Documents/spiritual-things.org/daily/{today}"
        edit_file(args)
    elif args[0] == 'seamanslog':
        today = localdate().strftime("%m/%d") + ".md"
        args[0] = f"Documents/seamanslog.com/sampler/{today}"
        edit_file(args)
    elif args[0] == 'words':
        write_words(args[1:])
    else:
        write_pub(args)


def greenhouse():
    edit_file('Documents/shrinking-world.com/greenhouse')


def plant(args):
    outline_file = f'Documents/shrinking-world.com/greenhouse/{args[0]}'
    markdown_dir = args[1]
    return create_markdown_files(outline_file, markdown_dir)


def create_markdown_files(outline_file, markdown_dir):
    text = read_file(outline_file)
    index = create_index_file(markdown_dir, text)
    for topic in find_subtopics(text):
        create_topic_file(markdown_dir, topic)
    return index


def create_index_file(markdown_dir, outline):
    def link(topic):
        return f"[{topic[1]}]({f'{(topic[0]+1):02}.md'})"

    docs = [link(topic) for topic in find_subtopics(outline)]
    topic = text_lines(outline)[0]
    data = dict(title=topic, docs=docs)
    text = render_to_string("pub/pub_index.md", data)
    md = f'{markdown_dir}/Index.md'
    write_file(md, text)
    return md


def create_topic_file(markdown_dir, topic):
    f = f'{markdown_dir}/{(topic[0]+1):02}.md'
    title = topic[1]
    text = render_to_string("pub/pub_lesson.md", dict(title=title))
    write_file(f, text)


def find_subtopics(text):
    return [(i, sub(r'    (\w*)', r'\1', x))
            for i, x in enumerate(findall('        .*', text))]


def markdown(args):
    f = f'Documents/shrinking-world.com/greenhouse/{args[0]}'
    md = f.replace('.ol', '.md')
    write_markdown(f, md)
    edit_file(md)


def write_markdown(outline_file, markdown_file):
    text = read_file(outline_file)
    text = text.replace('\n', '\n\n# ')
    text = '# ' + text.replace('    ', '#')
    write_file(markdown_file, text)


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
