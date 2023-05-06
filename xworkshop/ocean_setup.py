from os import system

from publish.files import read_file, write_file


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


def create_new_demo_project(project_path, project_name, project_app):

    if not project_path.exists():
        project_path.mkdir()

    project_path = project_path/project_name
    project_config = project_path/'config'
    project_static = project_path/'static'
    project_templates = project_path/'templates'

    if not project_path.exists():
        project_path.mkdir()
        print('Create ', project_path)

    if not project_static.exists():
        project_static.mkdir()
        print('Create ', project_static)

    if not project_templates.exists():
        project_templates.mkdir()
        print('Create ', project_templates)

    if not project_config.exists():
        system(f'cd {project_path} && django-admin startproject config .')
        edit_settings_file(project_path, project_name, project_app)
        print('Create ', project_config)

    if not (project_path/project_app).exists():
        system(f'cd {project_path} && python manage.py startapp {project_app}')
        print('Create ', project_app)

    create_ocean_setup(project_path, project_static, project_templates)
