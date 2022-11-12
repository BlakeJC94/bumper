import os
import tempfile
from pathlib import Path

import pytest


@pytest.fixture(autouse=True)
def _import_modules_for_doctest(doctest_namespace):
    doctest_namespace["Path"] = Path


def create_tmp_file(data):
    file = tempfile.mkstemp()[1] + ".py"
    with open(file, "w", encoding="utf-8") as fh:
        fh.write(data)

    return file


@pytest.fixture
def test_file_with_version(version):
    with open("tests/templates/with_version.py.template", "r", encoding="utf-8") as fh:
        data = fh.read()

    version_marker = "%VERSION%"
    if version_marker in data:
        data = data.replace(version_marker, f'"{version}"', 1)

    file = create_tmp_file(data)
    yield file
    os.remove(file)


@pytest.fixture
def test_file_without_version_symbol():
    with open("tests/templates/without_version_symbol.py.template", "r", encoding="utf-8") as fh:
        data = fh.read()

    file = create_tmp_file(data)
    yield file
    os.remove(file)


@pytest.fixture
def test_file_without_version_defined():
    with open("tests/templates/without_version_symbol.py.template", "r", encoding="utf-8") as fh:
        data = fh.read()
    file = create_tmp_file(data)
    yield file
    os.remove(file)
