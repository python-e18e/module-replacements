# Python module replacements

A small, reviewable manifest of Python packages with standard-library or maintained alternatives. This is the second [python-e18e](https://github.com/python-e18e) repository in the rollout, following [ecosystem-issues](https://github.com/python-e18e/ecosystem-issues). It is intentionally independent of the [CLI](https://github.com/python-e18e/cli).

[`replacements.json`](replacements.json) is the source of truth. Each entry records the old distribution name, alternative, earliest supported Python version, migration caveat, and primary source. The CLI can inspect it with:

```console
python -m python_e18e scan /path/to/project --replacements /path/to/replacements.json
```

Validate a proposed entry with `python validate.py` and `python -m unittest discover -s tests`. A suggestion is a review prompt: verify imports, supported Python versions, platform behavior, and test results before removing a dependency.

See [CONTRIBUTING.md](CONTRIBUTING.md) for evidence requirements.
