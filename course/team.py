from pathlib import Path
from django.template.loader import render_to_string

from publish.document import document_body, document_html, document_title, title
from publish.files import write_file

from .course import course_settings, read_document
from .models import Team


def get_page(team=None, milestone=None, role=None):
    if not team:
        path = page_path('TeamProjects.md')
        write_page(path)
        return read_page(path)
    t = Team.objects.get(pk=team)
    if not milestone:
        path = page_path('TeamProject.md', team)
        write_page(path, t)
        return read_page(path)
    if not role:
        path = page_path('Feedback.md', team, milestone)
        if not path.exists():
            write_page(path, t, milestone)
        if path.exists():
            return read_page(path)
        path = page_path('Milestone.md', team, milestone)
        if not path.exists():
            write_page(path, t, milestone)
        return read_page(path)


def read_page(path):
    if path.exists():
        text = path.read_text()
        t = title(text)
        markdown = document_body(text)
        html = document_html(markdown)
        return dict(title=t, html=html, path=path)
    else:
        return dict(title='NO FILE', html='<h1>NO FILE FOUND</h2>', path=path)


def page_path(doc=None, team=None, milestone=None, role=None):
    path = Path(f'Documents/shrinking-world.com/cs350/team')
    if not doc:
        return path
    if not team:
        return path/doc
    if not milestone:
        return path/team/doc
    if not role:
        return path/team/milestone/doc
    return path/team/milestone/role/doc


def team_view_data(user, **kwargs):
    kwargs = course_settings(**kwargs)
    course = kwargs["course_object"]
    team = kwargs.get('team')
    milestone = kwargs.get('milestone')
    role = kwargs.get('role')
    if user.is_anonymous:
        kwargs['doctype'] = 'docs'
        kwargs['doc'] = 'StudentWorkspace.md'
        html = read_document(course, kwargs)
        kwargs.update(dict(title=course.title, html=html))
    elif not team:
        kwargs['doctype'] = 'docs'
        kwargs['doc'] = 'TeamProjects.md'
        html = read_document(course, kwargs)
        kwargs.update(dict(title=course.title, html=html))
    elif not milestone:
        kwargs.update(get_page(str(team)))
    elif not role:
        kwargs.update(get_page(str(team), str(milestone)))
    return kwargs


def setup_team_pages():
    for t in Team.objects.all():
        get_page(str(t.pk))
        get_page(str(t.pk), '1')
        get_page(str(t.pk), '2')
        get_page(str(t.pk), '3')
        get_page(str(t.pk), '4')
        get_page(str(t.pk), '5')
        get_page(str(t.pk), '6')
        get_page(str(t.pk), '7')


def setup_teams():
    Team.objects.get_or_create(name='BridgeOut', pk=1)
    Team.objects.get_or_create(name='Shop Zone', pk=2)
    Team.objects.get_or_create(name='PixlPix', pk=3)
    Team.objects.get_or_create(name='ClipBoard', pk=4)

    x = Team.objects.get(pk=1)
    x.github = 'https://github.com/josh-flatt/cs350'
    x.server = 'https://plankton-app-5fssv.ondigitalocean.app'
    x.save()

    x = Team.objects.get(pk=2)
    x.github = 'https://github.com/alexhovick/ShopZoneCS350'
    x.server = 'https://shopzone-app.netlify.app'
    x.save()

    x = Team.objects.get(pk=3)
    x.github = 'https://github.com/Esi-Mena/Instagram'
    x.server = 'https://instagram-production.up.railway.app'
    x.save()

    x = Team.objects.get(pk=4)
    x.github = 'https://github.com/JLeFevre559/CS350-Clipboard'
    x.server = 'https://clipboard-unco-cs350.vercel.app'
    x.save()

    for t in Team.objects.all():
        print(t.pk, t.name, t.github, t.server)


def write_team_page(path, team, milestone=None):
    path.parent.mkdir(exist_ok=True, parents=True)
    t = Team.objects.get(pk=team)
    template = 'team.md'
    md = render_to_string(template, {'team': t, 'milestone': milestone})
    if not path.exists():
        path.write_text(md)


def write_page(path, team=None, milestone=None, overwrite=False):
    path.parent.mkdir(exist_ok=True, parents=True)
    if path.name == 'TeamProject.md':
        template = 'team.md'
    elif milestone == '1':
        if path.name == 'Milestone.md':
            template = 'milestone1.md'
        elif path.name == 'Feedback.md':
            template = 'feedback1.md'
        else:
            return
    elif milestone == '2':
        if path.name == 'Milestone.md':
            template = 'milestone2.md'
        elif path.name == 'Feedback.md':
            template = 'feedback2.md'
        else:
            return
    elif milestone == '3':
        if path.name == 'Milestone.md':
            template = 'milestone3.md'
        elif path.name == 'Feedback.md':
            template = 'feedback3.md'
        else:
            return

    elif milestone == '4':
        if path.name == 'Milestone.md':
            template = 'milestone4.md'
        elif path.name == 'Feedback.md':
            template = 'feedback4.md'
        else:
            return

    elif milestone == '5':
        if path.name == 'Milestone.md':
            template = 'milestone5.md'
        elif path.name == 'Feedback.md':
            template = 'feedback5.md'
        else:
            return

    elif milestone == '6':
        if path.name == 'Milestone.md':
            template = 'milestone6.md'
        elif path.name == 'Feedback.md':
            template = 'feedback6.md'
        else:
            return

    elif milestone == '7':
        if path.name == 'Milestone.md':
            template = 'milestone7.md'
        # elif path.name == 'Feedback.md':
        #     template = 'feedback6.md'
        else:
            return

    md = render_to_string(template, {'team': team, 'milestone': milestone})
    write_file(path, md, overwrite=overwrite)
