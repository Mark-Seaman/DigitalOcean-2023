from pathlib import Path
from random import choice
from shutil import copyfile

from .document import document_body, document_html, document_title
from .files import read_file, read_json
from .import_export import create_pubs, import_pub, save_pub_data
from .models import Content, Pub
from .text import line_count, text_join, word_count
from .toc import (create_pub_index, pub_contents)


def all_blogs():
    return [p for p in Pub.objects.filter(pub_type="blog")]


def all_books():
    return [p for p in Pub.objects.filter(pub_type="book")]


def all_courses():
    return [p for p in Pub.objects.filter(pub_type="course")]


def all_privates():
    return [p for p in Pub.objects.filter(pub_type="private")]


def all_pubs():
    return [p for p in Pub.objects.all()]


def build_pubs(pub=None):
    def copy_static_files(pub):
        js1 = f'{pub.doc_path}/{pub.name}.json'
        js2 = f'static/js/{pub.name}.json'
        if Path(js1).exists():
            # print(js1, js2)
            copyfile(js1, js2)
        source = Path(pub.doc_path)/'../Images'
        dest = Path(pub.image_path[1:])
        if source.exists():
            if not dest.exists():
                dest.mkdir()
            for f in source.iterdir():
                # print(f"COPY FILES {pub.name} {f} {dest/f.name}")
                copyfile(f, dest/f.name)

    # delete_pubs()
    log = create_pubs()

    text = ""
    pubs = [pub] if pub else all_pubs()
    for pub in pubs:
        import_pub(pub)
        if pub.auto_index:
            # print("CREATE Index")
            create_pub_index(pub, get_pub_contents(pub))
        copy_static_files(pub)
        text += f"Pub: {pub.title}, Path: {pub.doc_path}\n"

    save_pub_data()
    return text


def delete_pubs():
    Pub.objects.all().delete()


def doc_view_context(**kwargs):
    path = kwargs.get('path', 'Documents/shrinking-world.com/blog/Index.md')
    json = kwargs.get('json', 'Documents/shrinking-world.com/blog.json')
    kwargs = read_json(json)
    markdown = document_body(read_file(path))
    kwargs['title'] = document_title(path)
    kwargs['html'] = document_html(markdown)
    return kwargs


def get_host(request):
    host = request.get_host()
    if not host or host.startswith("127.0.0.1") or host.startswith("localhost"):
        host = "seamanslog.com"
    return host


def get_pub(name):
    return Pub.objects.get(name=name)


def get_pub_contents(pub):
    def doc_objects(pub, folder):
        return (
            Content.objects.filter(blog=pub, doctype="chapter", folder=folder)
            .order_by("order")
            .values()
        )

    def docs_in_folder(pub, folder):
        return [d for d in doc_objects(pub, folder)]

    def folder_objects(pub):
        return (
            Content.objects.filter(blog=pub, doctype="folder")
            .order_by("order")
            .values()
        )

    folders = []
    for folder in folder_objects(pub):
        docs = docs_in_folder(pub, folder.get("order"))
        folder.update(dict(documents=docs))
        folders.append(folder)
    return folders


def get_pub_folders(pub):
    def objects(pub, type):
        return Content.objects.filter(blog=pub, doctype=type).order_by("order")

    def folders(pub):
        return [(f, docs(f)) for f in objects(pub, "folder")]

    def docs(folder):
        return objects(pub, "chapter").filter(folder=folder)

    return folders


def list_content(pub):
    return [c for c in Content.objects.filter(blog=pub)]


def pub_redirect(host, pub, doc):
    if host == "shrinking-world.com" and not pub:
        return f"/tech"
    if host == "seamanslog.com" and not pub:
        return f"/io"
    if host == "seamansguide.com" and not pub:
        return f"/publish/book"
    if host == "seamanfamily.org" and not pub:
        return f"/family/Index.md"
    if host == "spiritual-things.org" and not pub:
        return f"/spiritual/today"
    if host == "markseaman.org" and not pub:
        return f"/mark"
    if host == "markseaman.info" and not pub:
        return f"/private"
    if "localhost" in host and not pub:
        return f"/io"
    return f"/{pub}/{doc}"


def random_doc(directory):
    return choice([p for p in Path(directory).iterdir()])


def random_doc_page(path):
    x = choice([str(f.name)
               for f in Path(path).iterdir() if str(f).endswith(".md")])
    return x.replace(".md", "")


def save_pub_details():
    text = ''
    for pub in all_pubs():
        text += show_pub_details(pub)
        word_count_file(pub).write_text(text)
    return line_count(text)


def select_blog_doc(host, blog, doc):
    def load_object(pub):
        return Pub.objects.filter(pk=pub.pk).values()[0]

    def load_document(pub):
        # Find doc path - Use the markdown file extension
        path = pub.doc_path
        path = Path(path) / doc.replace("-", "/")
        if not Path(path).exists() and Path(f"{path}.md").exists():
            path = Path(f"{path}.md")

        # Load the correct document
        if path.exists():
            markdown = document_body(read_file(path), pub.image_path)
            title = document_title(path)
            html = document_html(markdown)
        else:
            title = "Missing Document"
            html = f"<h1>Document file not found<h1><h2> {path}</h2>"

        return dict(
            title=title, html=html, site_title=pub.title, site_subtitle=pub.subtitle
        )

    pub = get_pub(blog)
    kwargs = load_object(pub)
    kwargs.update(load_document(pub))
    menu = kwargs.get("menu")
    if menu:
        kwargs["menu"] = read_json(menu)["menu"]

    return kwargs


def show_pub_content(pub):
    text = f"PUB CONTENT - {pub.title}\n\n"
    folders = get_pub_contents(pub)
    for f in folders:
        text += f"\nFOLDER {f.get('path')}\n"
        for d in f.get("documents"):
            text += f"\n     {d}\n"
    return text


def show_pub_details(pub):
    content = pub.content_set.all()
    output = f'Pub Contents - {pub.name} - {pub.title}'
    total_words = 0
    for f in content.filter(folder=0):
        folder_words = word_count(read_file(f.path))
        output += f'\n{f.title} - {f.path} - {folder_words} words\n'
        for d in content.filter(folder=f.order):
            words = word_count(read_file(d.path))
            folder_words += words
            output += f'    {d.title} - {d.path} - {words} words\n'
        output += f'    Words in {f.title}: {folder_words} words\n'
        total_words += folder_words
    output += f'\nTotal Words in {pub.title}: {total_words} words, {int(total_words/250)} pages\n'
    return output


def show_pub_words(pub=None):
    text = "PUB WORDS\n\n"
    pubs = [pub] if pub else all_pubs()
    for pub in pubs:
        path = word_count_file(pub)
        text += f"\n\n---\n\n{path}\n\n---\n\n"
        text += path.read_text()
    return text


def show_pub_json():
    text = "PUB JSON\n\n"
    for js in Path("static/js").iterdir():
        text += f"\n\n---\n\n{js}\n\n---\n\n"
        text += js.read_text()
    return text


def word_count_file(pub):
    return Path("Documents/markseaman.info") / "words" / pub.name
