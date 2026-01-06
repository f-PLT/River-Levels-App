import re
from pathlib import Path

import nox

ARG_RE = re.compile(r"^-[-\w=]+$")  # e.g. "-k", "--maxfail=1", "tests/foo.py"

nox.options.reuse_existing_virtualenvs = True  # Reuse virtual environments
nox.options.sessions = ["precommit"]


def get_paths(session):
    monorepo_path = Path(session.bin).parent.parent.parent
    apps_folder = monorepo_path / "apps"
    api = apps_folder / "api/src"
    api_tests = apps_folder / "api/tests"
    worker = apps_folder / "worker/src"
    worker_tests = apps_folder / "worker/tests"
    packages_folder = monorepo_path / "packages"
    packages = [f"{str(p)}/src" for p in packages_folder.iterdir() if p.is_dir()]
    packages_tests = [f"{str(p)}/tests" for p in packages_folder.iterdir() if p.is_dir()]
    scripts = monorepo_path / "scripts"
    python_apps_packages = [api, worker] + packages
    tests = [api_tests, worker_tests] + packages_tests
    return {
        "all": [
            *python_apps_packages,
            *tests,
            scripts,
        ],
        "module": [
            *python_apps_packages,
            scripts,
        ],
        "root": [monorepo_path],
    }


#
# Sessions
#
@nox.session()
def docformatter(session):
    paths = get_paths(session)
    session.run(
        "docformatter",
        "--config",
        f"{paths['all'][0].parent}/pyproject.toml",
        *paths["all"],
        external=True,
    )


@nox.session()
def check(session):
    paths = get_paths(session)
    session.run("flynt", *paths["all"], external=True)
    session.run(
        "docformatter",
        "--config",
        f"{paths['all'][0].parent}/pyproject.toml",
        *paths["all"],
        external=True,
    )
    session.run("ruff", "check", *paths["all"], external=True)


@nox.session()
def fix(session):
    paths = get_paths(session)

    session.run("flynt", *paths["all"], external=True)
    session.run(
        "docformatter",
        "--in-place",
        "--config",
        f"{paths['all'][0].parent}/pyproject.toml",
        *paths["all"],
        external=True,
    )
    session.run("mdformat", *paths["root"], external=True)
    session.run("ruff", "check", "--fix", *paths["all"], external=True)
    session.run("ruff", "format", *paths["all"], external=True)


@nox.session()
def precommit(session):
    session.run("pre-commit", "run", "--all-files", external=True)


@nox.session()
def flynt(session):
    paths = get_paths(session)
    session.run("flynt", *paths["all"], external=True)


@nox.session()
def mdformat(session):
    paths = get_paths(session)
    session.run("mdformat", *paths["root"], external=True)


@nox.session(name="ruff-lint")
def ruff_lint(session):
    paths = get_paths(session)
    session.run("ruff", "check", *paths["all"], external=True)


@nox.session(name="ruff-fix")
def ruff_fix(session):
    paths = get_paths(session)
    session.run("ruff", "check", "--fix", *paths["all"], external=True)


@nox.session(name="ruff-format")
def ruff_format(session):
    paths = get_paths(session)
    session.run("ruff", "format", *paths["all"], external=True)


@nox.session()
def test(session):
    session.run("pytest", external=True)


@nox.session()
def test_custom(session):
    for a in session.posargs:
        if not ARG_RE.match(a):
            session.error(f"unsafe pytest argument detected: {a!r}")

    session.run(
        "python", "-m", "pytest", external=True, *session.posargs
    )  # Pass additional arguments directly to pytest


@nox.session()
def test_nb(session):
    session.run(
        "pytest",
        "--nbval",
        "tests/test_notebooks/",
        "--nbval-sanitize-with=tests/test_notebooks/sanitize_file.cfg",
        external=True,
    )
