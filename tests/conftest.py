import os
import logging
import tempfile
from pathlib import Path

import pytest

logger = logging.getLogger(__file__)


@pytest.fixture(autouse=True)
def _import_modules_for_doctest(doctest_namespace):
    doctest_namespace["Path"] = Path


@pytest.fixture
def test_file(version, template):
    with open(template, "r", encoding="utf-8") as fh:
        data = fh.read()

    version_marker = "%VERSION%"
    if version_marker in data:
        data = data.replace(version_marker, f'"{version}"', 1)

    # setup fixture
    file = tempfile.mkstemp()[1] + ".py"
    with open(file, "w", encoding="utf-8") as fh:
        fh.write(data)

    yield file

    # teardown fixture
    os.remove(file)


FILE_CONTENTS_WITH_VERSION = """'''Mock file with version'''
from foo import bar, baz

__version__ = "1.2.3"

class Foo:
    bar = bar
    baz = baz

    def __init__(self)
        self.barbaz = [bar, baz]

if __name__ == "__main__":
    bar(Foo().barbaz)
"""


@pytest.fixture
def file_contents_with_version():
    return FILE_CONTENTS_WITH_VERSION


FILE_CONTENTS_WITHOUT_VERSION_SYMBOL = """'''Mock file without version'''
from foo import bar, baz

class Foo:
    bar = bar
    baz = baz

    def __init__(self)
        self.barbaz = [bar, baz]

if __name__ == "__main__":
    bar(Foo().barbaz)
"""


@pytest.fixture
def file_contents_without_version_symbol():
    return FILE_CONTENTS_WITHOUT_VERSION_SYMBOL


FILE_CONTENTS_WITHOUT_VERSION_DEFINED = """'''Mock file without version'''
from foo import bar, baz, __version__

class Foo:
    bar = bar
    baz = baz
    version = __version__

    def __init__(self)
        self.barbaz = [bar, baz]

if __name__ == "__main__":
    bar(Foo().barbaz)
"""


@pytest.fixture
def file_contents_without_version_defined():
    return FILE_CONTENTS_WITHOUT_VERSION_DEFINED
