from pathlib import Path
from django.utils.timezone import localdate

from publish.models import Content

from .pub import get_pub, show_pub_summaries, show_pub_words
from .seamanslog import create_toot_file, random_article, review_file
from workshop.management.commands.edit import edit_file


def write_blog(args=[]):
    print(f"write blog {args}")
    if not args:
        args = review_file(args)
    elif Path(args[0]).exists():
        pass
    elif args[0] == 'spiritual':
        today = localdate().strftime("%m/%d") + ".md"
        args[0] = f"Documents/spiritual-things.org/daily/{today}"
    elif args[0] == 'seamanslog':
        today = localdate().strftime("%m/%d") + ".md"
        args[0] = f"Documents/seamanslog.com/sampler/{today}"
    else:
        pub = get_pub(args[0])
        if args[1:]:
            # print("FIND", args[1:])
            c = Content.objects.filter(blog=pub, path__endswith=args[1])
            if c:
                args = [c[0].path]
                # print('CHOOSE', c[0].path)
        else:
            article = random_article(pub)
            args[0] = article["doc"]

    edit_file(args)
    return f'Edit file {args}'


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
