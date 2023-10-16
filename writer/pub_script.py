from os import getenv, system
from pathlib import Path
from re import match
from shutil import copyfile
from django.template.loader import render_to_string

from markdown import markdown

from publish.document import title
from publish.files import create_directory, read_json
from publish.publication import build_pubs
from publish.text import text_join, text_lines, word_count

from .cover import create_book_cover
from .outline import create_index, create_outlines


def ai_script(args):
    if not args[2:]:
        return 'usage: ai pub chapter doc'
    pub_name, chapter, doc = args
    return f'Running ai on {pub_path(pub_name,chapter,doc)}'


def build_script(args):
    text = build_pubs(verbose=False)
    return f'Build all pubs: {text}'


def chapter_list(pub):
    path = pub_path(pub)
    x = []
    chapters = sorted(path.iterdir())
    for chapter in chapters:
        if chapter.is_dir():
            x.append(pub_link(pub, chapter.name))
    return x
    # return [pub_link(pub, chapter.name) for chapter in path.iterdir() if chapter.is_dir()]


def chapter_script(args):
    if not args[1:]:
        return 'usage: chapter pub-name chapter-name'
    pub, chapter = args
    chapter_path = pub_path(pub, chapter)
    create_directory(chapter_path)
    doc_script([pub, chapter, 'Outline.md'])
    return f'chapter ({chapter_path})'


def cover_script(args):
    if not args:
        return 'usage: pub cover write'
    pub = args[0]
    images = pub_path(pub).parent/'Images'
    return create_book_cover(images)


def create_outline(args):
    def markdown_to_outline(text):
        # Define a regular expression pattern to match headings
        heading_pattern = r'^(#+)\s+(.*)'
        lines = text.split('\n')
        outline = ''
        for line in lines:
            # Check if the line matches the heading pattern
            x = match(heading_pattern, line)
            if x:
                # Extract the heading level and text
                level = len(x.group(1))
                text = x.group(2)
                # Add the heading to the outline with the appropriate indentation
                outline += '    ' * (level - 1) + text + '\n'
        return outline

    path = pub_path(args[0], args[1], args[2])
    text = markdown_to_outline(path.read_text())
    if args[3:]:
        text = extract_outline(text, args[3])
    return text


def create_pub_content(path):
    args = path.split('/')
    if args[2:]:
        doc_script(args[:3])
        return pub_url(args[0], args[1], args[2])
    elif args[1:]:
        chapter_script(args[:2])
        return pub_url(args[0], args[1])
    elif args:
        project_script(args)
        return pub_url(args[0])


def doc_ai(pub, chapter, doc):
    doc = doc.replace('.md', '.ai')
    path = pub_path(pub, chapter, doc)
    if path.exists():
        return markdown(path.read_text())


def doc_html(pub, chapter, doc):
    return markdown(read_pub_doc(pub, chapter, doc),  extensions=['tables'])


def doc_human(pub, chapter, doc):
    doc = doc.replace('.md', '.txt')
    path = pub_path(pub, chapter, doc)
    if path.exists():
        return markdown(path.read_text())


def doc_link(pub, chapter, doc):
    url = f'/writer/{pub}/{chapter}/{doc}'
    # title = doc_title(pub, chapter, doc)
    # return f'<a href="{url}">{title}</a>'
    return f'<a href="{url}">{doc[:-3]}</a>'


def doc_list(pub, chapter):
    path = pub_path(pub, chapter)
    for ai in path.glob('*.ai'):
        md = Path(str(ai).replace('.ai', '.md'))
        if not md.exists():
            copyfile(ai, md)
    return [doc_link(pub, chapter, doc.name) for doc in sorted(path.glob('*.md')) if doc.is_file()]


def doc_script(args, edit=False):
    if not args[2:]:
        return 'usage: doc pub-name chapter-name doc-name'
    pub, chapter, doc = args[:3]
    path = pub_path(pub, chapter, doc)
    for d in pub_doc_files(path):
        if not Path(d).exists():
            Path(d).write_text('')
    return str(path)


def pub_doc_title(pub, chapter, doc):
    return title(read_pub_doc(pub, chapter, doc))


def doc_text(pub, chapter, doc):
    lines = text_lines(read_pub_doc(pub, chapter, doc))[2:]
    return text_join(lines)


def doc_view_data(**kwargs):
    pub = kwargs.get('pub', 'ghost')
    chapter = kwargs.get('chapter')
    doc = kwargs.get('doc')

    pub_js = pub_path() / pub / "pub.json"
    kwargs.update(read_json(pub_js))

    if doc and chapter and pub:
        kwargs['text'] = read_pub_doc(pub, chapter, doc)
        kwargs['words'] = word_count(kwargs['text'])
        kwargs['html'] = doc_html(pub, chapter, doc)
        kwargs['ai'] = doc_ai(pub, chapter, doc)
        kwargs['human'] = doc_human(pub, chapter, doc)
    if chapter and pub:
        kwargs['docs'] = doc_list(pub, chapter)
    if pub:
        kwargs['chapters'] = chapter_list(pub)
    kwargs['pubs'] = pub_list()
    kwargs['menu'] = get_menu(pub, chapter, doc)
    return kwargs


def edit_doc_script(pub, chapter, doc):
    path = pub_path(pub, chapter, doc)
    files = pub_doc_files(path)
    edit_files(files)
    return str(path)


def execute_pub_script(args):
    if not args:
        return 'usage: script script-file'
    script = Path(args[0])
    if not script.exists():
        return f'SCRIPT not found: (script)'
    commands = text_lines(script.read_text())
    commands = [pub_script(c.strip().split(' '))
                for c in commands if c.strip()]
    return text_join(commands)


def extract_outline(text, section_number):
    lines = text.split('\n')
    outline = ''
    matching = False
    for line in lines:
        i = len(line)-len(line.lstrip())
        if matching == True:
            if indent >= i:
                return outline
            outline += line[indent:]+'\n'
        elif line.lstrip().startswith(section_number):
            matching = True
            indent = i
            outline += line[indent:]+'\n'
    return outline


def edit_files(files):
    editor = getenv("EDITOR")
    editor = editor.replace(' -w', '')
    command = f'"{editor}" -w  {" ".join(files)}'
    print(command)
    system(command)


def files_script(args):
    if not args:
        return 'usage: files pub-name'
    pub_root = Path(f'{getenv("SHRINKING_WORLD_PUBS")}/{args[0]}')
    files = pub_root.rglob('*')
    files = [str(f).replace(str(pub_root)+'/', '    ')
             for f in files if f.is_file()]
    return f'Files:\n\n{text_join(files)}'


def get_menu(pub, chapter, doc):
    items = [("Publications", "/pubs/book"),
             ("Pubs", pub_url())]
    if pub:
        items.append(("Chapters", pub_url(pub)),)
    if chapter:
        items.append(("Docs", pub_url(pub, chapter)),)
    return {"title": ('GhostWriter', '/writer/'),
            "items": items}


def project_script(args):
    def make_json(pub_dir):
        pub_name = pub_dir
        pub_root = pub_path() / pub_dir
        pub_root.mkdir(exist_ok=True, parents=True)
        js = pub_root / f'pub.json'
        if not js.exists():
            data = dict(pub_name=pub_name, pub_dir=pub_dir,
                        tag_line='AI tools for Authors')
            json = render_to_string('pub_script/pub.json', data)
            js.write_text(json)
        return f'JSON file: {js}\n'

    text = f"Create Pub: {args[0]}\n"
    if not args:
        text += 'usage: project pub-name'
        return text
    text += make_json(args[0])
    chapter_script([args[0], 'Index'])
    return text


def pub_doc_files(path):
    path1 = str(path)
    path2 = str(path).replace('.md', '.txt')
    path3 = str(path).replace('.md', '.ai')
    if Path(path2).exists():
        return [path1, path2, path3]
    else:
        return [path1, path3]


def pub_edit(**kwargs):
    pub = kwargs.get('pub')
    chapter = kwargs.get('chapter')
    doc = kwargs.get('doc')
    edit_doc_script(pub, chapter, doc,)
    url = pub_url(pub, chapter, doc)
    return url


def pub_link(pub, chapter=None):
    if chapter:
        url = f'/writer/{pub}/{chapter}'
        title = chapter
    else:
        url = f'/writer/{pub}'
        title = pub

    return f'<a href="{url}">{title}</a>'


def pub_list():
    path = pub_path()
    pubs = []
    for pub in path.glob('*/pub.json'):
        if (pub.parent/'AI').is_dir() and pub.parent.parent.name == "Shrinking-World-Pubs":
            pubs.append(pub_link(pub.parent.name))
    return pubs


def pub_path(pub=None, chapter=None, doc=None):
    path = Path(f'{getenv("SHRINKING_WORLD_PUBS")}')

    if doc and chapter and pub:
        path = path/pub/'AI'/chapter/doc
    elif chapter and pub:
        path = path/pub/'AI'/chapter
    elif pub:
        path = path/pub/'AI'
    else:
        path = path
    return path


def pub_script(command_args):
    if not command_args:
        return "Invalid command: {}".format(command_args) + usage
    command = command_args[0]
    args = command_args[1:]
    if command == 'ai':
        from .ai import pub_ai
        if not args[2:]:
            return 'usage: pub ai ghost GhostWriter Draft.md'
        pub_ai(pub=args[0], chapter=args[1], doc=args[2])
    if command == 'build':
        output = build_script(args)
    elif command == 'chapter':
        output = chapter_script(args)
    elif command == 'cover':
        output = cover_script(args)
    elif command == 'doc':
        output = doc_script(args)
    elif command == 'edit':
        output = edit_doc_script(args[0], args[1], args[2])
    elif command == 'files':
        output = files_script(args)
    elif command == 'index':
        path = pub_path(args[0], args[1])
        output = create_index(path)
    elif command == 'outline':
        path = pub_path(args[0], args[1])
        output = create_outlines(path)
    elif command == 'project':
        output = project_script(args)
    elif command == 'publish':
        from .publisher import publish_script
        output = publish_script(args)
    elif command == 'script':
        output = execute_pub_script(args)
    elif command == 'test':
        output = test_script(args)
    else:
        output = "Invalid command: {}".format(command) + usage
    return output


def pub_url(pub=None, chapter=None, doc=None):
    if doc:
        return f'/writer/{pub}/{chapter}/{doc}'
    if chapter:
        return f'/writer/{pub}/{chapter}'
    if pub:
        return f'/writer/{pub}'
    return f'/writer/'


def read_pub_doc(pub, chapter, doc):
    path = pub_path(pub, chapter, doc)
    if not path.exists():
        path.write_text(f'# {chapter} {doc}')
        path2 = str(path).replace('.md', '.ai')
        path2.write_text(f'# {chapter} {doc}')
    if not path.exists():
        return f"FILE NOT FOUND: {path}"
    return path.read_text()


usage = '''

usage:
    build
    test

    project GhostWriter writer
    chapter GhostWriter Chapter1
    doc GhostWriter Chapter1 A-Outline.md
    edit GhostWriter Chapter1
    publish GhostWriter Chapter1 FinalVerson.md

    files GhostWriter Chapter1
    ai GhostWriter Chapter1 Outline1
    md GhostWriter Chapter1 Outline1
    txt GhostWriter Chapter1 Outline1

    # outline GhostWriter Chapter1 Outline1
    # expand GhostWriter Chapter1 Outline1

'''


def test_script(args):
    # if args:
    #     return 'usage: test'
    from publish import publish_script
    text = publish_script(args)

    # text = f'Pubs:\n\n{[str(p) for p in all_pubs()]}\n'
    # text += get_pub_info(args[0])

    return f'Test all pubs:\n\n{text}'
