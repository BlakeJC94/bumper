import re
from tempfile import NamedTemporaryFile
from shutil import copy
from os import remove

from bumper.core import bump, get_version_from_line
from bumper.globals import SEMVER_REGEX


DEST = "scrap.new.txt"
SEMVER_REGEX_COMPILED = re.compile(SEMVER_REGEX)


with (
    open("scrap.txt", encoding="utf-8") as fh,
    NamedTemporaryFile(mode="w", encoding="utf-8") as fh_tmp,
):
    fn_tmp = fh.name

    version_bumped = False
    for line in fh.readlines():
        if not version_bumped and (version := get_version_from_line(line)) is not None:
            new_version = bump(version, mode="patch")
            new_line = re.sub(SEMVER_REGEX_COMPILED, line, new_version)
            fh_tmp.write(new_line)
            # TODO test

        else:
            fh_tmp.write(line)

copy(fn_tmp, DEST)
remove(fn_tmp)


# import fileinput

# with fileinput.input(files='scrap.new.txt') as f:
#     for line in f:
#         process(line)
