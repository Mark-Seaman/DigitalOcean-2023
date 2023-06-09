from publish.publication import (build_pubs, save_pub_details, show_pub_json,
                         show_pub_words)


def test_pub_import():
    return build_pubs()


def test_pub_json():
    return show_pub_json()


def test_pub_show():
    details = save_pub_details()
    return show_pub_words() + '\n\n' + details + '\n'
