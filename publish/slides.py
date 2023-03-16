from os import system
from pathlib import Path
from re import findall, sub

from django.template.loader import render_to_string

from course.slides import render_slides
from workshop.management.commands.edit import edit_file

from .document import document_body, document_html, document_title
from .files import read_file, read_json, write_file
from .text import text_lines


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


def create_markdown_files(outline_file, markdown_dir):
    text = read_file(outline_file)
    index = create_index_file(markdown_dir, text)
    for topic in find_subtopics(text):
        create_topic_file(markdown_dir, topic)
    return index


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

    if args:
        outline_file = args[0] + '.ol'
    else:
        outline_file = 'Documents/shrinking-world.com/workshop/publish/Publish.ol'
    markdown_file = outline_file.replace('.ol', '-slides.md')
    print(f'Slides: {outline_file} {markdown_file}')
    text = read_file(outline_file)
    text = slides(text)
    write_file(markdown_file, text)
    system('open http://localhost:8000/slides')
    return markdown_file


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


def plant(args):
    outline_file = f'Documents/shrinking-world.com/greenhouse/{args[0]}'
    markdown_dir = args[1]
    return create_markdown_files(outline_file, markdown_dir)


def slides_view_context(**kwargs):
    pub = kwargs.get('pub', 'webapps')
    doc = kwargs.get('doc', 'WebApps')
    pub = kwargs.get('pub', 'publish')
    # doc = kwargs.get('doc', 'Publish')
    # json = f"Documents/shrinking-world.com/workshop/{pub}/slides_settings.json"
    # md_path = f'Documents/shrinking-world.com/workshop/{pub}/{doc}-slides.md'
    json = f"Documents/shrinking-world.org/slides_settings.json"
    md_path = f'Documents/shrinking-world.org/L2-howto-slides.md'
    kwargs = read_json(json)
    md_text = read_file(md_path)
    text = render_slides(md_text, **kwargs)
    kwargs.update(dict(server=True, text=text))
    return kwargs


def write_lesson_files(path):

    def write_lesson(path, text):
        if not Path(path).exists():

            text += '''
        
## Video

<div style="position: relative; padding-bottom: 56.25%; height: 0;"><iframe style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; border: 0;" src="https://www.tella.tv/video/cldtdbws0030n0fld7qun3l85/embed" allowfullscreen allowtransparency></iframe></div>

## Learn More

* [Publishing for Writers Slides](slides)
* [Publishing](Publish-1.md)
* [Publishing Tools](Publish-2.md)
* [Publishing Requirements](Publish-3.md)
* [Four biggest mistakes](Publish-4.md)
* [Use Ghost](Publish-5.md)
'''
            write_file(path, text)

    text = read_file(path+'.ol')
    x = ''
    lesson = 0
    for line in text_lines(text):
        if not line:
            x += f'{line}\n'
        elif not line.startswith('    '):
            x += f'# {line}\n'
        elif not line.startswith('        '):
            lesson += 1
            write_lesson(f'{path}-{lesson}.md', x)
            x = ''
            line = line.replace('    ', '')
            x += f'\n\n## {line}\n'
        elif not line.startswith('            '):
            line = line.replace('        ', '')
            x += f'\n### {line}\n'
        else:
            line = line.replace('            ', '')
            x += f'* {line}\n'

    write_lesson(f'{path}-{lesson+1}.md', x)
    # print(x)
    return x


def write_markdown(outline_file, markdown_file):
    text = read_file(outline_file)
    text = text.replace('\n', '\n\n# ')
    text = '# ' + text.replace('    ', '#')
    write_file(markdown_file, text)


def write_workshop(args):
    path = 'Documents/shrinking-world.com/workshop/publish/Publish'
    print("WORKSHOP: ", path, args)
    write_lesson_files(path)
    create_slides([path])
    edit_file(path+'-slides.md')
    system('open http://localhost:8002/workshop/publish')
