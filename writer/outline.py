from pathlib import Path
from re import DOTALL, findall, split
from shutil import copyfile

from django.template.loader import render_to_string

from publish.document import title


def create_index(path):
    outline = path/'Outline.md'
    index = path/'Index.md'
    text = outline.read_text()
    pattern = r'\n## ([^\n]*)?'
    matches = findall(pattern, text)
    links = [(match,match) for match in matches]
    text = render_to_string('pub/index.md', {'title': title(text), 'links': links})
    print(text)
    if not index.exists():
        index.write_text(text)


def show_links(path):
    links = extract_links(path)
    for url,title in links:
        print('Title:', title)
        print('URL:', url)
        print()


def create_ai_file(path, text):
    outline = '# '+text.replace('###', '*')
    text = render_to_string('pub_script/draft.ai', {'outline': outline})
    path.write_text(text)
    md = Path(str(path).replace('.ai', '.md'))
    if not md.exists():
        copyfile(path, md)
        print(path)


def create_outlines(path):
    outline = path/'Outline.md'
    index = path/'Index.md'
    o = split_outline(outline.read_text())[1:]
    i = extract_links(index)
    for link, topics in zip(i, o):
        f = link[0].replace('.md', '.ai')
        create_ai_file(path/f, topics['outline'])


def split_outline(outline):
    return [dict(title=title('# '+x), outline=x) for x in split(r'\n## ', outline)]


def extract_urls(file_path):
    text = Path(file_path).read_text()
    url_pattern = r'\[(.*?)\]\((.*?)\)'
    matches = findall(url_pattern, text)
    urls = [match[1] for match in matches]
    return urls


def extract_links(file_path):
    text = Path(file_path).read_text()
    url_pattern = r'\[(.*?)\]\((.*?)\)'
    matches = findall(url_pattern, text)
    urls = [(match[1], match[0]) for match in matches]
    return urls


def extract_outlines(file_path):
    text = Path(file_path).read_text()
    url_pattern = r'(### (.*)?\n)*'
    matches = findall(url_pattern, text)
    return [match for match in matches]


def show_outlines(path):
    outlines = extract_outlines(path)
    for outline in outlines:
        print('Outline:', outline)
        print()

    
