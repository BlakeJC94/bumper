import logging
from argparse import ArgumentParser
from glob import glob
from importlib.metadata import metadata
from pathlib import Path
from typing import Optional, List, Dict

logger = logging.getLogger(__name__)

ARGS = [("M", "major"), ("m", "minor"), ("p", "patch")]


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

    if all(result[var] is None for _, var in ARGS):
        parser.parse_args(["-h"])

    # TODO update filter to get only files with __version__ strings
    all_py_files = _filter_py_files(['setup.py', *glob("**/*")])
    for _, var in ARGS:
        if result[var] is None:
            continue
        result[var] = _filter_py_files(result[var]) if len(result[var]) > 0 else all_py_files

    result["minor"] = _filter_overlaps(result["minor"], result["major"])
    result["patch"] = _filter_overlaps(result["patch"], result["major"])
    result["patch"] = _filter_overlaps(result["patch"], result["minor"])

    return result


def _filter_py_files(files: List[str]) -> List[str]:
    """Filters a list of filepaths to paths that end with .py

    Usage:
        >>> _filter_py_files(['foo.py', 'bar.pyc', 'baz.txt'])
        ['foo.py']
        >>> _filter_py_files([])
        []
        >>> _filter_py_files(None)
        []
    """
    if files is None:
        return []
    out = sorted([fp for fp in set(files) if fp.endswith(".py")])
    return out if len(out) > 0 else None

# def _get_version_str(file: str) -> Optional[str]:
#     with open(file, 'wb', encoding='utf-8') as f:
#         data = f.read().split('\n')
#     try:
#         version = next(line.strip() for line in data if line.strip().startswith('__version__'))
#     except StopIteration:
#         return None

#     return version.replace("'", '"').str


def _filter_overlaps(list_0: List[str], list_1: List[str]) -> Optional[List[str]]:
    """Filters overlaps between lists

    Usage:
        >>> _filter_overlaps(['foo', 'bar'], ['bar', 'baz'])
        ['foo']
    """
    if list_0 is None or list_1 is None:
        return list_0
    out = sorted([fp for fp in list_0 if fp not in list_1])
    return out if len(out) > 0 else None
