from publish.pub import get_pub, show_pub_summaries, show_pub_words
from publish.seamanslog import create_toot_file
from task.todo import edit_blog_files, edit_spirit_files
from workshop.management.commands.edit import edit_file


def write_blog(args=[]):
    print(f"write blog {args}")
    edit_blog_files()
    edit_spirit_files()


def write_masto(args=[]):
    print(f"write masto {args}")
    edit_file(create_toot_file())


def write_review(args=[]):
    print(f"write review {args}")
    edit_file("Documents/shrinking-world.com/blog/tech")


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
