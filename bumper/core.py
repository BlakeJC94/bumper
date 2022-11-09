import re
from pathlib import Path
from typing import Optional

from git import Repo

from .globals import ALLOWED_MODES, SEMVER_REGEX


def bump(version: str, mode: str) -> str:
    """Bumps a semver version.

    Args:
        version: string representing a semver version. Must have MAJOR.MINOR.PATCH format
        mode: Whether to bump 'major', 'minor', or 'patch'.

    Usage:
        >>> bump("1.2.3", "patch")
        '1.2.4'
        >>> bump("1.2.3", "minor")
        '1.3.0'
        >>> bump("1.2.3", "major")
        '2.0.0'
    """
    assert mode in ALLOWED_MODES, f"Invalid `mode` given, must be one of {ALLOWED_MODES}."
    assert re.match(
        SEMVER_REGEX, version
    ), "Invalid `version` given, must be a semver 'major.MINOR.PATCH' string."

    major, minor, patch = version.split(".")

    if mode == "major":
        major, minor, patch = str(int(major) + 1), "0", "0"
    if mode == "minor":
        minor, patch = str(int(minor) + 1), "0"
    if mode == "patch":
        patch = str(int(patch) + 1)

    return ".".join([major, minor, patch])


def get_version(file: str) -> Optional[str]:
    """Get the version string from a versioned python file.

    Usage:
        >>> get_version('setup.py')
        '0.0.0'
    """
    version = None
    with open(file, "r", encoding="utf-8") as fh:
        try:
            version_line = next(
                l for l in fh.readlines() if "__version__='" in l.replace(" ", "").replace('"', "'")
            )
            version = re.search(SEMVER_REGEX, version_line)[0]
        except StopIteration:
            pass

    return version


def is_py_file_with_version(fp: str) -> bool:
    """
    Usage:
        >>> is_py_file_with_version('setup.py')
        True
        >>> is_py_file_with_version('doesnt_exist.py')
        False
        >>> is_py_file_with_version('bumper/__init__.py')
        False
    """
    has_version = False
    if not Path(fp).exists() or not fp.endswith(".py"):
        return has_version

    if get_version(fp) is not None:
        has_version = True

    return has_version


# TODO remove this for now
def get_files_to_bump():
    repo = Repo()

    # Get the git diff between this branch and main
    commit_branch = repo.commit()
    commit_origin_main = repo.commit("HEAD~1")
    diff = commit_origin_main.diff(commit_branch, create_patch=True, unified=0)

    # Find changed files
    changed_files = set()
    for diff_item in diff:
        if not diff_item.a_path:
            continue
        changed_files.add(diff_item.a_path)

    # Determine if only configs have changed (so then don't select setup.py)
    files_to_bump = {f for f in VERSIONED_FILES if f in changed_files}
    if any(v not in VERSIONED_FILES for v in changed_files):
        files_to_bump.add("setup.py")

    return files_to_bump
