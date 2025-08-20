# Review

## Bugs

- Sometimes no ingredients can be selected.
- Invalid path error due to usage of upper case leters in filenames.

## Documentation

- For github projects use markdown on doc files, especially the readme, to
improve readability and integration with the platform.

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
