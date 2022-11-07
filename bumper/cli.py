import logging
from argparse import ArgumentParser, REMAINDER
from importlib.metadata import metadata
from pathlib import Path
from typing import Optional, List, Any, Dict

logger = logging.getLogger(__name__)


def parse_args(args: Optional[List[str]] = None) -> Dict[str, Any]:
    """Parser for CLI interface that converts command line args to a python dictionary.

    Args:
        args: List of args passed into the cli interface (uses `sys.argv` if left as None).

    Usage:
        >>> result = parse_args("--patch foo bar".split())
        >>> print(result)
        {'major': False, 'minor': False, 'patch': True, 'files': ['foo', 'bar']}

    """
    prog = Path(__file__).parent.name
    parser = ArgumentParser(
        prog=prog,
        description=metadata(prog)["Summary"],
        add_help=True,
    )

    for bump_long, bump_short in [("major", "M"), ("minor", "m"), ("patch", "p")]:
        parser.add_argument(
            "-" + bump_short,
            "--" + bump_long,
            action="store_true",
            help=f"Bump all `__version__` variables by {bump_long} version.",
        )

    parser.add_argument(
        "files",
        nargs=REMAINDER,
        type=str,
        default=None,
        help="Files to bump (automatically searches if no args given).",
    )

    result = vars(parser.parse_args(args))

    if sum(result[var] for var in ["major", "minor", "patch"]) != 1:
        raise ValueError("One of --major, --minor, --patch must be passed")

    invalid_options = [f for f in result['files'] if f.startswith('-')]
    if len(invalid_options) > 0:
        raise ValueError(f"Invalid options given: {invalid_options}")

    return result
