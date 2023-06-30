from os import path
from pathlib import Path

from django.template.loader import render_to_string
from PIL import Image

from publish.files import read_file, read_json, write_json

from .resize_image import crop_image, save_image


def create_book_cover(images):
    verbose = False
    assert images.exists()
    cover = images/'Cover.png'
    if cover.exists():
        if verbose: 
            print('cover:', cover)
        create_cover_images(str(cover), verbose)
        cover1600 = images/'Cover-1600.png'
        assert cover1600.exists()
    return str(cover1600)


def create_cover_html(path, js):
    if path.exists():
        return
    data = read_json(js)
    create_cover_image(path, **data)
    text = render_to_string('pub/cover_design.html', data)
    cover = path/'Cover.html'
    cover.write_text(text)
    print(data)
    print(cover)


def create_cover_images(path, verbose):
    image = Image.open(path)
    if verbose:
        print(f'Image: {path} Size: {image.size[0]}x{image.size[1]}')
        print(f'Shape: 1000x{image.size[1]*1000/image.size[0]}')
    image = crop_image(image, verbose)

    image = save_image(image, path, 1600, verbose)
    image = save_image(image, path, 800, verbose)
    image = save_image(image, path, 400, verbose)
    image = save_image(image, path, 200, verbose)


def create_cover_image(path, **kwargs):
    width = kwargs.get('width', 1000)
    height = kwargs.get('height', 1600)
    cover = path/'CoverImage.png'
    if not cover.exists():
        print(kwargs)
        artwork = kwargs.get('cover_image')
        if artwork:
            artwork = Path(path)/artwork
            if artwork.exists():
                image = Image.open(artwork)
                image = reshape_image(image, width, height)
                image.save(cover)
        else:
            print(f'FILE NOT FOUND -- {artwork}')


def scale_image(path, width, height):
    image = Image.open(path)
    image = image.resize((width, height), Image.Resampling.LANCZOS)
    image.save(path)


def reshape_image(image, width, height):
    print(f'Image: {path} Size: {image.size[0]}x{image.size[1]}')
    print(f'Shape: 1000x{int(image.size[1]*1000/image.size[0])}')
    if image.size[1]*width > image.size[0]*height:
        print('Too Tall')
        size = image.size[0], int(image.size[0]*height/width)
    else:
        print('Too Wide')
        size = int(image.size[1] * width / height), image.size[1]
    offset = 0, 0
    image = image.crop(
        (offset[0], offset[1], size[0]+offset[0], size[1]+offset[1]))
    print(f'Crop Size: {size[0]}x{size[1]}',
          f'Shape: {width}x{int(size[1]*width/size[0])}')
    print(f'Crop Shape: {width}x{image.size[1]*width/image.size[0]}')
    return image


def write_cover(args):
    if args:
        path = Path(f'Documents/Shrinking-World-Pubs/{args[0]}/Images')
        js = path/'Cover.json'
        if js.exists():
            create_cover_html(path, js)
        else:
            data = dict(title='TITLE', tagline="TAG",
                        author="AUTHOR", cover_image="xxx")
            write_json(js, data)
        scale_image(path/'Intro.png', 800, 450)
        scale_image(path/'Overview.png', 800, 450)
        scale_image(path/'Teacher.png', 800, 450)

