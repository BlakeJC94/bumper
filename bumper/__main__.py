from .cli import parse_args

# bumper will automatically look at git diffs and determine where to bump


def main():
    result = parse_args()
    print(result)

    for index, files in result.items():
        if files is None:
            continue

        for file in files:
            print(f"Bumping `__version__` in {file} by {index} version.")
            version = get_version(file)
            # bump it
            # write version

    # replace each __version__
    return 0
