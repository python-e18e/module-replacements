# Python module replacements

A researched catalog of Python packages with standard-library or maintained alternatives. This is the second [python-e18e](https://github.com/python-e18e) repository in the rollout, following [ecosystem-issues](https://github.com/python-e18e/ecosystem-issues). It is independent of the [CLI](https://github.com/python-e18e/cli).

[`replacements.json`](replacements.json) is the source of truth: **53 entries**, with HTTP guidance updated on **2026-09-30** (initial research: **2026-09-29**). Read the [research findings and evidence](RESEARCH.md) and [migration examples](MIGRATIONS.md). Inclusion does not mean a package is abandoned: some entries are optional architectural choices between maintained tools.

## Compatibility

| Value | Meaning |
| --- | --- |
| `drop-in` | Dependency declaration changes; existing application imports and ordinary API use stay the same. Interpreter upgrades still need testing. |
| `import-only` | Dependency and import changes cover the documented API scope. |
| `conditional` | Only specified APIs or behavior are covered. Audit usage; extra code changes may be needed. |
| `code-change` | Deliberate migration requiring application, configuration, or workflow rewrites and behavior checks. |

Examples: `sklearn` → `scikit-learn` is a distribution rename; `requests` → `httpx2` requires code changes; `attrs` → `dataclasses` or Pydantic requires choosing and implementing different model semantics. For tooling, `code-change` also covers configuration, editor, and CI workflow rewrites.

This catalog treats `httpx` as deprecated in favor of the Pydantic-maintained [HTTPX2](https://github.com/pydantic/httpx2). See the [HTTPX → HTTPX2 recipe](MIGRATIONS.md#httpx--httpx2) for compatibility checks.

[asyncio with uvloop](RESEARCH.md#asyncio-with-uvloop-optional-performance-information) is optional performance information, not a distribution migration.

## Modern project tooling

See [Astral tools and pyproject.toml](TOOLING.md) for pip/pip-tools → uv, Flake8/Black/isort → Ruff, mypy/Pyright → ty, and setup.cfg/setup.py → pyproject.toml. Distribution-level tooling alternatives are in the catalog. Configuration-file migrations are documented as workflows because filenames are not installable distributions.

## Manifest fields

| Field | Meaning |
| --- | --- |
| `name` | Installed **distribution** name, matched using normalized PyPI names. |
| `alternative` | Suggested distribution or standard-library API; `/` denotes choices or multiple APIs, not an install command. |
| `minimum_python` | Feature floor for the documented stdlib scope; for package successors, the Python floor of the explicitly researched release. For combined choices, a conservative floor covering both, with individual floors in guidance. This is not proof of full API parity. |
| `guidance` | Scope, limitations, required code changes, and checks before migration. |
| `source` | Primary evidence URL. |
| `kind` | `stdlib`, `package`, or `stdlib-or-package`. |
| `compatibility` | One of the classifications above. |
| `references` | Additional primary evidence and versioned release metadata. |

The original five string fields remain compatible with existing consumers. The validator accepts legacy entries without the three added fields; new contributions must include all eight. Sources and Python floors are researched snapshots, not dynamically refreshed metadata.

## Use

The CLI can inspect the catalog with:

```console
python -m python_e18e scan /path/to/project --replacements /path/to/replacements.json
```

Validate a proposed entry with `python validate.py` and `python -m unittest discover -s tests`. The validator and CI use only the standard library. Optional research probes have isolated, pinned dependencies; see [RESEARCH.md](RESEARCH.md#reproducible-checks).

A suggestion is a review prompt. The current CLI reports the guidance and Python floor; it does not enforce the new compatibility classifications or apply migrations. Verify every import, supported Python version, platform behavior, and test result before removing a dependency. Keep environment markers when older runtimes still need a backport.

See [CONTRIBUTING.md](CONTRIBUTING.md) for evidence requirements.
