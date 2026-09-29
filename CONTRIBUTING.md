# Contributing replacements

Add a distribution name only when there is a concrete alternative. Include all eight fields described in [README.md](README.md#manifest-fields), using normalized distribution names to avoid duplicates. An import name alone is not a distribution: `pkg_resources`, for example, is not grounds to replace every use of `setuptools`.

Use maintainer documentation, source, changelogs, Python documentation, and versioned PyPI metadata. Record the research date and exact successor release when setting a package's Python floor. Verify the floor against the APIs actually suggested, not just the version that introduced a module. Explain whether an older supported interpreter still needs a dependency marker.

Use `drop-in` only for a dependency-only change within the documented scope; `import-only` for import rewrites; `conditional` for a limited compatible subset; and `code-change` for broader application or tooling migrations. State which code, configuration, or workflow must change and what behavior must be tested. Maintained packages can be architectural alternatives without being obsolete. Do not present performance claims without a relevant benchmark.

For multiple targets, explain when to choose each. If only a subset of the old package is covered, say what must remain or be rewritten before dependency removal. Show a real usage example or a reproducible probe for surprising compatibility differences; do not infer whole-package parity from similar function names.

Run `python validate.py` and `python -m unittest discover -s tests`. Discuss uncertain replacements in [ecosystem-issues](https://github.com/python-e18e/ecosystem-issues) first.
