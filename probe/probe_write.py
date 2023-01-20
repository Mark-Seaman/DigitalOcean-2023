from pathlib import Path
from publish.files import read_file

from publish.write import plant, write_blog


def test_write_script():
    plant(['Prometa.ol', 'Documents/shrinking-world.com/prometa'])
    return read_file('Documents/shrinking-world.com/prometa/Index.md')


def test_write_render():
    return write_blog(['render', 'Documents/seamansguide.com/poem/FromTheEdge.md', '', '', 'blog']) +\
        write_blog(
            ['render', 'Documents/seamansguide.com/poem/x.md', '', 'x', 'x'])
