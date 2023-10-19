from pathlib import Path
from probe.data import save_json_data
from publish.days import is_old
from publish.publication import all_pubs, build_pubs, show_pub_json
from writer.words import measure_pub_words


def test_build_pubs():
    build_pubs()
    save_json_data('config/publish.json', 'publish')
    return 'OK'


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
