import json
import tempfile
import unittest
from pathlib import Path

from validate import validate


class CatalogTests(unittest.TestCase):
    def test_manifest_and_duplicate_name(self):
        self.assertGreater(validate(), 0)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "replacements.json"
            entry = {
                "name": "old_name",
                "alternative": "new_name",
                "minimum_python": "3.11",
                "guidance": "Check API use.",
                "source": "https://docs.python.org/3/",
            }
            path.write_text(json.dumps([entry, {**entry, "name": "old-name"}]), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "duplicate"):
                validate(path)


if __name__ == "__main__":
    unittest.main()
