from pathlib import Path
from publish.text import text_join
from publish.pub import build_pubs, list_pubs, show_pub_json, show_pubs


def test_pub_import():
    return build_pubs()


def test_pub_toc():
    return list_pubs()


def test_pub_show():
    return show_pubs()


def test_pub_json():
    return show_pub_json()
