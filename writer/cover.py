
from django.template.loader import render_to_string
from PIL import Image

from publish.files import read_json

from .resize_image import crop_image, save_image


def create_book_cover(images):
    verbose = True
    images.mkdir(exist_ok=True)
    assert images.exists()

    # Downsample the thumbnails
    cover = images/'Cover.png'
    cover1600 = images/'Cover-1600.png'
    if cover.exists() and not cover1600.exists():
        create_cover_thumbnails(str(cover), verbose)
        assert cover1600.exists()
        return str(cover1600)

    # Create the artwork image
    image = images/'CoverImage.jpg'
    if not image.exists():
        return 'Save cover artwork as "CoverImage.jpg"'

    # Create the HTML cover - Render the cover with settings
    html = images/'Cover.html'
    js = read_json(images.parent/'pub.json')
    create_cover_image(images/'CoverImage.jpg')
    text = render_to_string('pub_script/cover_design.html', js)
    html.write_text(text)
    return 'Do a screen capture and save as "Cover.png"'


def create_cover_thumbnails(path, verbose):
    image = Image.open(path)
    if verbose:
        print('cover downsample:', path)
        print(f'Image: {path} Size: {image.size[0]}x{image.size[1]}')
        print(f'Shape: 1000x{image.size[1]*1000/image.size[0]}')
    image = crop_image(image, verbose)

    image = save_image(image, path, 1600, verbose)
    image = save_image(image, path, 800, verbose)
    image = save_image(image, path, 400, verbose)
    image = save_image(image, path, 200, verbose)


def create_cover_image(artwork, **kwargs):
    width = kwargs.get('width', 1000)
    height = kwargs.get('height', 1600)
    assert artwork.exists()
    image = Image.open(artwork)
    image = reshape_image(image, width, height)
    image.save(artwork)


def scale_image(path, width, height):
    image = Image.open(path)
    image = image.resize((width, height), Image.Resampling.LANCZOS)
    image.save(path)


def reshape_image(image, width, height, verbose=False):
    if verbose:
        print(f'Image Size: {image.size[0]}x{image.size[1]}')
        print(f'Image Shape: 1000x{int(image.size[1]*1000/image.size[0])}')
    if image.size[1]*width > image.size[0]*height:
        if verbose:
            print('Too Tall')
        size = image.size[0], int(image.size[0]*height/width)
    else:
        if verbose:
            print('Too Wide')
        size = int(image.size[1] * width / height), image.size[1]
    offset = 0, 0
    image = image.crop(
        (offset[0], offset[1], size[0]+offset[0], size[1]+offset[1]))
    if verbose:
        print(f'Crop Size: {size[0]}x{size[1]}',
              f'Shape: {width}x{int(size[1]*width/size[0])}')
        print(f'Crop Shape: {width}x{image.size[1]*width/image.size[0]}')
    return image
