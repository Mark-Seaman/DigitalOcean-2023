from pathlib import Path

from publish.days import is_old

from publish.files import read_file
from publish.import_export import get_pub_contents
from publish.management.commands.edit import edit_file
from publish.models import Content, Pub
from publish.publication import all_pubs, get_pub
from publish.shell import banner
from publish.text import word_count


def count_nodes():
    pubs = Pub.objects.all()
    contents = Content.objects.all()
    words = sum([x.words for x in contents])
    pages = int(words/250)
    return len(pubs), len(contents), words, pages


# def count_pub_words(pub_name):
#     #     f = Path(f'Documents/markseaman.info/words/{pub_name}')
#     #     pub = get_pub(pub_name)
#     words = measure_pub_words(pub=pub_name)
#     return words
#     f.write_text(words)
#     # if not f.exists() or is_old(f):
#     #     f.write_text(words)
#     # else:
#     #     words = f.read_text()
#     # return pub.words


def measure_pub_words(**kwargs):

    def pub_words(pub):
        output = banner(pub.name)
        words = 0
        pub_content = get_pub_contents(pub)
        for content in pub_content:
            w = chapter_words(content)
            words += w
            output += f'\n{content["title"]:45} {content["words"]:5},{w:5} words {int(w/250):10} pages\n\n'
            for doc in content["documents"]:
                output += f'    {doc["title"]:40}  {doc["words"]:5} words\n'
        output += f'\nPub Words: {words:40} {int(words/250):10} pages'
        pub.words = words
        pub.save()
        return output

    def chapter_words(content):
        words = content["words"]
        for doc in content["documents"]:
            words += doc["words"]
        return words

    # def save_published_words():
    #     text = '# Published Words\n\n'
    #     for pub in all_pubs():
    #         text += f'* [{pub.title}](/{pub.name}) - {pub.words} words\n'
    #     path = Path("Documents/markseaman.info/words/Published.md")
    #     path.write_text(text)

    p = kwargs.get('pub')
    pubs = [get_pub(p)] if p else all_pubs()
    text = ''
    for pub in pubs:
        path = Path("Documents/markseaman.info/words") / pub.name
        path.write_text(pub_words(pub))
        text += path.read_text() + '\n\n'
    save_published_words()
    return text


# def show_pub_words(pub=None):
#     text = "PUB WORDS\n\n"
#     pubs = [pub] if pub else all_pubs()
#     for pub in pubs:
#         path = word_count_file(pub)
#         text += f"\n\n---\n\n{path}\n\n---\n\n"
#         text += path.read_text()
#     return text


# def word_count_file(pub):
#     path = Path("Documents/markseaman.info") / "words" / pub.name
#     if not path.exists():
#         path.write_text('')
#     return path


def save_published_words():
    text = '# Published Words\n\n'
    total = 0
    for t in ['book', 'blog', 'course', 'private']:
        words = 0
        text2 = ''
        for pub in all_pubs(t):
            link = f'[{pub.title}](/{pub.name})'
            text2 += f'* {link:40} {pub.words:5} words {int(pub.words/250):5} pages\n'
            words += pub.words
            total += pub.words
        text += f'\n## Pubs - {t:30} {words:7} words {int(words/250):5} pages\n\n{text2}\n'
    text += f'\n\n## Grand Total  {total:7} words {int(total/250):5} pages'

    path = Path("Documents/markseaman.info/words/Published.md")
    path.write_text(text)


# def show_pubs(pub=None):
#     if pub:
#         p = get_pub(pub)
#         return f'{p.name:15} -  {p.title:35} - {p.words:5} words - {int(p.words/250)} pages'
#     else:
#         output = "PUBLICATIONS:\n\n"
#         for t in ['book', 'blog', 'course', 'private']:
#             text = ''
#             words = 0
#             for p in all_pubs(t):
#                 text += f'    {p.name:15} -  {p.title:35} - {p.words:5} words\n'
#                 words += p.words
#                 get_pub(p.name)
#             output += f'\nPubs - {t} - {words} words - {int(words/250)} pages\n{text}\n'
#         return output


# def show_pub_details(pub):
#     content = pub.content_set.all()
#     output = f'Pub Contents - {pub.name} - {pub.title}'
#     total_words = 0
#     for f in content.filter(folder=0):
#         folder_words = word_count(read_file(f.path))
#         output += f'\n{f.title} - {f.path} - {folder_words} words\n'
#         for d in content.filter(folder=f.order):
#             words = word_count(read_file(d.path))
#             folder_words += words
#             output += f'    {d.title} - {d.path} - {words} words\n'
#         output += f'    Words in {f.title}: {folder_words} words\n'
#         total_words += folder_words
#     output += f'\nTotal Words in {pub.title}: {total_words} words, {int(total_words/250)} pages\n'
#     pub.words = total_words
#     pub.save()
#     return output
