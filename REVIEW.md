# Review

## Bugs

- Sometimes no ingredients can be selected.
- Invalid path error due to usage of upper case leters in filenames.

## Documentation

- For github projects use markdown on doc files, especially the readme, to
improve readability and integration with the platform.

## Version Control

- Improve the collaboration with a git workflow, github workflow is suggested.
- Remove branches which are no longer used.
> Fix: delete unused remote branches.
> ```bash
> git push --delete <remote> <branch>
> ```

- Improve `.gitignore` to a standard.
> Fix: use github python gitignore
> [template](https://github.com/github/gitignore/blob/main/Python.gitignore).

- Untrack control files that shouldn't be tracked.
> Fix: untrack files.
> ```bash
> git rm --cached Hamburger_Fever_Scores.txt
> ```

- Names, commits and branches must be consistent:
    - avoid interchanging english and spanish.
    - Improve consistency on commit messages, some are too short, and some are
    too long, and some say nothing (like `f70de08 alright`).
      > Fix: use [conventional
      > commits](https://www.conventionalcommits.org/en/v1.0.0/).

- Consider using git tags and [semver](https://semver.org/https://semver.org/)
to maintain project versions.

## Python Coding Standards

- Missing dependency management, needed for replicability and clear
highlighting of dependencies.
> Fix: added `requirements.txt` with:
> ```bash
> virtualenv .pyvenv
> source .pyvenv/bin/activate
> pip install numpy pygame
> pip freeze >requirements.txt
> ```
> Some alternatives of the classic `venv + pip` are
> [uv](https://docs.astral.sh/uv/) or [poetry](https://python-poetry.org/).

- Missing formatting and static analysis.
> Fix: Added `format.sh`, which formats and lints with
> [ruff](https://docs.astral.sh/ruff/).
