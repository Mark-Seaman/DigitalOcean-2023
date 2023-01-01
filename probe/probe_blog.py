from pathlib import Path
from publish.text import text_join
from publish.pub import build_pubs, list_pubs, show_pubs
from requests import get


def test_blog_import():
    return build_pubs()


def test_blog_toc():
    return list_pubs()


def test_blog_list():
    page = "https://seamanslog.com/publish/blog"
    return get(page).text


def test_book_list():
    page = "https://seamanslog.com/publish/book"
    return get(page).text


def test_blog_show():
    return show_pubs()


def test_blog_json():
    return text_join([j.read_text() for j in Path("static/js").iterdir()])


# def test_blog_export():
# return export_blogs()


# def test_book_content():
#     return show_all_books()
