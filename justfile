# Examples: msgspec

# Disable showing recipe lines before execution.
set quiet

# Enable unstable features.
set unstable

# Configure the shell for Windows.
set windows-shell := ["pwsh.exe", "-NoProfile", "-NonInteractive", "-ExecutionPolicy", "Bypass", "-Command"]

# We don't want to install any dev dependencies by default.
# export UV_NO_DEV := "true"

alias t := test
alias c := check
set dotenv-load

default_python := "3.13"
# TITLE := `uv version`
TITLE := `uv run --with setuptools_scm python -m setuptools_scm`
# VERSION := `uv version --short`
log := "warn"

export JUST_LOG := log

@_default:
    just --list

[group('dev')]
@version:
    uv run --with setuptools_scm python -m setuptools_scm 

# create venv, if not exists
[group('dev')]
@venv:
    [ -d .venv ] || uv venv --python {{ default_python }}

# build package
[group('dev')]
@build: venv
    uv build

# check distribution with twine
[group('dev')]
@check-dist: build
    uvx twine check dist/*

# clean reproducible files
[group('dev')]
@clean:
    #!/bin/bash
    dirs_to_clean=(
        ".benchmarks"
        ".cache"
        ".eggs"
        ".mypy_cache"
        ".pytest_cache"
        ".ruff_cache"
        ".venv"
        "__pycache__"
        "_build"
        "build"
        "dist"
        "htmlcov"
    )
    for d in "${dirs_to_clean[@]}"; do
        echo "Remove $d"
        find . -type d -name "$d" -exec rm -rf {} +
    done
    coverage erase
    #pyreverse files
    find . -type f -name "classes_numjuggler.*" -delete
    find . -type f -name "packages_numjuggler.*" -delete

# install package
[group('dev')]
@install: build
    uv sync   

# clean build
[group('dev')]
@reinstall: clean install

# Check style and test
[group('dev')]
@check: pre-commit test

# Check style includeing mypy and pylint and test
# [group: 'dev']
# @check-full: check mypy pylint pyright

# # Bump project version
# [group: 'dev']
# @bump *args="patch":
#   uv version --bump {{args}}
#   git commit -m "bump: version $(uv version)" pyproject.toml uv.lock

# update tools
[group('dev')]
@up-tools:
    pre-commit autoupdate
    uv self update
    pre-commit run -a 

# update dependencies
[group('dev')]
@up:
    uv sync --upgrade --all-extras
    pre-commit run -a 
    pytest

# show dependencies
[group('dev')]
@tree *args:
    uv tree --outdated {{ args }}

# run pyupgrade
[group('dev')]
@pyupgrade *args="--py314-plus":
    uvx pyupgrade {{ args }}  # presumably, code is updated by ruff, just to check occasionally

# test up to the first fail
[group('test')]
@test-ff *args:
    uv run --no-dev --group test pytest -x {{ args }}

# test with clean cache
[group('test')]
@test-cache-clear *args:
    uv run --no-dev --group test pytest --cache-clear {{ args }}

# test fast
[group('test')]
@test-fast *args:
    uv run --no-dev --group test pytest -m "not slow" {{ args }}

# run all the tests
[group('test')]
@test *args:
    uv run --no-dev --group test pytest {{ args }}

# run documentation tests
[group: 'test']
@xdoctest *args:
  uv run --no-dev --group test xdoctest --silent -c all src/numjuggler tools {{args}}

# create coverage data
[group('test')]
@coverage:
    uv run --no-dev --group test pytest --cov --cov-report=term-missing:skip-covered

# coverage to html
[group('test')]
@coverage-html:
    uv run --no-dev --group test pytest --cov --cov-report html:htmlcov 
    open htmlcov/index.html

# check correct typing at runtime
# [group: 'test']
# typeguard *args:
#   @uv run --no-dev --group test --group typeguard pytest --typeguard-packages=src {{args}}

# ruff check and format
[group('style')]
@ruff:
    ruff check --fix src tests
    ruff format src tests

# Run pre-commit on all files
[group('style')]
@pre-commit:
    uv run --no-dev --group style pre-commit run --show-diff-on-failure --color=always --all-files

# Run mypy
# [group: 'lint']
# @mypy:
#   uv run --no-dev --group mypy mypy src tests docs/source/conf.py

[group('style')]
@pylint:
    uv run --no-dev --group style pylint --recursive=y --output-format colorized src tests

# [group: 'lint']
# @pyright:
#   uv run --no-dev --group pyright pyright src tests

# Lint with ty
[group('style')]
@ty:
    uv run --no-dev --group style ty check 

# Draw UML diagrams
[group('style')]
@pyreverse:
    uv run --no-dev --group style pyreverse --project numjuggler --colorized --output puml --output-directory .pyreverse --ignore data --source-roots src/**/*.py

# Find code duplicates
[group('style')]
@symilar:
    uv run --no-dev --group style symilar src/**/*.py

# # Check rst-texts
# [group: 'docs']
# @rstcheck:
#   uv run --no-dev --group docs rstcheck --recursive *.rst docs
#
# build documentation
[group('docs')]
@docs-build *args:
    uv run --no-dev --group docs mkdocs build -d .docs-build --theme readthedocs {{ args }}

# browse and edit documentation with auto build
[group('docs')]
@docs:
    uv run --no-dev --group docs mkdocs  serve --dirty --watch docs --theme readthedocs
