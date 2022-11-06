import logging
from argparse import ArgumentParser
from importlib.metadata import metadata
from pathlib import Path
from typing import Optional, List, Any, Dict

logger = logging.getLogger(__name__)


def parse_args(args: Optional[List[Any]] = None) -> Dict[str, Any]:
    """Parser for CLI interface that converts command line args to a python dictionary.

    Args:
        args: List of args passed into the cli interface (uses `sys.argv` if left as None).

    Usage:
        >>> result = parse_args("file1 file2 file3 --patch".split())
        >>> print(result)

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
        nargs="?",
        type=str,
        default=None,
        help="Files to bump (automatically searches if no args given).",
    )

    try:
        return vars(parser.parse_args(args))
    except Exception as e:
        breakpoint()
