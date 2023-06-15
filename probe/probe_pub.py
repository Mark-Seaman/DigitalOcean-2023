from pathlib import Path
from publish.publication import all_pubs, build_pubs, get_pub_info, show_pub_json


def test_pub_import():
    return build_pubs()


def test_pub_json():
    return show_pub_json()


def test_pub_info():
    for pub in all_pubs():
        text = get_pub_info(pub.name)
        Path(f'probe/pubs/{pub.name}').write_text(text)