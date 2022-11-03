# bumper
Version bumper for python projects across many files

**WIP** - will update README with details once things have started to come together. Assume
versions < 1.0.0 are unstable.

Main motivation for the project:
* Semver is cool
* I'm forgetful and don't remember to bump versions upon merging PRs
* My projects have a central version in `setup.py`
    * I also have many independent files within the project with a `__version__` variable I also
      (more often) forget to bump.

There are a couple of nice projects like `bumpver`, `python-semantic-version`, `tbump`, and various
`Poetry` plugins that have been tried and tested. But all of these tools use a central ground truth
variable in a configuration file, which means I can't bump independent files automatically. I also
don't want to tie a tool like this to `Poetry` since not every project uses that.

## Installation
Clone the repo to your system and install

```bash
$ git clone https://github.com/PLACEHOLDER
$ cd PLACEHOLDER
$ pip install .
```

## Quickstart
TODO

## Future developments
This also seems like a small project with a relatively small scope which seems like a good
opportunity to learn about Github actions and whatnot. This may become useful for someone someday -
who knows? I'll be making this tool for my personal projects for now, and (for now) I'm aiming to
create a cli app `bumper` that will
* Determines if files have changed between the current commit and the last commit
    * Bump the semver `__version__` string in `setup.py` if any changes have occured
    * Bump the semver `__version__` string in any watched files (most likely specified through
      `pyproject.toml`)
* The `__version__` in the last change is taken as the ground truth, so there should be minimal
  initialisation required besides installing this tool.
    * If `__version__` has been manually changed, `bumper` should skip bumping
* Major/minor/patch bump will be specified as command line flags
    * When running as a Github action, detect the major/minor/patch label on the PR and use that as
      the command line flag.

This tool will not
* Automatically make releases/tags on Github (though this may happen in the future)
* Support tagged semver versions, such as MAJOR.MINOR.PATCH-TAG
* Support other versioning systems, such as calendar-based systems. Just basic semver for now


*Question: How does this rectify, for example, a major bump for `setup.py` and a patch bump for a
watched file in the same PR?*
- Idea: extra tags?
    - not a perfect solution, will this mean a new 1-3 tags for each watched file??
    - Maybe just 3 extra tags: watched-major, watched-minor, watched-patch
        - Thought: If one watched file has a major bump and another one has a patch bump, maybe
          this isn't the right approach?
        - That's either the users fault, or maybe extra input could be parsed?
- Idea: Parse PR content?
    - A PR template could be useful here
- Idea: Bump it all with the same tag
    - This could be misleading
    - Might be a sensible default though if nothing else given?


## Contributing
This is a small personal project, but pull requests are most welcome!

* Code is styled using `[black](https://github.com/psf/black)` (`pip install black`)
* Code is linted with `pylint` (`pip install pylint`)
* Requirements are managed using `pip-tools` (run `pip install pip-tools` if needed)
    * Add dependencies by adding packages to `setup.py` and running
        `pip-compile --annotation-style=line`
    * Add dev dependencies to `setup.py` under `extras_require` and run
        `pip-compile --annotation-style=line --extra=dev --output-file=requirements-dev.txt setup.py`
* [Semantic versioning](https://semver.org) is used in this repo (shockingly)
    * Major version: rare, substantial changes that break backward compatibility
    * Minor version: most changes - new features, models or improvements
    * Patch version: small bug fixes and documentation-only changes

Virtual environment handling by `pyenv` is preferred:
```bash
# in the project directory
$ pyenv virtualenv 3.9.7 bumper
$ pyenv local bumper
$ pip install -e .
```
