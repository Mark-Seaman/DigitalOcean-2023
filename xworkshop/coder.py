from pathlib import Path
from os import system
from django.contrib.auth import get_user_model
from shutil import copyfile, copytree

# from hammer.text import match_pattern, text_join, transform_matches
from publish.files import read_file, recursive_dirs, recursive_files, write_file


def create_new_project(project_path, project_name):

    project_path = project_path / project_name
    if not project_path.exists():
        project_path.mkdir()
        print('Create ', project_path)

    project_config = project_path/'config'
    if not project_config.exists():
        system(f'cd {project_path} && django-admin startproject config .')
        print('Create ', project_config)

    prototypes = Path('workshop/prototype/project').glob('*')
    for p in prototypes:
        if not ('config' in str(p)):
            if p.is_dir() and not p.exists():
                copytree(p, project_path / p.name)
            if p.is_file():
                copyfile(p, project_path / p.name)

    prototypes = Path('workshop/prototype/project/config').glob('*')
    for p in prototypes:
        if p.is_file():
            copyfile(p, project_path / 'config' / p.name)


# def create_new_project(project_path, project_name, project_app):
#
#     if not project_path.exists():
#         project_path.mkdir()
#
#     project_path = project_path/project_name
#     project_config = project_path/'config'
#     project_static = project_path/'static'
#     project_templates = project_path/'templates'
#
#     if not project_path.exists():
#         project_path.mkdir()
#         print('Create ', project_path)
#
#     if not project_static.exists():
#         project_static.mkdir()
#         print('Create ', project_static)
#
#     if not project_templates.exists():
#         project_templates.mkdir()
#         print('Create ', project_templates)
#
#     if not project_config.exists():
#         system(f'cd {project_path} && django-admin startproject config .')
#         edit_settings_file(project_path, project_name, project_app)
#         print('Create ', project_config)
#
#     if not (project_path/project_app).exists():
#         system(f'cd {project_path} && python manage.py startapp {project_app}')
#         print('Create ', project_app)
#
#     create_ocean_setup(project_path, project_static, project_templates)


def create_ocean_setup(project_path, project_static, project_templates):

    static_index = '<h1>Placeholder file for static server at Digital Ocean</h1>'
    create_setup_file(project_static/'index.html', static_index)

    requirements = '''
        asgiref
        Django
        gunicorn
        psycopg2-binary
        pytz
        sqlparse
        whitenoise
        dj-database-url
    '''
    create_setup_file(project_path/'requirements.txt', requirements)

    runtime = 'python-3.10.4'
    create_setup_file(project_path/'runtime.txt', runtime)

    index = '''
        {% extends 'theme.html' %}
        
        {% block content %}
        
        <div class="container row">
        
            {% for note in object_list %}
        
            <div class="card bg-light text-dark col m-5 p-5">
        
                <a href="{{ note.pk }}">
                    {{ note.title }} by {{ note.author }}
                </a>
        
            </div>
        
            {% endfor %}
        
        </div>
        
        <a href="/admin/" class="text-light">Add New Note</a>
        
        {% endblock content %}
    '''

    create_setup_file(project_templates/'index.html', index)

    theme = '''
        <!DOCTYPE html>
        <html lang="en">
        
        <head>
            <meta charset="UTF-8">
            <meta http-equiv="X-UA-Compatible" content="IE=edge">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.1/dist/css/bootstrap.min.css" rel="stylesheet">
            <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.1/dist/js/bootstrap.bundle.min.js"></script>
            <title>Note Pad Demo App</title>
        </head>
        
        <body class=" bg-dark text-light">
        
            <header class="bg-success p-5 mb-5">
                <h1>Note Pad</h1>
                <h2>Simple application with data</h2>
            </header>
        
            {% block content %}
            <h2>No Block Defined</h2>
            {% endblock content %}
        
        </body>
        
        </html>
    '''
    create_setup_file(project_templates/'theme.html', theme)


def create_setup_file(path, text):
    if not path.exists():
        write_file(path, text)
        print('Create ', path)


def edit_settings_file(project_path, project_name, project_app):
    settings_path = project_path/'config'/'settings.py'
    text = read_file(settings_path)
    # text = findall('ALLOWED_HOSTS = \[\]',text)
    text = text.replace('ALLOWED_HOSTS = []', "ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '.ondigitalocean.app']")
    text = text.replace("STATIC_URL = 'static/'", "STATIC_URL = 'static/'\nSTATICFILES_DIRS = [BASE_DIR / 'static']")
    text = text.replace("'DIRS': \[\]",  "'DIRS': [BASE_DIR / 'templates']")
    text = text.replace('INSTALLED_APPS = ', f"INSTALLED_APPS =\n    '{project_app}',\n")
    # print(text)
    write_file(settings_path, text)


def create_test_user():
    args = dict(username='seaman', email='me@here.com', password='secret')
    user = get_user_model().objects.filter(username='seaman')
    if user:
        user = user[0]
    else:
        user = get_user_model().objects.create_user(**args)
    return user, args


def application_files(path='.'):
    def exclude(p):
        f = str(p)
        return (f.startswith('env') or
                f.startswith('.git') or
                f.startswith('Temp') or
                f.startswith('Github') or
                f.startswith('Documents') or
                f.startswith('.cache') or
                '.pyc' in f or
                '/migrations/' in f)

    return recursive_files('.', '', exclude)


def probe_files():
    return [f for f in python_code_files() if 'probe/probe_' in f]


def python_code_files(path='.'):

    def exclude(p):
        f = str(p)
        return (f.startswith('env') or
                f.startswith('.git') or
                f.startswith('Temp') or
                f.startswith('Github') or
                f.startswith('Documents') or
                f.startswith('.cache') or
                '/migrations/' in f)

    return recursive_files('.', '.py', exclude)


def template_files(path='.'):

    def exclude(p):
        f = str(p)
        return (f.startswith('env') or
                f.startswith('.git') or
                f.startswith('.Documents/') or
                f.startswith('Temp') or
                f.startswith('Github') or
                f.startswith('Documents') or
                f.startswith('.cache') or
                f.startswith('static/reveal.js/'))

    return recursive_files('.', '.html', exclude)


def code_directories(path='.'):
    return recursive_dirs('.')

# def code_search(word):
#     return file_text_search('code', [word])
#

# def doc_files():
#     files = recursive_files('Documents', ['/history/', 'info/Test', '.DS_Store', '.git'])
#     return [join('Documents', f) for f in files]
#
#
# def doc_search(word):
#     return file_text_search('doc', [word])
#
#
# def find_classes(text):
#     pattern = r'class (.*)\(.*\)'
#     return match_pattern(text, pattern).split('\n')
#
#
# def find_functions(text):
#     pattern = r'\ndef (.*)\(.*\)'
#     return findall(pattern, text)
#
#
# def find_signatures(text):
#     pattern = r'def(.*\(.*\)):'
#     return transform_matches(text, pattern, r'\1').split('\n')
#
#
# def html_files():
#     all_files = recursive_files('.', ['env/', '.git'])
#     return [f for f in all_files if f.endswith('.html')] + [f for f in all_files if f.endswith('.css')]

# exclude = ['env', '.venv']
# files = text_lines(shell_file_list('.', 'html', exclude))
# files += text_lines(shell_file_list('.', 'css', exclude))
# return files


# def html_search(words):
#     files = html_files()
#     return file_search(files, words)
#

# def list_functions():
#     functions = []
#     files = code_files()
#     for code in files:
#         text = open(code).read()
#         functions.append(code + ':')
#         functions.append('    ' + '\n    '.join(find_functions(text)))
#     return text_join(functions)
#
#
# def source_code():
#     return '\n'.join([open(code).read() for code in code_files()])


# def file_text_search(file_selector='all', words=[]):
#     if file_selector == 'code':
#         files = code_files()
#     elif file_selector == 'doc':
#         files = doc_files()
#     elif file_selector == 'html':
#         files = html_files()
#     else:
#         files = code_files() + html_files() + doc_files()
#     # print(selector + 'search:')
#     return file_search(files, words)
