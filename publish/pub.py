from random import choice
from pathlib import Path

from .document import document_body, document_html, document_title
from .files import read_file, read_json, write_file
from .import_export import create_pubs, import_pub, save_data
from .models import Content, Pub
from .text import text_join, word_count
from .toc import create_pub_index, pub_contents, table_of_contents


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
    delete_pubs()
    log = create_pubs()
    import_pubs(pub)
    save_data()
    return log


# def create_index_files():
#     for pub in all_pubs():
#         create_pub_index(pub, get_pub_contents(pub))


def delete_pubs():
    Pub.objects.all().delete()


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


def import_pubs(pub=None):
    text = ""
    pubs = [pub] if pub else all_pubs()
    for pub in pubs:
        import_pub(pub)
        auto_index = pub.name == "sampler"
        if auto_index:
            create_pub_index(pub, get_pub_contents(pub))
        text += f"Pub: {pub.title}, Path: {pub.doc_path}\n"
    return text


def list_content(pub):
    return [c for c in Content.objects.filter(blog=pub)]


def list_pubs():
    pubs = [pub_contents(pub) for pub in all_pubs()]
    return text_join(pubs)


def pub_redirect(host, pub, doc):
    if host == "shrinking-world.com" and not pub:
        return f"/tech"
    if host == "seamanslog.com" and not pub:
        return f"/sampler/today"
    if host == "seamansguide.com" and not pub:
        return f"/publish/books"
    if host == "spiritual-things.org" and not pub:
        return f"/spiritual/today"
    if host == "markseaman.org" and not pub:
        return f"/mark"
    if host == "markseaman.info" and not pub:
        return f"/private"
    return f"/{pub}/{doc}"


def random_doc(directory):
    return choice([p for p in Path(directory).iterdir()])


def random_doc_page(path):
    x = choice([str(f.name) for f in Path(path).iterdir() if str(f).endswith(".md")])
    return x.replace(".md", "")


def show_pub_content(pub):
    text = f"PUB CONTENT - {pub.title}\n\n"
    folders = get_pub_contents(pub)
    for f in folders:
        text += f"\nFOLDER {f.get('path')}\n"
        for d in f.get("documents"):
            text += f"\n     {d}\n"
    return text


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


def show_pub_json():
    return text_join([j.read_text() for j in Path("static/js").iterdir()])


def show_pubs():
    def count_words(pub):
        words = 0
        for c in Content.objects.filter(blog=pub):
            words += doc_words(c.path)
        pub.words = words
        pub.save()

    def doc_words(path):
        return word_count(read_file(path))

    def pub_summary(pub):
        count_words(pub)
        title = f"{pub.pub_type:8} {pub.name:15} {pub.title:30}"
        posts = f"{len(Content.objects.filter(blog=pub))} Posts, {int(pub.words/1000)}k Words"
        text = f"{title} {posts}\n"
        return text

    def pub_summaries():
        text = "My Pubs\n\n"
        total_words = 0
        for pub in all_pubs():
            text += pub_summary(pub)
            total_words += pub.words
            update_word_counts(pub)
        return text + f"\n\nTotal Words: {int(total_words/1000)}k Words\n"

    def update_word_counts(pub):
        path = Path("Documents/markseaman.info") / pub.name / "Words.md"
        contents = get_pub_contents(pub)
        write_file(path, table_of_contents(pub, contents, True))

    return pub_summaries()
