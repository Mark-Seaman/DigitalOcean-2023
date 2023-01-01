from os.path import join
from random import choice, randint

from course.models import UrlGame


def generate_url_question():
    url_type = choice(['Relative', 'Absolute', 'Server'])
    d1 = random_domain()
    d2 = random_domain()

    path = random_path()
    page = join(d1, path, random_page())
    file_name = random_file()
    dir_name = random_path()

    if url_type == 'Absolute':
        url = join(d2, dir_name, file_name)
        correct = join(d2, dir_name, file_name)
    elif url_type == 'Server':
        url = join(d1, dir_name, file_name)
        correct = join('/', dir_name, file_name)
    else:
        url = join(d1, dir_name, file_name)
        dir_name = relative_path(path, dir_name)
        correct = join(dir_name, file_name)

    return dict(page=page, url=url, url_type=url_type, correct=correct, hint=get_hint(url_type))


def get_hint(url_type):
    hint = "URL Type is %s URL." % url_type
    if url_type == 'Absolute':
        hint += '  Always include the protocol and domain in the URL.'
    elif url_type == 'Relative':
        hint += '  Only list the path (directory path and filename).'
    else:
        hint += '  Always start with "/" to get to the root of the current domain in the URL.'
    return hint


def relative_path(p1, p2):
    if p1 == p2: return ''
    p1 = p1.split('/')
    p2 = p2.split('/')
    x1 = p1
    x2 = p2
    # print('before', p1, p2)
    if p1 == ['']:
        x1 = []

    for i,x in enumerate(p1):
        if p1[i:] and p2[i:] and p1[i] == p2[i]:
            x1 = p1[i+1:]
            x2 = p2[i+1:]
            # print('same', x1, x2)
        else:
            break

    p1 = '/'.join(['..' for d in x1])
    p2 = '/'.join([d for d in x2])
    # print('after', p1, p2)
    # print(p1+'/'+p2)
    return join(p1, p2)


def random_page():
    pages = [
        "lesson40.html",
        "image.html",
        "color.html",
        "lesson10.html",
        "pie.html",
    ]
    return choice(pages)


def random_file():
    files = [
        "cat.jpg",
        "dog.png",
        "abe.png",
        "Abe.png",
        "abe.PNG",
        "dog.gif",
        "index.html",
        "animals.html",
        "projects.html",
        "Lesson-1.html",
        "styles.css",
    ]
    return choice(files)


def random_domain():
    protocols = [
        'http:/',
        'https:/',
    ]

    domains = [
        'www.unco.edu',
        'shrinking-world.com',
        'unco-bacs.org',
        'google.com',
        'greeley-colorado.gov',
    ]

    return '/'.join([choice(protocols), choice(domains)])


def random_path():
    directories = [
        "css",
        "images",
        "assets",
        "bacs200",
        "pages",
        "project",
    ]
    return '/'.join([choice(directories) for d in range(randint(0, 2))])


def reset_questions_left():
    for game in UrlGame.objects.all():
        print(game.student.name, game.answered, game.left)
        game.left = 10
        game.save()


def url_feedback(answer, correct):
    if answer == correct:
        return 'smiley1.jpg'
    else:
        return 'sad1.jpg'


# def game_data(student):
#     game = UrlGame.objects.get_or_create(student=student)[0]
#     return dict(correct=game.correct,
#                 incorrect=game.answered - game.correct,
#                 answered=game.answered,
#                 left=game.left)
def check_answer(game):
    question = eval(game.question)
    question['iscorrect'] = (question['correct'] == game.answer)

    if question['iscorrect']:
        game.left = game.left - 1
        game.correct += 1
    else:
        game.left = 10
    game.answered = game.answered + 1
    game.question = question
    game.save()
