import logging
import sys

from .cli import parse_args
from .core import bump_file


logger = logging.getLogger(__file__)
# bumper will automatically look at git diffs and determine where to bump


def main():
    result = parse_args()
    logger.info(f"Parsed input: {repr(result)}")

    for mode, files in result.items():
        if files is None:
            continue

        for file in files:
            logger.info(f"Bumping `__version__` in {file} by {mode} version.")
            bump_file(file, mode)

    return 0


if __name__ == "__main__":
    sys.exit(main())
