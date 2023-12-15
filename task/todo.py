from pathlib import Path

from django.utils.timezone import localdate, localtime

from publish.days import tomorrow, yesterday
from publish.files import fix_chars
from publish.management.commands.edit import edit_file
from publish.seamanslog import (create_history_file, create_sampler_file,
                                create_spirit_file)


def create_files(path, start_day, num_days, path_name, set_text):
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
            text = fix_chars(text)
            f.write_text(text)
        return f

    return [
        create_file(path, date, path_name, set_text)
        for date in recent_days(start_day, num_days)
    ]


def edit_blog_files():
    def blog_path(path, date):
        return path / (date.strftime("%m/%d") + ".md")

    path = Path("Documents/seamanslog.com/sampler")
    open_files(path, 0, 1, blog_path, create_sampler_file)


def edit_todo_list():
    print("HAMMER TODO -", localtime().strftime("%A, %m-%d  %H:%M"))
    edit_task_files()
    # edit_spirit_files()
    # edit_blog_files()
    # edit_file(create_toot_file())


def edit_task_files():
    def path_name(path, date):
        return path / (date.strftime("%Y/%m/%d"))

    path = Path("Documents/markseaman.info/history")
    edit_file([path/'Today.md', path/localdate().strftime("%Y/%m")])
    # edit_file([path/'Goals.md'])
    open_files(path, 0, 3, path_name, create_history_file)


def edit_spirit_files():
    def path_name(path, date):
        return path / (date.strftime("%m/%d") + ".md")

    path = Path("Documents/spiritual-things.org/daily")
    open_files(path, 0, 1, path_name, create_spirit_file)


def open_files(path, start_day, num_days, path_name, set_text):
    edit_file(create_files(path, start_day, num_days, path_name, set_text))
