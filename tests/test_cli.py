import pytest

from bumper.cli import parse_args


@pytest.mark.parametrize("cli_args", ["-h", "--help", ""])
def test_cli_help(capsys, cli_args):
    """Test that the help dialog is printed to stderr if given help flag."""
    with pytest.raises(SystemExit):
        parse_args(cli_args.split())
    assert "usage:" in capsys.readouterr().out


@pytest.mark.parametrize(
    "cli_args",
    [
        "foo bar",  # no options given
        "--badarg foo bar",
        "--badarg",
    ],
)
def test_cli_raise_invalid_args(cli_args):
    with pytest.raises(SystemExit):
        parse_args(cli_args.split())


def test_cli_globs_parsed():
    """Make sure globs only pick up files in a __version__ symbol defined"""
    cli_args = "--patch *"
    result = parse_args(cli_args.split())
    assert result["major"] is None
    assert result["minor"] is None
    assert result["patch"] == ["setup.py"]


def test_cli_no_duplicates():
    """Make sure globs only pick up files in a __version__ symbol defined"""
    cli_args = "--patch setup.py setup.py"
    result = parse_args(cli_args.split())
    assert result["major"] is None
    assert result["minor"] is None
    assert result["patch"] == ["setup.py"]


@pytest.mark.parametrize(
    "cli_args, expected",
    [
        (
            "--patch setup.py --minor setup.py",
            [("major", None), ("minor", ["setup.py"]), ("patch", None)],
        ),
        (
            "--major setup.py --minor setup.py",
            [("major", ["setup.py"]), ("minor", None), ("patch", None)],
        ),
        (
            "--major setup.py --patch setup.py",
            [("major", ["setup.py"]), ("minor", None), ("patch", None)],
        ),
        (
            "--major setup.py --minor setup.py --patch setup.py",
            [("major", ["setup.py"]), ("minor", None), ("patch", None)],
        ),
    ],
)
def test_cli_overlapping_args(cli_args, expected):
    """Make sure globs only pick up files in a __version__ symbol defined"""
    result = parse_args(cli_args.split())
    expected = dict(expected)
    for key in expected:
        assert result[key] == expected[key]


@pytest.mark.parametrize(
    "cli_args",
    [
        "--patch setup.py",
        "--patch setup.py --dryrun",
    ],
)
def test_cli_dryrun(cli_args):
    result = parse_args(cli_args.split())
    assert result["major"] is None
    assert result["minor"] is None
    assert result["patch"] == ["setup.py"]
    assert result["dryrun"] == ("dryrun" in cli_args)
