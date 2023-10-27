from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from writer.models import Author


def authors(**kwargs):
    return Author.objects.filter(**kwargs).order_by('name')


def get_user(username):
    return get_user_model().objects.filter(username=username).first()


def create_user(**kwargs):

    username = kwargs.get('username')
    assert username
    email = kwargs.get('email', f"{username}@shrinking-world.com")
    user = get_user(username)
    if user:
        return user
    user = get_user_model().objects.create_user(
        username=username,
        email=email,
        first_name=kwargs.get('first_name', 'First name'),
        last_name=kwargs.get('last_name', 'last name'),
        password=kwargs.get('password', 'password'),
    )
    return user


def create_author(**kwargs):
    create_user(**kwargs)
    user = get_user(kwargs.get('username'))
    assert user

    # Check for required kwargs
    assert kwargs.get('first_name')
    assert kwargs.get('last_name')
    assert kwargs.get('email')
    assert kwargs.get('username')
    assert kwargs.get('password')

    #     # Create user with kwargs
    #     user = User.objects.create_user(
    #         username=kwargs['username'],
    #         email=kwargs['email'],
    #         password=kwargs['password'],
    #         first_name=kwargs['first_name'],
    #         last_name=kwargs['last_name']
    #     )

    # Setup defaults for user

    # Use get_or_create instead of create_user
    #     user = User.objects.get_or_create(
    #         username=kwargs['username'],
    #         email=kwargs['email'],
    #         password=kwargs['password'],
    #         first_name=kwargs['first_name'],
    #         last_name=kwargs['last_name']
    #     )

    # create author with user and remaining kwargs
    author = Author.objects.create(user=user, **kwargs)

    return author
