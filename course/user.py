from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password


def make_user(**kwargs):
    name = kwargs.get('name')
    first, last = name.split(' ')[:2]
    username = kwargs.get('username', f'{first}{last}'.replace(' ', ''))
    email = kwargs.get('email', f'{username}@shrinking-world.com')
    password = 'UNC'
    kwargs = dict(username=username, first_name=first,
                  last_name=last, email=email)
    user, created = get_user_model().objects.get_or_create(
        username=username,
        defaults=kwargs)
    # if not created:
    user.username = username
    user.first_name = first
    user.last_name = last
    user.email = email
    user.set_password(password)
    user.save()
    return user


def users(**kwargs):
    return get_user_model().objects.all()
