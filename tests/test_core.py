import tempfile
import os
import shutil
from unittest.mock import patch, mock_open

import pytest

from bumper.core import bump_file, get_version, line_has_version


@pytest.mark.parametrize(
    "version, mode, expected",
    [
        ("1.2.3", "patch", "1.2.4"),
        ("1.2.3", "minor", "1.3.0"),
        ("1.2.3", "major", "2.0.0"),
    ],
)
def test_bump_file_with_version(test_file_with_version, version, mode, expected):
    assert get_version(test_file_with_version) == version
    with open(test_file_with_version, "r", encoding="utf-8") as fh:
        data = fh.read()

    # run func without os.remove
    with patch("os.remove", return_value=None) as mock_os_remove:
        bump_file(test_file_with_version, mode)
        mock_os_remove.assert_called_once_with(test_file_with_version + ".bumper")

    # cleanup temp file after check
    os.remove(test_file_with_version + ".bumper")

    # check results
    assert get_version(test_file_with_version) == expected
    with open(test_file_with_version, "r", encoding="utf-8") as fh:
        for original_line, new_line in zip(data.split("\n"), fh.readlines()):
            if not line_has_version(original_line):
                assert original_line == new_line.replace("\n", "")


@pytest.mark.parametrize("mode", ["patch", "minor", "major"])
def test_bump_file_without_version(
    test_file_without_version_symbol,
    test_file_without_version_defined,
    mode,
):
    for test_file in [test_file_without_version_symbol, test_file_without_version_defined]:
        with patch("os.remove", return_value=None) as mock_os_remove:
            bump_file(test_file, mode)
            assert not os.path.exists(test_file + ".bumper")
            mock_os_remove.assert_not_called()
