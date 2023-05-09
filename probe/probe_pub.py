from pathlib import Path
from publish.pub import (
    build_pubs,
    show_pub_contents,
    show_pub_index,
    show_pub_json,
    show_pub_summaries,
    show_pub_words,
)


def test_pub_contents():
    return show_pub_contents()


def test_pub_import():
    return build_pubs()


def test_pub_index():
    text = show_pub_index()
    return show_pub_index()


def test_pub_json():
    return show_pub_json()


def test_pub_show():
    return show_pub_summaries()


def test_pub_words():
    return show_pub_words()
