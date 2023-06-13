from os import getenv, system
from pathlib import Path

from markdown import markdown

from publish.document import title
from publish.text import text_join, text_lines


def doc_html(pub, chapter, doc):
    return markdown(read_pub_doc(pub, chapter, doc),  extensions=['tables'])


def doc_title(pub, chapter, doc):
    return title(read_pub_doc(pub, chapter, doc))


def doc_text(pub, chapter, doc):
    lines = text_lines(read_pub_doc(pub, chapter, doc))[2:]
    return text_join(lines)


def list_pubs():
    path = pub_path()
    return [pub_link(pub.parent.name) for pub in path.glob('*/pub.json') if pub.parent.is_dir()]


def doc_list(pub, chapter):
    path = pub_path(pub, chapter)
    return [doc_link(pub, chapter, doc.name) for doc in sorted(path.glob('*.md')) if doc.is_file()]


def chapter_list(pub):
    path = pub_path(pub)
    x = []
    chapters = path.iterdir()
    for chapter in chapters:
        if chapter.is_dir():
            x.append(pub_link(pub, chapter.name))
    return x
    # return [pub_link(pub, chapter.name) for chapter in path.iterdir() if chapter.is_dir()]


def pub_link(pub, chapter=None):
    if chapter:
        url = f'/writer/{pub}/{chapter}'
        title = chapter
    else:
        url = f'/writer/{pub}'
        title = pub

    return f'<a href="{url}">{title}</a>'

def pub_url(pub=None, chapter=None, doc=None):
    if doc:
        return f'/writer/{pub}/{chapter}/{doc}'
    if chapter:
        return f'/writer/{pub}/{chapter}'
    if pub:
        return f'/writer/{pub}'
    return f'/writer/'


def doc_link(pub, chapter, doc):
    url = f'/writer/{pub}/{chapter}/{doc}'
    # title = doc_title(pub, chapter, doc)
    # return f'<a href="{url}">{title}</a>'
    return f'<a href="{url}">{doc[:-3]}</a>'


def pub_path(pub=None, chapter=None, doc=None):
    path = Path(f'{getenv("SHRINKING_WORLD_PUBS")}')

    if doc and chapter and pub:
        path = path/pub/'AI'/chapter/doc
    elif chapter and pub:
        path = path/pub/'AI'/chapter
    elif pub:
        path = path/pub/'AI'
    else:
        path = path
    return path


def doc_ai(pub, chapter, doc):
    doc = doc.replace('.md', '.ai')
    path = pub_path(pub, chapter, doc)
    if path.exists():
        return markdown(path.read_text())


def doc_human(pub, chapter, doc):
    doc = doc.replace('.md', '.txt')
    path = pub_path(pub, chapter, doc)
    if path.exists():
        return markdown(path.read_text())


def get_menu(pub, chapter, doc):
    items = [("Publications", "/publish/book"),
             ("Pubs", pub_url())]
    if pub:
        items.append(("Chapters", pub_url(pub)),)
    if chapter:
        items.append(("Docs", pub_url(pub, chapter)),)
    return  {"title": ('GhostWriter', '/writer/'), 
             "items":items}


def pub_view_data(**kwargs):
    pub = kwargs.get('pub')
    chapter = kwargs.get('chapter')
    doc = kwargs.get('doc')

    if doc and chapter and pub:
        kwargs['text'] = read_pub_doc(pub, chapter, doc)
        kwargs['html'] = doc_html(pub, chapter, doc)
        kwargs['ai'] = doc_ai(pub, chapter, doc)
        kwargs['human'] = doc_human(pub, chapter, doc)
    if chapter and pub:
        kwargs['docs'] = doc_list(pub, chapter)
    if pub:
        kwargs['chapters'] = chapter_list(pub)
    kwargs['pubs'] = list_pubs()
    kwargs['menu'] = get_menu(pub, chapter, doc)
    return kwargs


def pub_edit(**kwargs):
    pub = kwargs.get('pub')
    chapter = kwargs.get('chapter')
    doc = kwargs.get('doc')
    path = pub_path(pub, chapter, doc)
    path2 = str(path).replace('.md', '.txt')
    path3 = str(path).replace('.md', '.ai')
    editor = getenv("EDITOR").replace(' -w', '')
    # editor='/Applications/Visual Studio Code.app/Contents/Resources/app/bin/code'
    # TODO Windows compatible editor
    command = f'"{editor}" -w "{path}" "{path2}" "{path3}"'
    print(command)
    system(command)
    url = pub_url(pub, chapter, doc)
    return url


def read_pub_doc(pub, chapter, doc):
    path = pub_path(pub, chapter, doc)
    if not path.exists():
        return f"FILE NOT FOUND: {path}"
    return path.read_text()
