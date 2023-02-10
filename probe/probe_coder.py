from pathlib import Path

from django.utils.timezone import localdate
from publish.files import join_files, read_file

from publish.text import text_join, text_lines
from probe.probe import check_file_count, check_line_count, show_files
from workshop.file_search import probe_files, python_code_files, source_code, template_files


def test_coder_app_spec():
    return read_file("config/app.yaml")


def test_coder_date():
    return localdate().strftime("%Y-%m-%d")


def test_coder_probe_source():
    return show_files("Probe Code ", probe_files, 360, 375)


def test_coder_python_source():
    return show_files("Python Code ", python_code_files, 9000, 9200)


def test_coder_templates():
    text = "test_template_files: Templates " + \
        check_file_count(template_files(), 120, 160)
    return text + text_join(template_files())
