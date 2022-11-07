from .cli import parse_args
# bumper will automatically look at git diffs and determine where to bump

def main():
    result = parse_args()
    print(result)
    # If no files specified, determine which files have changed
    # exclude files that have had __version__ change (globs as well?)
    # Check overrides from args
    # replace each __version__
    return 0

    # IDEA: bumper --patch foo bar --minor baz --major wumbo mini
