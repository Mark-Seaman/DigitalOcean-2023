from django.template.loader import render_to_string
from json import loads
from genericpath import isdir, isfile
from os import system
from pathlib import Path

from .document import document_title, get_document
from .files import read_json, read_csv_file
from .text import text_join
from .models import Pub, Content


def create_pub_index(pub, content_tree):
    def url(path):
        path = Path(path)
        return f"{path.parent.name}-{path.name}"

    def link(doc):
        return f"[{doc['title']}]({url(doc['path'])})"

    def folder_index_text(folder, documents):
        path = folder.get("path")
        docs = []
        for doc in documents:
            docs.append(link(doc))
        title = f"Month {Path(path).parent.name}"
        data = dict(title=title, docs=docs)
        return render_to_string("pub/pub_index.md", data)

    def top_index_text(content_tree):
        docs = [link(f) for f in content_tree]
        # docs = [f"[{f['title']}]({url(f['path'])})" for f in content_tree]
        data = dict(title="Table of Contents", docs=docs)
        return render_to_string("pub/pub_index.md", data)

    def folder_index(folder):
        text = folder_index_text(folder, folder.get("documents"))
        path = Path(folder.get("path"))
        path.write_text(text)

    for f in content_tree:
        folder_index(f)
    print(top_index_text(content_tree))


def content_file(pub):
    return Path(pub.doc_path) / "_content.csv"


def pub_contents(pub):
    return f"\n\n{pub.title}\n\n{read_content_csv(pub)}"


def read_content_csv(pub):
    path = content_file(pub)
    if not path.exists():
        write_content_csv(pub)
    return path.read_text()


def table_of_contents(pub, content_tree, word_count=False):
    def link(folder, pub, title, url, words):
        url = url.replace(pub.doc_path, "")[1:]
        url = url.replace("/", "-")
        if words:
            words = f" - {words} words"
        if folder:
            return f"\n## [{title}](/{pub.name}/{url}){words}\n\n"
        else:
            return f"* [{title}](/{pub.name}/{url}){words}\n"

    text = f"# {pub.title}\n\n"
    for f in content_tree:
        url = Path(f.get("path")).name
        title = f.get("title")
        # text += f"\n## [{title}](/{pub.name}/{url})\n\n"
        w = f["words"] if word_count else ""
        text += link(True, pub, title, f.get("path"), w)
        # if word_count:
        # text += f"{pub.words} words\n"
        for d in f.get("documents"):
            url = Path(d.get("path")).name
            title = d.get("title")
            # text += f"* [{title}](/{pub.name}/{url})\n"
            w = d["words"] if word_count else ""
            text += link(False, pub, title, d.get("path"), w)
            # if d["words"] == 0:
            #     print(d)
            #     Content.objects.filter(pk=d["id"]).delete()
    return text


def write_toc_index(pub, content_tree):
    toc = Path(pub.doc_path) / "Index.md"
    # print(f"TOC: {toc}")
    toc.write_text(table_of_contents(pub, content_tree))


def write_content_csv(pub):
    content = ""
    folder = Path(pub.doc_path)
    for i, d in enumerate(sorted(folder.iterdir())):
        if d.is_file():
            print(d)
            if str(d).endswith(".md"):
                content += f"{d.name},{i+1}\n"
        elif d.is_dir():
            content += f"{d.name}/Index.md,{i+1}\n"
            for j, f in enumerate(sorted(d.iterdir())):
                print(f)
                if str(f).endswith(".md"):
                    content += f"{d.name}/{f.name},{i+1},{j+1}\n"
    Path(content_file(pub)).write_text(content)
