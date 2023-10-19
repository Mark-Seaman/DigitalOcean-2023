from django.core.management import call_command
from io import StringIO
from json import loads
from os import system
from pathlib import Path
from shutil import copyfile


from .document import get_document
from .files import read_csv_file
from .models import Content, Pub
from .toc import content_file, write_content_csv


def create_pub(pub_name, pub_path, verbose=False):

    def update_record(name, doc_path):
        data = loads(pub_json_path(name, doc_path).read_text())
        pub, created = Pub.objects.get_or_create(name=name)
        pub.doc_path = doc_path
        for field in Pub._meta.get_fields():
            field_name = field.name
            if field_name in data and field_name != 'id':
                setattr(pub, field_name, data[field_name])
        if data.get('site_title') and pub.title != data.get('site_title'):
            pub.title = data.get('site_title')
        if data.get('site_subtitle') and pub.subtitle != data.get('site_subtitle'):
            pub.subtitle = data.get('site_subtitle')
        pub.save()
        return pub

    def import_pub(pub):
        content = content_file(pub)
        if pub.auto_contents:
            write_content_csv(pub)
        import_content(pub, content)
        delete_extra_objects(pub)

    def set_content(pub, doctype, path, folder, order):
        path = Path(pub.doc_path) / path
        x = Content.objects.get_or_create(
            blog=pub, doctype=doctype, order=order, path=path
        )[0]
        doc = get_document(path)
        x.folder = folder
        x.title = doc["title"]
        x.words = doc["words"]
        x.retain_object = True
        x.save()

    def import_content(pub, index):
        content = read_csv_file(index)
        try:
            for row in content:
                if row[2:]:
                    set_content(pub, "chapter", row[0], row[1], row[2])
                    # print('import:', row[0])
                elif row:
                    set_content(pub, "folder", row[0], 0, row[1])
            contents = len(Content.objects.filter(blog=pub))
        except:
            print(f"***Error while reading CSV ***  -- {index}")
        if verbose:
            print(f'Import Contents objects: {pub.name} {contents}')
        assert contents > 0

    def delete_extra_objects(pub):
        x = Content.objects.filter(blog=pub, retain_object=False).delete()
        if verbose:
            print(f"Deleting old content nodes: {x[0]}\n")
        for c in Content.objects.filter(blog=pub):
            c.retain_object = False
            c.save()

    if verbose:
        print(f"\nCreating Pub: name={pub_name}, path={pub_path}")
    pub = update_record(pub_name, pub_path)
    import_pub(pub)
    copy_static_files(pub, verbose)
    return pub


def copy_static_files(pub, verbose=False):
    doc_path = Path(pub.doc_path)
    if doc_path.name != 'Pub':
        if verbose:
            print(f"Old Pub: {pub}")
        return
    source = doc_path.parent/'Images'
    if source.exists() and pub.image_path:
        dest = Path(pub.image_path[1:])
        dest.mkdir(exist_ok=True, parents=True)
        for f in source.iterdir():
            if verbose:
                print(f"COPY FILES {pub.name} {f} {dest/f.name}")
            if not (dest/f.name).exists():
                copyfile(f, dest/f.name)


def pub_json_path(name, doc_path):
    path = Path(doc_path)
    path.mkdir(exist_ok=True, parents=True)
    json1 = Path(f'static/js/{name}.json')
    json2 = path/'pub.json'
    json3 = path.parent/'pub.json'
    if json2.exists():
        if path.name == 'Pub':
            json2.rename(json3)
            return json3
        return json2
    if json3.exists():
        return json3
    if json1.exists():
        # print("COPY FILE", json1, json2)
        copyfile(json1, json2)
        return json1
    return json2


def load_data():
    Pub.objects.all().delete()
    system("python manage.py loaddata config/publish.json")
    Content.objects.filter(words=0).delete()
    pubs = len(Pub.objects.all())
    print(f"Loaded {pubs} Pubs")
    content = len(Content.objects.all())
    print(f"Loaded {content} Content Posts")


def rename_file(f1, f2):
    if not Path(f1).exists():
        print("No PATH", f1)
    else:
        assert Path(f1).exists()
        Path(f1).rename(Path(f2))
        print(f"rename {f1} {f2}")
    assert Path(f2).exists()


def refresh_pub_from_git():
    system('cd Documents/Shrinking-World-Pubs && git pull')


def save_pub_data():
    command = '''
        {
            python manage.py dumpdata --indent 4 publish > config/publish.json &&
            git add config/publish.json &&
            git commit -m "Save pub JSON" &&
            git push
        } 2>/dev/null  > /dev/null 
    '''
    system(command)


def get_pub_contents(pub):
    def doc_objects(pub, folder):
        return (
            Content.objects.filter(blog=pub, doctype="chapter", folder=folder)
            .order_by("order")
            .values()
        )

    def docs_in_folder(pub, folder):
        return [d for d in doc_objects(pub, folder)]

    def folder_objects(pub):
        return (
            Content.objects.filter(blog=pub, doctype="folder")
            .order_by("order")
            .values()
        )

    folders = []
    for folder in folder_objects(pub):
        docs = docs_in_folder(pub, folder.get("order"))
        folder.update(dict(documents=docs))
        folders.append(folder)
    return folders


# def save_json_data(file, app=None):
#     output = StringIO()
#     if app:
#         call_command('dumpdata', app, stdout=output, indent=4)
#     else:
#         call_command('dumpdata', stdout=output, indent=4)
#     text = output.getvalue()
#     output.close()
#     Path(file).write_text(text)
#     return text


# def load_json_data(file):
#     output = StringIO()
#     call_command('loaddata', file, stdout=output)
#     text = output.getvalue()
#     output.close()
#     return text
