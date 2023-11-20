from pathlib import Path
from publish.days import is_old
from publish.publication import all_pubs, show_pub_json
from writer.words import measure_pub_words


def test_pub_json():
    return show_pub_json()


def test_pub_content():
    return measure_pub_words()


def test_word_files():
    text = 'OK'
    for p in all_pubs():
        f = Path(f'Documents/markseaman.info/words/{p.name}')
        if f.exists() and is_old(f):
            text += f'IS OLD {f}\n\n'
    return text
