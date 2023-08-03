from django.template.loader import render_to_string

from publish.files import read_csv_file, write_csv_file

from .pub_script import pub_path


def read_outline(pub_name):
    path = pub_path(pub_name, 'Index', 'Outline.md')
    return path.read_text()


def read_plays(pub_name):
    path = pub_path(pub_name, 'Index', 'plays.csv')
    return read_csv_file(path)


def write_plays(pub_name):
    path = pub_path(pub_name, 'Index', 'Outline.md')
    table = read_csv_file(path)
    table = [(".md", row[0]) for row in table if row]
    csv = pub_path(pub_name, 'Index', 'plays.csv')
    # write_csv_file(csv, table)
    return read_csv_file(csv)


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

    path = pub_path(pub_name, 'Index', 'plays.csv')
    table = read_csv_file(path)
    table = [play(row) for row in table if row][1:]
    for row in table:
        write_play(row)

    data = {'plays': table}
    playbook = render_to_string('pub_script/playbook_prompts.md', data)
    path = pub_path(pub_name, 'Index', 'Index.md')
    path.write_text(playbook)
    print(playbook)
    return 'ok'
