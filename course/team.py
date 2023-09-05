from pathlib import Path
from django.template.loader import render_to_string

from publish.document import document_body, document_html

from .course import course_settings, read_document
from .models import Team


def create_page(team=None, milestone=None, role=None):
    # print(f'create page: {team} {milestone} {role}')
    if team:
        t = Team.objects.get(pk=team)
        print(f'create page: {team} {milestone} {role}')
        print(t.pk, t.name, t.github, t.server)
        path = Path(f'Documents/shrinking-world.com/cs350/team/{t.pk}')
        path.mkdir(exist_ok=True, parents=True)
        md = render_to_string('team.md', {'team': t})
        path = path/'TeamProject.md'
        if not path.exists():
            path.write_text(md)
        return path.read_text()


def team_view_data(user, **kwargs):
    kwargs = course_settings(**kwargs)
    course = kwargs["course_object"]
    team = kwargs.get('team')
    milestone = kwargs.get('milestone')
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
        text = create_page(team)
        markdown = document_body(text)
        html = document_html(markdown)
        kwargs.update(dict(title=course.title, html=html))
    return kwargs


def setup_team_pages():

    for t in Team.objects.all():
        create_page(t.pk)


def setup_teams():
    Team.objects.get_or_create(name='LinkedIn', pk=1)
    Team.objects.get_or_create(name='Amazon', pk=2)
    Team.objects.get_or_create(name='Instagram', pk=3)
    Team.objects.get_or_create(name='Trello', pk=4)
    Team.objects.get_or_create(name='Ghost Writer', pk=5)

    x = Team.objects.get(pk=1)
    x.github = ''
    x.server = ''
    x.save()

    x = Team.objects.get(pk=2)
    x.github = 'https://github.com/alexhovick/ShopZoneCS350'
    x.server = 'https://clever-cucurucho-a93faa.netlify.app'
    x.save()

    x = Team.objects.get(pk=3)
    x.github = ''
    x.server = ''
    x.save()

    x = Team.objects.get(pk=4)
    x.github = 'https://github.com/JLeFevre559/CS350-Clipboard'
    x.server = 'https://clipboard-unco-cs350.vercel.app/'
    x.save()

    x = Team.objects.get(pk=5)
    x.github = 'https://github.com/Mark-Seaman/GhostWriter'
    x.server = 'https://shrinking-world.com/sweng'
    x.save()

    for t in Team.objects.all():
        print(t.pk, t.name, t.github, t.server)
