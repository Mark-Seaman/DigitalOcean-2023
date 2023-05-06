from pathlib import Path

from .coder import create_new_project
from .models import DataFactory


def generate_clone_code(factory_id):

    factory = DataFactory.objects.get(pk=factory_id)

    class_name = factory.class_name
    object_name = factory.object_name
    module_name = factory.module_name

    old_class = 'ClassName'
    old_object = 'object_instance'
    old_module = 'coder/prototype'

    clone_code(old_object, object_name, old_class, class_name, old_module, module_name)


# def generate_image_code(project_path):
#     class_name = "Image"
#     object_name = "image"
#     module_name = 'workshop'
#     old_class = 'ClassName'
#     old_object = 'object_instance'
#     old_module = 'coder/prototype'
#     clone_code(old_object, object_name, old_class, class_name, old_module, module_name)
#
#
# def generate_blog_code(project_path):
#     class_name = 'Blog'
#     object_name = "blog"
#     module_name = str(project_path)
#     old_class = 'ClassName'
#     old_object = 'object_instance'
#     old_module = 'workshop/prototype'
#     clone_code(old_object, object_name, old_class, class_name, old_module, module_name)
#     print(project_path, old_object, object_name, old_class, class_name, old_module, module_name)
#

def generate_data_type(project_path, project_app, class_name, object_name):

    def create_templates_dir(templates):
        if not templates.exists():
            if not templates.parent.exists():
                templates.parent.mkdir()
            templates.mkdir()

    module_name = project_app
    templates = project_path/project_app/'templates'
    create_templates_dir(templates)
    clone_code(project_path, object_name, class_name, module_name)


def clone_code(project, object_name, class_name, module_name):

    def prototypes_list():
        prototypes = Path('workshop/prototype').rglob('*')
        prototypes = [p for p in prototypes if not ('project' in str(p))]
        prototypes = [p for p in prototypes if p.is_file()]
        return prototypes

    def create_file_protoype(f1):
        f1 = f'{f1}'
        f2 = f1.replace('object_instance', object_name)
        base = 'workshop/prototype'
        f2 = f2.replace(base, module_name)
        f2 = f'{project}/{f2}'
        convert_file(f1, f2, module_name, object_name, class_name)

    def convert_file(f1, f2, module2, object2, class2):
        print(f'   {f1}  -->  {f2}')

        object1 = 'object_instance'
        class1 = 'ClassName'
        module1 = 'workshop/prototype'

        text = open(f1).read()
        text = text.replace(object1, object2)
        text = text.replace(class1, class2)
        text = text.replace(module1, module2)
        open(f2, 'w').write(text)

    print(f'\n\nGenerating code \nClass: {class_name}, Object: {module_name}\n')

    for f1 in prototypes_list():
        create_file_protoype(f1)


def generate_blog_code():
    project_path = Path('/Users/seaman/Github/BACS350/week6')
    project_name = 'BlogBuilder'
    project_app = 'blog'
    create_new_project(project_path, project_name, project_app)
    generate_data_type(project_path/project_name, project_app, 'Article', "article")


def generate_markdowner_code():
    project_path = Path('/Users/seaman/Github/BACS350/week7')
    project_name = 'MarkDowner'
    project_app = 'doc'
    create_new_project(project_path, project_name)
    generate_data_type(project_path/project_name, project_app, 'Document', "doc")
