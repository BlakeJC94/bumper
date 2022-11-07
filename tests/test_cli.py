import pytest

from bumper.cli import parse_args


@pytest.mark.parametrize("args", ["-h", "--help"])
def test_cli_help(capsys, args):
    """Test that the help dialog is printed to stderr if given help flag."""
    with pytest.raises(SystemExit):
        parse_args(args.split())
    assert "usage:" in capsys.readouterr().out


@pytest.mark.parametrize(
    "args",
    [
        "foo bar",  # no options given
        "--major --minor foo bar",  # conflicting options
    ],
)
def test_cli_raise_bad_arg_config(args):
    with pytest.raises(ValueError):
        parse_args(args.split())

@pytest.mark.parametrize(
    "args",
    [
        "--badarg foo bar",
        "--badarg",
    ],
)
def test_cli_raise_invalid_arg(args):
    with pytest.raises(SystemExit):
        parse_args(args.split())
