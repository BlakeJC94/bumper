import tempfile
import os
import shutil
from unittest.mock import patch, mock_open

import pytest

from bumper.core import bump_file, get_version, line_has_version


@pytest.mark.parametrize("template", ["tests/templates/with_version.py.txt"])
@pytest.mark.parametrize(
    "version, mode, expected",
    [
        ("1.2.3", "patch", "1.2.4"),
        ("1.2.3", "minor", "1.3.0"),
        ("1.2.3", "major", "2.0.0"),
    ],
)
def test_bump_file_with_version(test_file, version, mode, expected, template):
    # create test file with content TODO put into fixture
    assert get_version(test_file) == version
    with open(test_file, "r", encoding="utf-8") as fh:
        data = fh.read()

    # run func without os.remove
    with patch("os.remove", return_value=None) as mock_os_remove:
        bump_file(test_file, mode)
        mock_os_remove.assert_called_once_with(test_file + ".bumper")

    # cleanup temp file after check
    os.remove(test_file + ".bumper")

    # check results
    assert get_version(test_file) == expected
    with open(test_file, "r", encoding="utf-8") as fh:
        for original_line, new_line in zip(data.split("\n"), fh.readlines()):
            if not line_has_version(original_line):
                assert original_line == new_line.replace("\n", "")
