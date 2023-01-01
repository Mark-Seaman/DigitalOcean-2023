from pathlib import Path

from workshop.app_generator import clone_code, create_new_app, create_new_project, generate_data_type
from workshop.models import DataFactory


def generate_demo_apps():
    # generate_1_profile()
    # generate_3_pages()
    # generate_4_gallery()
    # generate_5_notes()
    # generate_6_blog_code()
    # generate_7_news_code()
    # generate_8_messenger()
    # generate_9_views()
    # generate_10_album()
    # generate_11_book()
    # generate_12_course()
    generate_13_code_builder()
    # generate_14_project_plan_code


def generate_1_profile():
    project_path = Path('/Users/seaman/Github/BACS350/01')
    project_name = 'ProfileApp'
    project_app = 'pages'
    project_path = create_new_project(project_path, project_name)
    create_new_app(project_path, project_app)


def generate_2_profile():
    pass


def generate_3_pages():
    project_path = Path('/Users/seaman/Github/BACS350/03')
    project_name = 'Pages'
    project_path = create_new_project(project_path, project_name)
    project_app = 'hero'
    create_new_app(project_path, project_app)


def generate_4_gallery():
    project_path = Path('/Users/seaman/Github/BACS350/04')
    project_name = 'Gallery'
    project_app = 'photos'
    project_path = create_new_project(project_path, project_name)
    create_new_app(project_path, project_app)


def generate_5_notes():
    project_path = Path('/Users/seaman/Github/BACS350/05')
    project_name = 'Notes'
    project_app = 'note'
    project_path = create_new_project(project_path, project_name)
    create_new_app(project_path, project_app)


def generate_6_blog_code():
    project_path = Path('/Users/seaman/Github/BACS350/06')
    project_name = 'Blog'
    project_app = 'blog'
    project_path = create_new_project(project_path, project_name)
    create_new_app(project_path, project_app)
    generate_data_type(project_path, project_app, 'Article', "article")
    generate_data_type(project_path, project_app, 'Blog', "blog")


def generate_7_news_code():
    project_path = Path('/Users/seaman/Github/BACS350/07')
    project_name = 'News'
    project_app = 'news'
    project_path = create_new_project(project_path, project_name)
    create_new_app(project_path, project_app)
    generate_data_type(project_path, project_app, 'Article', "article")
    generate_data_type(project_path, project_app, 'Author', "author")


def generate_8_messenger():
    project_path = Path('/Users/seaman/Github/BACS350/08')
    project_name = 'Messenger'
    project_app = 'messenger'
    project_path = create_new_project(project_path, project_name)
    create_new_app(project_path, project_app)
    generate_data_type(project_path, project_app, 'Person', "person")
    generate_data_type(project_path, project_app, 'Message', "message")


def generate_9_views():
    project_path = Path('/Users/seaman/Github/BACS350/09')
    project_name = 'ViewWorkshop'
    project_app = 'views'
    project_path = create_new_project(project_path, project_name)
    create_new_app(project_path, project_app)


def generate_10_album():
    project_path = Path('/Users/seaman/Github/BACS350/10')
    project_name = 'Album'
    project_app = 'photos'
    project_path = create_new_project(project_path, project_name)
    create_new_app(project_path, project_app)
    # generate_data_type(project_path, project_app, 'Author', "author")
    # generate_data_type(project_path, project_app, 'Album', "album")
    generate_data_type(project_path, project_app, 'Photo', "photo")


def generate_11_book():
    project_path = Path('/Users/seaman/Github/BACS350/11')
    project_name = 'BookBuilder'
    project_app = 'book'
    project_path = create_new_project(project_path, project_name)
    create_new_app(project_path, project_app)
    generate_data_type(project_path, project_app, 'Author', "author")
    generate_data_type(project_path, project_app, 'Book', "book")
    generate_data_type(project_path, project_app, 'Chapter', "chapter")


def generate_12_course():
    project_path = Path('/Users/seaman/Github/BACS350/12')
    project_name = 'CourseBuilder'
    project_app = 'course'
    project_path = create_new_project(project_path, project_name)
    create_new_app(project_path, project_app)
    generate_data_type(project_path, project_app, 'Chapter', "chapter")
    generate_data_type(project_path, project_app, 'Skill', "Skill")
    generate_data_type(project_path, project_app, 'Project', "project")
    generate_data_type(project_path, project_app, 'Demo', "demo")


def generate_13_code_builder():
    project_path = Path('/Users/seaman/Github/BACS350/13')
    project_name = 'CodeBuilder'
    project_app = 'coder'
    create_new_project(project_path, project_name)
    create_new_app(project_path/project_name, project_app)


def generate_14_project_plan_code():
    project_path = Path('/Users/seaman/Github/BACS350/13')
    project_name = 'ProjectPlan'
    project_app = 'swplan'
    create_new_project(project_path, project_name)
    generate_data_type(project_path / project_name, project_app, 'Project', "project")
    generate_data_type(project_path / project_name, project_app, 'Developer', "developer")
    generate_data_type(project_path / project_name, project_app, 'Milestone', "milestone")
    generate_data_type(project_path / project_name, project_app, 'Task', "task")


def generate_clone_code(factory_id):
    factory = DataFactory.objects.get(pk=factory_id)

    class_name = factory.class_name
    object_name = factory.object_name
    module_name = factory.module_name

    clone_code('workshop', object_name, class_name, module_name)


def generate_markdowner_code():
    project_path = Path('/Users/seaman/Github/BACS350/week7')
    project_name = 'MarkDowner'
    project_app = 'doc'
    create_new_project(project_path, project_name)
    generate_data_type(project_path / project_name, project_app, 'Document', "doc")
