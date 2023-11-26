
from .models import Note


def create_note(**kwargs):
    return Note.objects.create(**kwargs)


def set_note(**kwargs):
    note, created = Note.objects.get_or_create(
        title=kwargs.get('title'), defaults=kwargs)
    if not created:
        note.text = kwargs.get('text', note.text)
        note.author = kwargs.get('author', note.author)
        note.published = kwargs.get('published', note.published)
        note.save()
    return note


def get_note(title):
    return Note.objects.get(title=title)


def get_note_id(id):
    return Note.objects.get(id=id)


def notes(**kwargs):
    return Note.objects.filter(**kwargs).order_by('id')
