from pathlib import Path
from shutil import copyfile

from publish.import_export import copy_static_files
from publish.publication import get_pub
from writer.outline import extract_links

from .pub_script import edit_files, pub_path, pub_url

def pub_publish(**kwargs):
    pub = kwargs.get('pub')
    chapter = kwargs.get('chapter')
    doc = kwargs.get('doc')
    publish_script([pub, chapter, doc])
    url = pub_url(pub, chapter, doc)
    return url

def publish_script(args):
    if not args:
        return 'usage: publish pub-name chapter doc'
    pub_name = args[0]
    source = pub_path('apps')
    dest = pub_path()/'apps'/'Pub'
    # print('SOURCE:', source, ', DEST:', dest)
    dest.mkdir(exist_ok=True)
    copyfile(source/'Index'/'_content.csv', dest/'_content.csv')
    copyfile(source/'Index'/'Index.md', dest/'Index.md')

    # print('publish apps')
    if args[2:]:
        pub = get_pub(pub_name)
        chapter = args[1]
        text = copy_image_file(pub)
        edit_files([copy_doc_files(pub, chapter)])
        return text
    return 'OK'


def copy_image_file(pub):
    text = f'\nCopy Image Files:\n'
    images = Path(pub.doc_path).parent/'Images'
    if images.exists():
        text += f'copy the "{pub.image_path}" directory from "{images}"\n'
        copy_static_files(pub, True)
    return text


def copy_doc_files(pub, chapter):
    source_dir = pub_path(pub.name, chapter)
    dest_dir = Path(pub.doc_path)
    with open(dest_dir/'_content.csv', "a") as file:
        index = source_dir/'Index.md'
        if index.exists():
            links = extract_links(source_dir/'Index.md')
            for link in links:
                copyfile(source_dir/link[0], dest_dir/link[0])
                file.write(f'{link[0]},99,1\n')
        else:
            x = f'{chapter}.md'
            if (source_dir/x).exists():
                copyfile(source_dir/x, dest_dir/x)
    return str(dest_dir)

 