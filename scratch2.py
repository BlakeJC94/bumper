import re
from tempfile import NamedTemporaryFile
from shutil import copy
from os import remove

from bumper.core import bump, get_version_from_line
from bumper.globals import SEMVER_REGEX


SRC = "scrap.txt"


fp_tmp = SRC + ".bumper"
with (
    open(fp_tmp, mode="w", encoding="utf-8") as fh_tmp,
    open(SRC, encoding="utf-8") as fh,
):
    version_bumped = False
    for i, line in enumerate(fh.readlines()):
        line_to_write = line
        if not version_bumped and (version := get_version_from_line(line)) is not None:
            new_version = bump(version, mode="patch")
            line_to_write = re.sub(SEMVER_REGEX, new_version, line)
            version_bumped = True
        fh_tmp.write(line)

copy(fp_tmp, SRC)


# import fileinput

# with fileinput.input(files='scrap.new.txt') as f:
#     for line in f:
#         process(line)
