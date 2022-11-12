from pathlib import Path

import pytest


@pytest.fixture(autouse=True)
def _import_modules_for_doctest(doctest_namespace):
    doctest_namespace["Path"] = Path


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
