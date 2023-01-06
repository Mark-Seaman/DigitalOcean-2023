from django.template.loader import render_to_string
from pathlib import Path


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
            if not doc["path"].endswith("Index.md"):
                # print(doc)
                docs.append(link(doc))
        title = f"Month {Path(path).parent.name}"
        data = dict(title=title, docs=docs)
        return render_to_string("pub/pub_index.md", data)

    def top_index_text(content_tree):
        path = Path(pub.doc_path) / "Index.md"
        docs = [link(f) for f in content_tree if f["path"] != str(path)]
        # print(docs)
        data = dict(title="Table of Contents", docs=docs)
        text = render_to_string("pub/pub_index.md", data)
        path.write_text(text)

    def folder_index(folder):
        text = folder_index_text(folder, folder.get("documents"))
        path = Path(folder.get("path"))
        path.write_text(text)

    for f in content_tree:
        folder_index(f)
    top_index_text(content_tree)


def content_file(pub):
    return Path(pub.doc_path) / "_content.csv"


def pub_contents(pub):
    return f"\n\n{pub.title}\n\n{read_content_csv(pub)}"


def read_content_csv(pub):
    path = content_file(pub)
    if not path.exists():
        write_content_csv(pub)
    return path.read_text()


def show_word_count(label, word_count, post_count=None):
    words = f"{int(word_count / 1000)}k" if word_count > 1000 else word_count
    pages = int(word_count / 250)
    if post_count:
        return f"{label} - {post_count} Posts, {words} Words, {pages} Pages\n"
    else:
        return f"{label} - {post_count} Posts, {words} Words, {pages} Pages\n"


def table_of_contents(pub, content_tree, word_count=False):
    def link(folder, pub, title, url, words):
        url = url.replace(pub.doc_path, "")[1:]
        url = url.replace("/", "-")
        words = int(words) if words else 0
        if folder:
            label = f"\n## [{title}](/{pub.name}/{url})"
            return show_word_count(label, words)
            # return f"\n## [{title}](/{pub.name}/{url}){words}\n\n"
        else:
            label = f"* [{title}](/{pub.name}/{url})"
            return show_word_count(label, words)
            # return f"* [{title}](/{pub.name}/{url}){words}\n"

    text = f"# {pub.title}\n\n"
    for f in content_tree:
        url = Path(f.get("path")).name
        title = f.get("title")
        w = f["words"] if word_count else ""
        text += link(True, pub, title, f.get("path"), w)
        for d in f.get("documents"):
            url = Path(d.get("path")).name
            title = d.get("title")
            w = d["words"] if word_count else ""
            text += link(False, pub, title, d.get("path"), w)
    return text


def write_toc_index(pub, content_tree):
    toc = Path(pub.doc_path) / "Index.md"
    # print(f"TOC: {toc}")
    toc.write_text(table_of_contents(pub, content_tree))


def write_content_csv(pub):
    def is_markdown(path):
        x = str(path)
        return path.is_file() and x.endswith(".md") and not x.endswith("Index.md")

    content = "Index.md,0\n"
    folder = Path(pub.doc_path)
    for i, d in enumerate(sorted(folder.iterdir())):
        if d.is_file():
            if is_markdown(d):
                # print(d)
                content += f"{d.name},{i+1}\n"
        elif d.is_dir():
            content += f"{d.name}/Index.md,{i+1}\n"
            for j, f in enumerate(sorted(d.iterdir())):
                if is_markdown(f):
                    # print(f)
                    content += f"{d.name}/{f.name},{i+1},{j+1}\n"
    Path(content_file(pub)).write_text(content)
