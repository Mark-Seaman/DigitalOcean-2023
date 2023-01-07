from django.template.loader import render_to_string
from django.utils.timezone import localdate
from pathlib import Path
from random import choice
from re import split, sub

from publish.pub import get_pub, list_content
from publish.days import yesterday
from publish.document import document_body, document_title, title
from publish.files import read_file
from workshop.management.commands.edit import edit_file


def article_paragraphs(text):
    def is_paragraph(text):
        return len(text) > 250 and len(text) < 400

    return [x for x in split("\n\n", text) if is_paragraph(x)]


def article_path(pub, doc):
    return f"{pub.doc_path}/{doc}"


def article_posts(text):
    def is_post(text):
        return len(text) > 150 * 5 and len(text) < 400 * 5

    return [x for x in article_sections(text) if is_post(x)]


def article_sections(text):
    return [x for x in split(" *\#\# ", text)]


def article_url(pub, doc):
    return f"{pub.domain}{pub.url}/{doc}"


def create_history_file(date):
    return render_to_string("history.md", {"day": f'{date.strftime("%A")}'})


def create_sampler_file(date=None):
    def blog_daily_post(date):
        post = random_post(random_pub())
        print("BLOG", post["doc"])
        edit_file([post["doc"]])
        return render_to_string("pub/blog.md", post)

    def blog_weekly_post(date):
        docs = []
        for d in [yesterday(date, 7 - d) for d in range(8)]:
            doc_date = d.strftime("%A, %B %d")
            f = d.strftime("%m/%d")
            title = document_title(f"Documents/seamanslog.com/sampler/{f}.md")
            if not "Document not found" in title:
                link = d.strftime("%m-%d")
                doc = dict(date=doc_date, url=link, title=title)
                docs.append(doc)
        day = f'{date.strftime("%a, %B %d")}'
        return render_to_string("pub/blog_weekly.md", dict(day=day, docs=docs))

    if not date:
        date = localdate()
    if date.strftime("%a") == "Sun":
        return blog_weekly_post(date)
    else:
        return blog_daily_post(date)


def create_spirit_file(date):
    return render_to_string("spirit.md", {"day": f'{date.strftime("%B %-d")}'})


def create_toot_file():
    date = localdate()
    path = Path("Documents/mastodon/mdseaman") / date.strftime("_%m%d")
    article = random_article()
    message = random_message(article)
    if message:
        edit_file([article["doc"]])
        print(path, message)
        path.write_text(message)
        return [path]


def extract_post(path):
    text = read_file(path)
    paragraphs = article_posts(text)
    if paragraphs:
        return choice(paragraphs)


def extract_message(path, url):
    text = read_file(path)
    paragraphs = article_paragraphs(text)
    if paragraphs:
        text = choice(paragraphs)
        text = text.replace("\n", " ")
        return text + f"\n... \n\nRead more - {url}"


def random_article(pub=None):
    pub = random_pub()
    content = choice(list_content(pub))
    # return blog_data(pub, Path(content.path).name)
    doc = Path(content.path).name
    url = article_url(pub, doc)
    doc_path = article_path(pub, doc)
    title = document_title(doc_path)
    text = document_body(read_file(doc_path))
    return dict(pub=pub, url=url, doc=doc_path, title=title, text=text)


def random_message(article):
    for i in range(5):
        text = extract_message(article["doc"], article["url"])
        if text:
            return text


def random_post(pub):
    pub = get_pub(pub)
    for i in range(5):
        content = choice(list_content(pub))
        doc = Path(content.path).name
        text = extract_post(content.path)
        if text:
            return dict(
                pub=pub,
                title=title(text),
                text=text,
                doc=content.path,
                url=article_url(pub, doc),
            )


def random_pub():
    pubs = ("journey", "quest", "poem")
    pub = choice(pubs)
    return get_pub(pub)


def review_file(path):
    if not path:
        article = random_article()
        path = article["doc"]
    edit_file([path])
    print(f"REVIEW: {article['doc']}")
    return path
