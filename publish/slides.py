from django.template.loader import render_to_string
from re import findall, sub

from course.slides import render_slides
from publish.files import read_file, read_json, write_file
from publish.text import text_lines
from workshop.management.commands.edit import edit_file


def create_slides(args):
    def slides(text):
        x = ''
        for line in text_lines(text):
            if not line:
                x += f'{line}\n'
            elif not line.startswith('    '):
                x += f'# {line}\n'
            elif not line.startswith('        '):
                line = line.replace('    ', '')
                x += f'\n\n## {line}\n'
            elif not line.startswith('            '):
                line = line.replace('        ', '')
                x += f'\n### {line}\n'
            else:
                line = line.replace('            ', '')
                x += f'* {line}\n'
        return x

    outline_file = 'Documents/shrinking-world.com/slides/Publish.ol'
    markdown_file = 'Documents/shrinking-world.com/slides/Publish.md'
    text = read_file(outline_file)
    text = slides(text)
    write_file(markdown_file, text)
    return markdown_file


def plant(args):
    outline_file = f'Documents/shrinking-world.com/greenhouse/{args[0]}'
    markdown_dir = args[1]
    return create_markdown_files(outline_file, markdown_dir)


def create_markdown_files(outline_file, markdown_dir):
    text = read_file(outline_file)
    index = create_index_file(markdown_dir, text)
    for topic in find_subtopics(text):
        create_topic_file(markdown_dir, topic)
    return index


def create_index_file(markdown_dir, outline):
    def link(topic):
        return f"[{topic[1]}]({f'{(topic[0]+1):02}.md'})"

    docs = [link(topic) for topic in find_subtopics(outline)]
    topic = text_lines(outline)[0]
    data = dict(title=topic, docs=docs)
    text = render_to_string("pub/pub_index.md", data)
    md = f'{markdown_dir}/Index.md'
    write_file(md, text)
    return md


def create_topic_file(markdown_dir, topic):
    f = f'{markdown_dir}/{(topic[0]+1):02}.md'
    title = topic[1]
    text = render_to_string("pub/pub_lesson.md", dict(title=title))
    write_file(f, text)


def find_subtopics(text):
    return [(i, sub(r'    (\w*)', r'\1', x))
            for i, x in enumerate(findall('        .*', text))]


def markdown(args):
    f = f'Documents/shrinking-world.com/greenhouse/{args[0]}'
    md = f.replace('.ol', '.md')
    write_markdown(f, md)
    edit_file(md)


def slides_view_context(**kwargs):
    json = f"Documents/shrinking-world.com/slides/slides_settings.json"
    md_path = f'Documents/shrinking-world.com/slides/Publish.md'
    kwargs = read_json(json)
    md_text = read_file(md_path)
    text = render_slides(md_text, **kwargs)
    kwargs.update(dict(server=True, text=text))
    return kwargs


def write_markdown(outline_file, markdown_file):
    text = read_file(outline_file)
    text = text.replace('\n', '\n\n# ')
    text = '# ' + text.replace('    ', '#')
    write_file(markdown_file, text)
