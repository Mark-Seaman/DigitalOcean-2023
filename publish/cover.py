from pathlib import Path
from django.template.loader import render_to_string
from PIL import Image

from publish.files import read_file, read_json, write_json
# from workshop.imager import crop_image
from workshop.resize_image import crop_image, save_image


def write_cover(args):
    if args:
        path = Path(f'Documents/Shrinking-World-Pubs/{args[0]}/Images')
        js = path/'Cover.json'
        if js.exists():
            data = read_json(js)
            create_cover_image(path, **data)
            text = render_to_string('pub/cover_design.html', data)
            cover = path/'Cover.html'
            cover.write_text(text)
            print(data)
            print(cover)
        else:
            data = dict(title='TITLE', tagline="TAG",
                        author="AUTHOR", cover_image="xxx")
            write_json(js, data)


def create_cover_image(path, **kwargs):
    cover = path/'CoverImage.png'
    if not cover.exists():
        print(kwargs)
        artwork = kwargs.get('cover_image')
        if artwork:
            artwork = Path(path)/artwork
            if artwork.exists():
                image = Image.open(artwork)
                print(f'Image: {path} Size: {image.size[0]}x{image.size[1]}')
                print(f'Shape: 1000x{int(image.size[1]*1000/image.size[0])}')
                image = crop_image(image)
                image.save(cover)
        else:
            print(f'FILE NOT FOUND -- {artwork}')
