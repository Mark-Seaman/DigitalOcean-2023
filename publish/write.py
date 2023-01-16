from django.utils.timezone import localdate
from django.template.loader import render_to_string
from pathlib import Path
from publish.document import title
from publish.files import read_file, write_file
from re import findall, search, sub
from shutil import copyfile

from publish.models import Content
from publish.text import text_lines, text_replace

from .pub import get_pub, show_pub_summaries, show_pub_words
from .seamanslog import create_toot_file, random_article, review_file
from workshop.management.commands.edit import edit_file


def write_blog(args=[]):
    print(f"write blog {args}")
    if not args:
        args = review_file(args)
    elif Path(args[0]).exists():
        pass
    elif args[0] == 'green':
        greenhouse()
        return
    elif args[0] == 'plant':
        plant(args[1:])
        return
    elif args[0] == 'markdown':
        markdown(args[1:])
        return
    elif args[0] == 'masto':
        write_masto()
        return
    elif args[0] == 'spiritual':
        today = localdate().strftime("%m/%d") + ".md"
        args[0] = f"Documents/spiritual-things.org/daily/{today}"
    elif args[0] == 'seamanslog':
        today = localdate().strftime("%m/%d") + ".md"
        args[0] = f"Documents/seamanslog.com/sampler/{today}"
    elif args[0] == 'words':
        write_words(args[1:])
        return
    else:
        pub = get_pub(args[0])
        if args[1:]:
            c = Content.objects.filter(blog=pub, path__endswith=args[1])
            if c:
                args = [c[0].path]
        else:
            article = random_article(pub)
            args[0] = article["doc"]

    edit_file(args)
    return f'Edit file {args}'


def greenhouse():
    edit_file('Documents/shrinking-world.com/greenhouse')


def plant(args):
    outline_file = f'Documents/shrinking-world.com/greenhouse/{args[0]}'
    markdown_dir = args[1]
    create_markdown_files(outline_file, markdown_dir)


def create_markdown_files(outline_file, markdown_dir):
    text = read_file(outline_file)
    create_index_file(markdown_dir, text)
    for topic in find_subtopics(text):
        create_topic_file(markdown_dir, topic)


def create_index_file(markdown_dir, outline):
    def link(topic):
        return f"[{topic[1]}]({f'{(topic[0]+1):02}.md'})"

    docs = [link(topic) for topic in find_subtopics(outline)]
    topic = text_lines(outline)[0]
    data = dict(title=topic, docs=docs)
    text = render_to_string("pub/pub_index.md", data)
    md = f'{markdown_dir}/Index.md'
    write_file(md, text)
    edit_file(md)


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


def write_review(args=[]):
    print(f"write review {args}")
    edit_file("Documents/shrinking-world.com/blog")


def write_tech(args=[]):
    print(f"write tech {args}")
    edit_file("Documents/shrinking-world.com/blog")


def write_words(args=[]):
    print(f"write words {args}")
    if not args:
        print(show_pub_summaries())
    for pub in args:
        pub = get_pub(pub)
        print(show_pub_words(pub))
        # edit_file(f"Documents/markseaman.info/words/{args[0]}")
    edit_file(f"Documents/markseaman.info/words")
