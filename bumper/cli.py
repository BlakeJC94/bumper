import logging
import re
from argparse import ArgumentParser
from glob import glob
from importlib.metadata import metadata
from pathlib import Path
from typing import Optional, List, Dict

logger = logging.getLogger(__name__)

ARGS = [("M", "major"), ("m", "minor"), ("p", "patch")]


# TODO: I should check if `setup.py` has __version__...
# TODO: (Downstream) bump version only if change is detected (something for the GH action?)
def parse_args(args: Optional[List[str]] = None) -> Dict[str, Optional[List[str]]]:
    """Parser for CLI interface that converts command line args to a python dictionary.

    Args:
        args: List of args passed into the cli interface (uses `sys.argv` if left as None).

    Usage:
        >>> parse_args("-m foo.py bar.py -M bar.py baz.py wumbo.txt".split())
        {'major': ['bar.py', 'baz.py'], 'minor': ['foo.py'], 'patch': None}

    """
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

    result = vars(parser.parse_args(args))

    # Filter args
    for _, var in ARGS:
        if result[var] is None:
            continue

        # Set default value (when arg is called with out inputs)
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
        result[var] = [fp for fp in result[var] if _is_py_file_with_version(fp)]

    # Major presides over minor, which presides over patch
    result["minor"] = _filter_overlaps(result["minor"], result["major"])
    result["patch"] = _filter_overlaps(result["patch"], result["major"])
    result["patch"] = _filter_overlaps(result["patch"], result["minor"])

    # If empty list after filters, replace with None
    for _, var in ARGS:
        if result[var] is not None and len(result[var]) == 0:
            result[var] = None

    # Print help and exit if all none
    if all(result[var] is None for _, var in ARGS):
        parser.parse_args(["-h"])

    return result


def _is_py_file_with_version(fp: str) -> bool:
    """
    Usage:
        >>> _is_py_file_with_version('setup.py')
        True
        >>> _is_py_file_with_version('doesnt_exist.py')
        False
        >>> _is_py_file_with_version('bumper/__init__.py')
        False
    """
    has_version = False
    if not Path(fp).exists() or not fp.endswith(".py"):
        return has_version

    with open(fp, "r", encoding="utf-8") as fh:
        try:
            _ = next(l for l in fh.readlines() if "__version__=" in l.replace(" ", ""))
            has_version = True
        except StopIteration:
            pass

    return has_version


def _filter_overlaps(list_0: List[str], list_1: List[str]) -> Optional[List[str]]:
    """Filters overlaps between lists

    Usage:
        >>> _filter_overlaps(['foo', 'bar'], ['bar', 'baz'])
        ['foo']
        >>> _filter_overlaps([], ['bar', 'baz'])
        None
        >>> _filter_overlaps(['foo', 'bar'], [])
        ['foo', 'bar']
        >>> _filter_overlaps([], [])
        None
    """
    if list_0 is None or list_1 is None:
        return list_0
    out = [fp for fp in list_0 if fp not in list_1]
    return sorted(out) if len(out) > 0 else None
