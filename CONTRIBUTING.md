# Contributing replacements

Add a direct dependency name only when there is a concrete alternative. Include `name`, `alternative`, `minimum_python`, `guidance`, and an authoritative `source` URL. Say what API or behavior differs; avoid a blanket drop-in claim. Show a real project that uses the old package and the check needed to migrate it.

Run `python validate.py` and `python -m unittest discover -s tests`. Discuss uncertain replacements in [ecosystem-issues](https://github.com/python-e18e/ecosystem-issues) first.
