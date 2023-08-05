from pathlib import Path
from django.template.loader import render_to_string
from publish.files import read_csv_file, write_csv_file, write_file
from publish.text import text_lines

from .pub_script import pub_path


def read_files_table(pub_name):
    csv = pub_path(pub_name, 'Index', '_plays.csv')
    table = read_csv_file(csv)
    return {row[2].strip(): row[0] for row in table}


def read_outline(pub_name):
    path = pub_path(pub_name, 'Index', 'Outline.md')
    return path.read_text()


def read_plays(pub_name):
    path = pub_path(pub_name, 'Index', '_plays.csv')
    return read_csv_file(path)


def write_chapters(pub_name):

    def create_chapter(chapter):
        d = pub_path(pub_name, chapter.replace('.md', ''))
        d.mkdir(exist_ok=True)
        chapter_index(chapter)
        return d

    def chapter_index(chapter, docs, fmap):
        cdir = fmap[chapter].replace('.md','')
        path = pub_path(pub_name, cdir, 'Index.md')
        print(chapter, cdir, path)
        text = f'# Chapter {chapter} - {cdir}\n\n'
        for d in docs:
            text += f'* [{d}]({d})\n'
        path.write_text(text)

    # xooxoxxxxoxoooxxooxxxxooxooooo

    # def move_docs(chapter,doc):
    #     d = create_chapter(chapter)
    #     f = d.parent/'Index'/doc
    #     # print("FILE", f)
    #     if f.exists():
    #         print(f'mv {f} {d/doc}')
    #         f.rename(d/doc)

    def chapter_map(table):
        map = {}
        table = [row[:2] for row in table]
        for f, c in table:
            map.setdefault(c, []).append(f)
        return map

    def filename_map(table):
        map = {}
        for row in table:
            key = ','.join(row[1:])
            map[key] = row[0]
        # print(map)
        return map

    path = pub_path(pub_name, 'Index', '_content.csv')
    table = read_csv_file(path)
    cmap = chapter_map(table)
    fmap = filename_map(table)
    for chapter in sorted(cmap, key=int):
        chapter_index(chapter,cmap[chapter], fmap)
        
        # for key in sorted(map, key=int):
        #     print(f"Chapter {key}: {', '.join(map[key])}")
    # path = pub_path(pub_name, 'Index', '_content.csv')
    # table = read_csv_file(path)
    # for row in table:
    #     if not row[2:]:
    #         print('NEW CHAPTER:', row)
    #         create_chapter(row[0])
    #         chapter = row[0]
    #     # move_docs(chapter,row[0])
    #     # move_docs(chapter,row[0].replace('.md', '.ai'))
    return f'{len(cmap)} Chapters'


def write_contents(pub_name):
    def folders (table):
        return {row[2].strip(): i for i,row in enumerate(table)}

    table = read_plays(pub_name)
    map = folders(table)
    text = ''
    for i,row in enumerate(table):
        file = row[0]
        folder = map.get(row[1])
        doc = map.get(row[2])
        if folder == doc:
            text += f'{file},{folder}\n'
        else:
            text += f'{file},{folder},{doc}\n'
    path = pub_path(pub_name, 'Index', '_content.csv')
    write_file(path, text, overwrite=False)
    return f'{len(text_lines(text))} Lines in contents file'


def write_index(pub_name):
    path = pub_path(pub_name, 'Index', 'Index.md')

    text = path
    return text


def write_playbook(pub_name):

    def play(row):
        title = row[1].strip()
        md = row[0]
        ai = row[0].replace('.md', '.ai')
        x = dict(title=title, md=md, ai=ai)
        x['prompt'] = prompt(x)
        return x

    def prompt(x):
        return render_to_string('pub_script/ai_prompt.md', {'plays': [x]})

    def write_play(play):
        path = pub_path(pub_name, 'Index', play['ai'])
        path.write_text(play['prompt'])
        path = pub_path(pub_name, 'Index', play['md'])
        path.write_text(play['prompt'])

    path = pub_path(pub_name, 'Index', '_plays.csv')
    table = read_csv_file(path)
    table = [play(row) for row in table if row][1:]
    for row in table:
        write_play(row)

    data = {'plays': table}
    text = render_to_string('pub_script/playbook_prompts.md', data)
    path = pub_path(pub_name, 'Index', 'Index.md')
    path.write_text(text)
    # print(playbook)
    return f'{len(text_lines(text))} Lines in playbook'


def write_plays_csv(pub_name):

    map = read_files_table(pub_name)
    path = pub_path(pub_name, 'Index', 'Outline.md')
    table = read_csv_file(path)
    text = ''
    for row in table:
        if row:
            if not row[0].startswith('        '):
                chapter = row[0][4:]
            title = row[0].strip()
            if title.startswith('# '):
                title = title[2:]
            f = map.get(title, title+'.md')
            text += f'{f},{chapter},{title}\n'

    csv = pub_path(pub_name, 'Index', '_plays.csv')
    write_file(csv, text)
    # return read_csv_file(csv)
    return f'{len(text_lines(text))} Lines in playlist'


