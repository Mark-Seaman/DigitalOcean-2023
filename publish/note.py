from django.contrib.auth.models import User
from course.user import make_user

from writer.author import create_user, get_user

from .models import Moderator, Note


def create_moderators(self=None):
    def create_moderator(**kwargs):
        # print(f"create_moderator: {kwargs}")
        user = create_user(**kwargs)
        m, _ = Moderator.objects.get_or_create(user=user)
        return m

    def check_moderator(**kwargs):
        user = User.objects.filter(email=kwargs.get('email')).first()
        m = Moderator.objects.get(user=user)
        assert user.first_name == kwargs.get('first_name')
        assert user.last_name == kwargs.get('last_name')
        assert user.email == kwargs.get('email')
        # assert user.password != "stacie"
        assert user.check_password("stacie")

    # def print users():
    #     for u in User.objects.all():
    #         if 'mark' in u.email:
    #             print([u.username, u.first_name, u.last_name, u.email])

    # Moderator.objects.all().delete()
    moderators = [
        dict(
            first_name="Mark", last_name="Seaman",
            email="mark@seamanfamily.org", password="stacie"
        ),
        dict(
            first_name="Elen", last_name="Hunt",
            email="hunt.elen@gmail.com", password="stacie"
        ),
        dict(
            first_name="Rachel", last_name="Garcia",
            email="rachel.seagarcia@gmail.com", password="stacie"
        )
    ]
    for moderator in moderators:
        create_moderator(**moderator)
        check_moderator(**moderator)


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
