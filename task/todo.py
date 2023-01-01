from django.template.loader import render_to_string
from django.utils.timezone import localdate, localtime
from pathlib import Path

from publish.seamanslog import (
    create_sampler_file,
    create_history_file,
    create_spirit_file,
    extract_message,
)
from workshop.management.commands.edit import edit_file
from publish.days import tomorrow, yesterday
from publish.pub import get_pub
from publish.seamanslog import random_article


# def select_article():
#     return dict(pub=get_pub("mark"), doc="Index.md")


def edit_blog_files():
    def path_name(path, date):
        return path / (date.strftime("%m/%d") + ".md")

    path = Path("Documents/seamanslog.com/sampler")
    open_files(path, 1, 2, path_name, create_sampler_file)


def edit_review_file(path):
    if not path:
        article = random_article()
        path = article["doc"]
    edit_file([path])
    print(f"REVIEW: {article['doc']}")


def edit_toot_file():
    date = localdate()
    path = Path("Documents/mastodon/mdseaman") / date.strftime("_%m%d")
    article = random_article()
    message = random_message(article)
    if message:
        print(path, message)
        path.write_text(message)
        edit_file([article["doc"], path])


def random_message(article):
    for i in range(5):
        text = extract_message(article["doc"], article["url"])
        if text:
            return text


def edit_todo_list():
    print("HAMMER TODO -", localtime().strftime("%A, %m-%d  %H:%M"))
    edit_task_files()
    edit_spirit_files()
    edit_blog_files()
    # edit_review_file(path)
    edit_toot_file()
    # system(f"subl Documents/shrinking-world.com/tweet")


def edit_task_files():
    def path_name(path, date):
        return path / (date.strftime("%Y/%m/%d"))

    path = Path("Documents/markseaman.info/history")
    open_files(path, 0, 3, path_name, create_history_file)


def edit_spirit_files():
    def path_name(path, date):
        return path / (date.strftime("%m/%d") + ".md")

    path = Path("Documents/spiritual-things.org/daily")
    open_files(path, 1, 2, path_name, create_spirit_file)


def open_files(path, start_day, num_days, path_name, set_text):
    def recent_days(today=0, days=1):
        start = tomorrow(localdate())
        return [yesterday(start, days - d - today) for d in range(days)]

    def create_file(path, date, path_name, set_text):
        f = path_name(path, date)
        if not f.exists():
            if not f.parent.exists():
                if not f.parent.parent.exists():
                    f.parent.parent.mkdir()
                f.parent.mkdir()
            text = set_text(date)
            f.write_text(text)
        return f

    files = [
        create_file(path, date, path_name, set_text)
        for date in recent_days(start_day, num_days)
    ]
    edit_file(files)
