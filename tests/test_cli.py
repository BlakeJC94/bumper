import pytest

from bumper.cli import parse_args


@pytest.mark.parametrize("args", ["-h", "--help", ""])
def test_cli_help(capsys, args):
    """Test that the help dialog is printed to stderr if given help flag."""
    with pytest.raises(SystemExit):
        parse_args(args.split())
    assert "usage:" in capsys.readouterr().out


@pytest.mark.parametrize(
    "args",
    [
        "foo bar",  # no options given
        "--badarg foo bar",
        "--badarg",
    ],
)
def test_cli_raise_invalid_args(args):
    with pytest.raises(SystemExit):
        parse_args(args.split())

@pytest.mark.parametrize(
    "args, expected",
    [
        (
            "--major foo.py bar.py --minor bar.py",
            {'major': ['foo.py', 'bar.py'], 'minor': None, 'patch': None}
        )
    ],
)
def test_cli_overlapping_inputs(args, expected):
    result = parse_args(args.split())
    assert result == expected
