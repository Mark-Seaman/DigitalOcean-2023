from publish.pub import (
    build_pubs,
    save_pub_details,
    show_pub_contents,
    show_pub_json,
    show_pub_words,
)


def test_pub_contents():
    return show_pub_contents()


def test_pub_import():
    return build_pubs()


def test_pub_json():
    return show_pub_json()


def test_pub_show():
    return save_pub_details()


def test_pub_words():
    return show_pub_words()
