from pathlib import Path
from django.template.loader import render_to_string
from publish.files import count_files, read_csv_file, write_csv_file, write_file
from publish.text import line_count, no_blank_lines, text_lines
from publish.document import title
from .pub_script import pub_path, pub_script


def chapter_index(pub_name, chapter, num):
    plays = read_plays(pub_name)
    for play in plays:
        if play[1] == num:
            title = play[3].strip()
            if play[2] == num:
                chap = play[0].replace('.md', '')
                text = f'## Chapter {chapter} - {title}\n\n'
            f = play[0]
            d = f.replace('.md', '')
            p = pub_path(pub_name, d, f)
            if p.exists():
                text += f'* [{title}]({d})\n'
    path = pub_path(pub_name, chap, 'Index.md')
    write_file(path, text, overwrite=True)
    return text


def create_docs(pub_name):
    plays = read_plays(pub_name)
    for play in plays:
        f = play[0]
        d = f.replace('.md', '')
        p = pub_path(pub_name, d, f)
        if not p.exists():
            write_file(p, f'# {play[3]}\n')
            print('Create', f, play[3])
        # else:
        #     print(f, 'Exists')


def publish_playbook(pub_name):
    # print(f'publish_playbook({pub_name})')
    pub_script(['project', pub_name])
    return pub_script(['publish', pub_name])


def title_map(pub_name):
    csv = pub_path(pub_name, 'Index', '_plays.csv')
    table = read_csv_file(csv)
    return {row[1].strip(): row[0] for row in table}


def read_outline(pub_name):
    path = pub_path(pub_name, 'Index', 'Outline.md')
    return text_lines(no_blank_lines(path.read_text()))[1:]


def read_plays(pub_name):
    path = pub_path(pub_name, 'Index', '_plays.csv')
    return read_csv_file(path)


def read_toc(pub_name):

    def chapter_map(table):
        map = {}
        table = [row[:2] for row in table]
        for f, c in table:
            if c != 'None':
                map.setdefault(c, []).append(f)
                # print(f, c)

        return map

    def filename_map(table):
        map = {}
        for row in table:
            key = ','.join(row[1:])
            map[key] = row[0]
        return map

    path = pub_path(pub_name, 'Index', '_content.csv')
    table = read_csv_file(path)
    cmap = chapter_map(table)
    fmap = filename_map(table)
    return cmap, fmap


def write_chapters(pub_name):

    def create_chapter(chapter, fmap):
        cdir = fmap[chapter].replace('.md', '')
        d = pub_path(pub_name, cdir.replace('.md', ''))
        d.mkdir(exist_ok=True)
        return d

    cmap, fmap = read_toc(pub_name)
    for chapter in sorted(cmap, key=int):
        create_chapter(chapter, fmap)
    return f'{len(cmap)} Chapters'


def write_contents(pub_name):
    def folders(table):
        return {row[2].strip(): i for i, row in enumerate(table)}

    table = read_plays(pub_name)
    map = folders(table)
    text = ''
    for i, row in enumerate(table):
        file = row[0]
        folder = map.get(row[1])
        doc = map.get(row[2])
        if folder == doc:
            text += f'{file},{folder}\n'
        else:
            text += f'{file},{folder},{doc}\n'
    path = pub_path(pub_name, 'Index', '_content.csv')
    write_file(path, text)
    return f'{len(text_lines(text))} Lines in contents file'


def write_index(pub_name):

    #     def pub_index(cmap, fmap):
    #         text = f"# Index for {pub_name}\n\n"
    #         for i, chapter in enumerate(sorted(cmap, key=int)):
    #             text += f'Chapter {i}: {fmap[chapter]}'
    #             chapter_index(i, chapter, cmap[chapter], fmap)
    #         #     cdir = fmap[chapter].replace('.md','')
    #         #     text += f'{read_index(pub_name, cdir)}\n\n'
    #         # path = pub_path(pub_name, 'Index', 'Index.md')
    #         # path.write_text(text)
    #         print(text)
    #         return text

    #     def read_index(pub_name, chapter):
    #         path = pub_path(pub_name, chapter, 'Index.md')
    #         return path.read_text()

    #     cmap, fmap = read_toc(pub_name)
    #     text = pub_index(cmap, fmap)
    #     # print(text)
    #     return f'{line_count(text)} Lines in Index'
    pass


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
    plays = read_plays('apps')
    titles = {row[3].strip(): row[0] for row in plays}
    lines = read_outline('apps')
    text = ''
    for i, line in enumerate(lines):
        default = line.replace(' ', '')+'.md'
        file = titles.get(line.strip(), default)
        if not line.startswith('        '):
            c = i
        row = f'{file},{c},{i},{line}'
        text += row+'\n'
    # print(text)
    csv = pub_path(pub_name, 'Index', '_plays.csv')
    write_file(csv, text, overwrite=True)
    return f'{len(text_lines(text))} Lines in playlist'
