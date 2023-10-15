from pathlib import Path
from publish.days import is_old
from publish.publication import all_pubs, build_pubs, show_pub_json
from writer.words import measure_pub_words, show_pubs


def test_pub_import():
    return build_pubs()


def test_pub_json():
    return show_pub_json()


def test_pub_info():
    return 'OK'
#     save_pub_info()
#     text = concatonate('probe/pubs/*')
#     return f'All Pub Info: {line_count(text)}'


def test_show_pubs():
    return show_pubs()


def test_pub_content():
    return measure_pub_words()


def test_word_files():
    text = ''
    for p in all_pubs():
        f = Path(f'Documents/markseaman.info/words/{p.name}')
        if f.exists() and is_old(f):
            text += f'IS OLD {f}\n\n'
    return text
