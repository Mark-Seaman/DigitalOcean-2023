from pathlib import Path

from django.utils.timezone import localdate
from publish.files import read_file

from publish.text import text_join
from probe.probe import check_file_count, check_line_count
from workshop.file_search import probe_files, python_code_files, template_files


def test_app_spec():
    return read_file("config/app.yaml")


def test_python_files():
    return "test_python_files: Python Code " + check_file_count(
        python_code_files(), 110, 130
    )


def test_template_files():
    return "test_template_files: Templates " + check_file_count(
        template_files(), 120, 160
    )


def test_probe_files():
    return "test_probe_files: Probes " + check_file_count(probe_files(), 7, 9)


def test_date():
    return localdate().strftime("%Y-%m-%d")


def test_python_source():
    return text_join(python_code_files())


def test_templates_source():
    return text_join(template_files())


def test_probe_source():
    return text_join(probe_files())


def test_python_lines():
    text = ""
    for f in python_code_files():
        text += Path(f).read_text()
    return check_line_count("Python code", text, 7000, 9000)
