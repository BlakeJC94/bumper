import tempfile
import os
import shutil
from unittest.mock import patch, mock_open

import pytest
from conftest import FILE_CONTENTS_WITH_VERSION

from bumper.core import bump_file, get_version, line_has_version


@pytest.fixture
def test_file(data):

    # setup fixture
    test_file = tempfile.mkstemp()[1] + ".py"
    with open(test_file, "w", encoding="utf-8") as fh:
        fh.write(data)

    yield test_file

    # teardown fixture
    os.remove(test_file)


@pytest.mark.parametrize("data", [FILE_CONTENTS_WITH_VERSION])
def test_bump_file_with_version(test_file, data):
    # create test file with content TODO put into fixture
    # test_file = resource(FILE_CONTENTS_WITH_VERSION)
    assert get_version(test_file) == "1.2.3"

    # run func without os.remove
    with patch("os.remove", return_value=None) as mock_os_remove:
        bump_file(test_file, "patch")
        mock_os_remove.assert_called_once_with(test_file + ".bumper")

    # cleanup temp file after check
    os.remove(test_file + ".bumper")

    # check results
    assert get_version(test_file) == "1.2.4"
    with open(test_file, "r", encoding="utf-8") as fh:
        for original_line, new_line in zip(data.split("\n"), fh.readlines()):
            if not line_has_version(original_line):
                assert original_line == new_line.replace("\n", "")
