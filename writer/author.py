from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from writer.models import Author


def authors(**kwargs):
    return Author.objects.filter(**kwargs).order_by('user__last_name', 'user__first_name')


def create_author(**kwargs):
    # Create user
    user = create_user(**kwargs)
    name = f"{user.first_name} {user.last_name}"

    # Object exists
    author = Author.objects.filter(user=user).first()
    if author:
        author.name = name
        author.save()
        return author

    # Create author
    author = Author.objects.create(user=user, name=name)
    return author


def create_user(**kwargs):
    # Name in kwargs
    first = kwargs.get('first_name')
    last = kwargs.get('last_name')
    username = f"{first}{last}".lower() if first and last else None
    username = kwargs.get('username', username)
    assert username

    # Email in kwargs
    email = f"{username}@shrinking-world.com"
    email = kwargs.get('email', email)
    assert email

    # Object exists
    user = get_user(username)
    if user:
        user.first_name = kwargs.get('first_name', user.first_name)
        user.last_name = kwargs.get('last_name', user.last_name)
        user.email = kwargs.get('email', user.email)
        password = kwargs.get('password', user.password)
        if password:
            user.set_password(password)
        user.save()
        return user

    # Create user
    user = get_user_model().objects.create_user(
        username=username,
        email=email,
        first_name=kwargs.get('first_name', 'First name'),
        last_name=kwargs.get('last_name', 'Last name'),
        password=kwargs.get('password', 'password'),
    )
    return user


def get_author(name):
    return Author.objects.filter(name=name).first()


def get_user(username):
    return get_user_model().objects.filter(username=username).first()
