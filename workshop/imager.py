from pathlib import Path
from traceback import format_exc

from PIL import Image

from publish.files import read_csv_file


def build_images():
    # image_path = Path('Documents/seamansguide.com/webapps/img/Section.jpg')
    # scale_image()

    # image_index()

    # shape_images()

    # image_path = Path('Documents/seamansguide.com/webapps/img')
    # max_width_images(image_path, 800)

    # limit_image_size()

    create_book_cover()


def create_book_cover():
    f1 = 'static/images/CoverArtwork/mark-cover.png'
    save_sizes(f1, [1600, 800, 400, 200])


def save_sizes(path, sizes):
    image = Image.open(path)
    for size in sizes:
        output_file = path.replace('.png', f'-{size}.png')
        image.thumbnail((size, size))
        image.save(output_file)


def limit_image_size():
    image_path = Path('static/images/shrinking-world.com/training/PythonWebApps.jpg')
    max_width_image(image_path, 200)
    max_width_image(image_path, 300)
    max_width_image(image_path, 400)

    image_path = Path('static/images/MarkSeaman/Mark-Seaman-Profile.jpg')
    max_width_image(image_path, 400)
    max_width_image(image_path, 200)

    image_path = Path('static/images/MarkSeaman/BusCard_.png')
    max_width_image(image_path, 978)


def build_logos():

    def crop(i):
        crop_rect = 200, 200, 800, 800
        return i.crop((crop_rect[0], crop_rect[1], crop_rect[2], crop_rect[3]))

    def scale(i, size):
        i.thumbnail((size, size))

    def save_size(i, size):
        output_file = Path(f'static/images/MarkSeaman/SWS-Logo-{size}.png')
        i.thumbnail((size, size))
        i.save(output_file)

    d = Path('static/images/MarkSeaman/sws-logo')
    for x in d.iterdir():
        # f = f'{d}/SWS-Logo-{str(x)[-6:]}'
        # x.rename(f)
        i = Image.open(x)
        scale(i, 1000)
        i = crop(i)
        f = d / f'SWS-Logo-600-{x.name[-6:]}'
        i.save(f)

    i = Image.open(Path('static/images/MarkSeaman/sws-logo/SWS-Logo-600-E5.png'))
    save_size(i, 600)
    save_size(i, 400)
    save_size(i, 200)
    save_size(i, 100)


def image_index():
    photo_path = Path('/Users/seaman/Desktop/Book_Photos')
    index_path = photo_path / 'images.csv'
    with open(index_path, 'w') as f:
        for i, path in enumerate(photo_path.glob('*.jp*g')):
            if i < 14:
                base = f'/Users/seaman/Hammer/Documents/images/shrinking-world.com/bacs350/chapter'
                f.write(f'{path.name},{base}-{i + 1}.jpg' + '\n')
            else:
                base = f'/Users/seaman/Hammer/Documents/images/shrinking-world.com/cs350/chapter'
                f.write(f'{path.name},{base}-{i - 13}.jpg' + '\n')
            if i > 19:
                break


def scale_image(image_path):
    print(f'Scale image {image_path}')
    im = Image.open(image_path)
    if im.size[0] > 200:
        im.thumbnail((200, 200))
        im.save(image_path)


def max_width_images(image_path, width):
    for path in image_path.iterdir():
        max_width_image(path, width)


def max_width_image(path, image_size):
    print(path)
    try:
        output_image = f'{path}.{image_size}{path.suffix}'
        print(output_image)
        im = Image.open(path)
        if im.size[0] > image_size:
            print(f'image size ({im.size[0]} x {im.size[1]})')
            print(f'image file ({output_image})')
            im.thumbnail((image_size, image_size))
        im.save(output_image)
    except IOError:
        print(format_exc())
        return "Cannot resize '%s'" % path


def shape_images():
    photo_path = Path('/Users/seaman/Desktop/Book_Photos')
    index_path = photo_path / 'images.csv'
    image_table = read_csv_file(index_path)
    for i in image_table:
        size = 600
        shape = (size, int(size / 1.6))
        reshape_image(photo_path / i[0], photo_path / i[1], shape)


def reshape_image(input_path, output_path, shape):
    if input_path != output_path:
        try:
            im = Image.open(input_path)
            im = crop_image(im, shape)
            im.thumbnail(shape)
            im.save(output_path)
        except IOError:
            print(format_exc())
            return "Cannot resize '%s'" % input_path
    return '%s --> %s (%s pixels)' % (input_path, output_path, shape)


def crop_image(image, shape):
    if image.size[1]*shape[0] > image.size[0]*shape[1]:
        print('Too Tall')
        size = image.size[0], int(image.size[0]*shape[1]/shape[0])
    else:
        print('Too Wide')
        size = int(image.size[1] * shape[0] / shape[1]), image.size[1]
    offset = 0, 0
    image = image.crop((offset[0], offset[1], size[0]+offset[0], size[1]+offset[1]))
    print(f'Crop Size: {size[0]}x{size[1]}', f'Shape: 1000x{int(size[1]*shape[0]/size[0])}')
    print(f'Crop Shape: 1000x{image.size[1]*shape[0]/image.size[0]}')
    return image
