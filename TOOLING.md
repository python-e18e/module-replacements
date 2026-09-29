# Astral tools and pyproject.toml

Researched **2026-09-29**. These migrations change commands, configuration, and development workflows. Existing tools can remain appropriate; inclusion does not imply they are obsolete.

| Existing workflow | Alternative | Work required |
| --- | --- | --- |
| pip / pip-tools | uv | Choose an environment workflow, preserve dependency intent, compare resolution, rewrite CI. |
| Flake8 | Ruff linter | Map rules/plugins and exclusions; compare diagnostics. |
| Black | Ruff formatter | Align settings and review formatting differences. |
| isort | Ruff I rules | Enable import sorting separately from formatting. |
| mypy / Pyright | ty | Translate rules, environments, suppressions, editor setup; compare checking results. |
| setup.cfg / setup.py metadata | pyproject.toml | Translate project/build metadata and verify built artifacts. |

## uv: environment and project management

For an existing requirements workflow, start with `uv venv`, `uv pip install -r requirements.txt`, or `uv pip compile` / `uv pip sync`. uv implements its own installer/resolver; review pip configuration, indexes, credentials, and environment selection against the [compatibility guide](https://docs.astral.sh/uv/pip/compatibility/).

For a project workflow, declare direct dependencies in pyproject.toml, commit uv.lock, and use `uv sync` and `uv run`. Import direct requirements with `uv add -r requirements.in`; use existing resolved pins as constraints when preserving versions. Separate development dependencies into groups. Review markers, extras, editable sources, and private indexes. [Migration guide](https://docs.astral.sh/uv/guides/migration/pip-to-project/).

After creating and reviewing the lockfile, CI can run:

```console
uv sync --locked
uv run --locked python -m unittest discover -s tests
```

`--locked` detects a stale lockfile instead of updating it. Pin the uv version in CI and compare the resolved environment before switching. [Locking and syncing](https://docs.astral.sh/uv/concepts/projects/sync/).

## Ruff: linting, formatting, and imports

Ruff includes implementations of many Flake8 plugin rules and isort checks; it does not execute arbitrary Flake8 plugins. Inventory existing rules and custom plugins, translate supported settings, and retain checks without equivalents. [Linter comparison](https://docs.astral.sh/ruff/faq/).

`ruff format` handles formatting, while `ruff check` handles lint rules, including import sorting when I rules are enabled. Review supported isort settings and documented Black differences. Apply fixes in a dedicated diff before replacing CI commands. [Configuration](https://docs.astral.sh/ruff/configuration/), [formatter scope](https://docs.astral.sh/ruff/formatter/).

```console
ruff check .
ruff format --check .
```

Neither command modifies files. Use `ruff check --select I --fix .` for reviewed import fixes, and `ruff format .` to apply formatting.

## ty: type checking

Run `ty check` alongside the current checker initially. Map settings to `[tool.ty]` or ty.toml, choose the source environment and target interpreter, and compare diagnostics. Translate checker-specific suppression comments to ty rule names. Strict modes and severity levels differ; review plugin-dependent checking and library support separately. [Migration guide](https://docs.astral.sh/ty/coming-from-mypy-or-pyright/), [configuration](https://docs.astral.sh/ty/configuration/).

Pin the evaluated ty release, record remaining diagnostic differences, and update editor integrations before replacing the old CI gate. The catalog records ty 0.0.84; no whole-project checking parity is assumed.

## pyproject.toml: shared metadata and configuration

pyproject.toml is a standardized project configuration file. `[build-system]` selects the build backend; `[project]` holds package metadata and runtime dependencies; `[project.optional-dependencies]` defines distributable extras. Development dependency groups and `[tool.*]` settings serve different purposes. Introducing the file does not require changing the build backend. [Packaging guide](https://packaging.python.org/en/latest/guides/writing-pyproject-toml/).

For setup.cfg/setup.py migrations, preserve package discovery, package data, entry points, extras, dynamic versions, and supported Python versions. Translate backend-specific settings under its tool table. Review built wheel/sdist contents, install the wheel in a clean environment, and compare metadata and tests before removing the old configuration. Keep executable build logic where it is still required. [Setuptools configuration](https://setuptools.pypa.io/en/latest/userguide/pyproject_config.html).

### Illustrative configuration

Adapt the metadata and dependency groups to the actual project. The example keeps setuptools as its backend and targets Python 3.11; tool installation floors do not determine the application's Python requirement.

```toml
[build-system]
requires = ["setuptools>=77"]
build-backend = "setuptools.build_meta"

[project]
name = "modern-example"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = []

[dependency-groups]
dev = ["ruff==0.16.9", "ty==0.0.84"]

[tool.ruff]
target-version = "py311"
line-length = 88

[tool.ruff.lint]
select = ["E4", "E7", "E9", "F", "I"]

[tool.ty.environment]
python-version = "3.11"
```

The Ruff rules are an example baseline, not a translation of every Flake8 configuration. Verify backend package layout and project-specific type-checker settings before adopting this example.

For GitHub repositories, update workflow commands, dependency-update configuration, and contributor instructions together. Existing python-e18e CLI checks identify setup.cfg, Flake8, requirements-file, and Pyright opportunities; this guide provides context for reviewing those suggestions.
