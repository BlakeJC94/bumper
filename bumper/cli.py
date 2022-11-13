import logging
from argparse import ArgumentParser
from glob import glob
from importlib.metadata import metadata
from pathlib import Path
from typing import Optional, List, Dict

from .core import is_py_file_with_version

logger = logging.getLogger(__name__)

ARGS = [("M", "major"), ("m", "minor"), ("p", "patch")]


def _get_parser():
    """Construct an argparse parser."""
    prog = Path(__file__).parent.name
    parser = ArgumentParser(
        prog=prog, description=metadata(prog)["Summary"], add_help=True, epilog=""
    )

    for arg_short, arg_long in ARGS:
        parser.add_argument(
            "-" + arg_short,
            "--" + arg_long,
            nargs="*",
            metavar="FILES",
            help=f"Bump `__version__` in FILES by {arg_long} version.",
        )

    parser.add_argument(
        "-d",
        "--dryrun",
        action="store_true",
        help="Don't modify files and print resulting actions if given",
    )

    return parser


# TODO: (Downstream) bump version only if change is detected (something for the GH action?)
# TODO: Use a namespace rather than a dict?
def parse_args(args: Optional[List[str]] = None) -> Dict[str, Optional[List[str]]]:
    """Parser for CLI interface that converts command line args to a python dictionary.

    Args:
        args: List of args passed into the cli interface (uses `sys.argv` if left as None).

    Usage:
        >>> parse_args("-m setup.py".split())
        {'major': None, 'minor': ['setup.py'], 'patch': None, 'dryrun': False}
        >>> parse_args("--patch".split())
        {'major': None, 'minor': None, 'patch': ['setup.py'], 'dryrun': False}
        >>> parse_args("-m setup.py -M setup.py".split())
        {'major': ['setup.py'], 'minor': None, 'patch': None, 'dryrun': False}

    """
    parser = _get_parser()
    result = vars(parser.parse_args(args))

    # Filter args
    for _, var in ARGS:
        if result[var] is None:
            continue

        # Set default value (when arg is called without inputs)
        if len(result[var]) == 0:
            result[var] = ["setup.py"]

        # Check for globs that weren't processed
        processed_globs = []
        for file in result[var]:
            if "*" in file:
                processed_globs.extend(glob(file))
                result[var].remove(file)
        result[var].extend(processed_globs)

        # Filter to selected files with versions
        result[var] = [fp for fp in result[var] if is_py_file_with_version(fp)]

    # Major presides over minor
    if result["minor"] is not None and result["major"] is not None:
        result["minor"] = _filter_overlaps(result["minor"], result["major"])

    # Major and minor preside over patch
    if result["patch"] is not None:
        if result["major"] is not None:
            result["patch"] = _filter_overlaps(result["patch"], result["major"])
        if result["minor"] is not None:
            result["patch"] = _filter_overlaps(result["patch"], result["minor"])

    # If empty list after filters, replace with None
    for _, var in ARGS:
        if result[var] is None:
            continue
        if len(result[var]) == 0:
            result[var] = None
        else:
            result[var] = list(set(result[var]))

    # Print help and exit if all none
    if all(result[var] is None for _, var in ARGS):
        parser.parse_args(["-h"])

    return result


def _filter_overlaps(list_0: List[str], list_1: List[str]) -> List[str]:
    """Filters overlaps between lists

    Usage:
        >>> _filter_overlaps(['foo', 'bar'], ['bar', 'baz'])
        ['foo']
        >>> _filter_overlaps([], ['bar', 'baz'])
        []
        >>> _filter_overlaps(['foo', 'bar'], [])
        ['bar', 'foo']
        >>> _filter_overlaps([], [])
        []
    """
    out = [fp for fp in list_0 if fp not in list_1]
    return sorted(out) if len(out) > 0 else []
