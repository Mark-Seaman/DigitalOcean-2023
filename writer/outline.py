from pathlib import Path
from probe.probe_pub import test_pub_json
from re import findall, split, DOTALL
from django.template.loader import render_to_string

from publish.document import title
from writer.pub_script import pub_path


def create_index(path):
    text = Path(path).read_text()
    pattern = r'\n## ([^\n]*)?'
    matches = findall(pattern, text)
    links = [(match,match) for match in matches]
    text = render_to_string('pub/index.md', {'title': title(text), 'links': links})
    print(text)
    outfile = Path(path).parent / 'Index.md'
    if not outfile.exists():
        outfile.write_text(text)


def show_links(path):
    links = extract_links(path)
    for url,title in links:
        print('Title:', title)
        print('URL:', url)
        print()

def show_outlines(path):
    outlines = extract_outlines(path)
    for outline in outlines:
        print('Outline:', outline)
        print()

    
def create_ai_file(path, text):
    if not path.exists():
        outline = '# '+text.replace('###', '*')
        text = render_to_string('pub_script/draft.ai', {'outline': outline})
        path.write_text(text)
        print(path)


def write_outlines(path):
    outline = path/'Outline.md'
    index = path/'Index.md'
    o = split_outline(outline.read_text())
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


def test_extraction(path):
    # urls = extract_urls(path)
    # for url in urls:
    #     print(url)
    # print()

    # links = extract_links(path)
    # for url,title in links:
    #     print('Title:', title)
    #     print('URL:', url)
    #     print()

    outlines = extract_outlines(path)
    for title, url, outline in outlines:
        print('Title:', title)
        print('URL:', url)
        print('Outline:', outline)
        print()


