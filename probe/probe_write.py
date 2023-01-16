from pathlib import Path
from publish.files import read_file

from publish.write import plant


def test_write_script():
    plant(['Prometa.ol', 'Documents/shrinking-world.com/prometa'])
    return read_file('Documents/shrinking-world.com/prometa/Index.md')
