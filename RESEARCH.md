# Replacement research

Research date: **2026-09-29**. Scope: 45 distribution-level suggestions, combining standard-library adoption, documented successors, and optional migrations that require application rewrites.

## Method and evidence

Reviewed maintainer documentation, source repositories, Python version notes, and PyPI release metadata. Package metadata establishes release and interpreter requirements; it does not establish API parity. Every manifest entry has primary evidence and additional references. The catalog is advisory and does not claim to have migrated arbitrary applications successfully.

Historical Python floors describe when a feature became available, not which Python versions a project should still support. For rolling backports, inspect the actual APIs used on the minimum supported interpreter. For package alternatives, the following release snapshots ground the manifest's floors; future releases may differ.

| Target release | Requires Python | Evidence |
| --- | --- | --- |
| redis 8.1.0 | ≥3.10 | [Release metadata](https://pypi.org/project/redis/8.1.0/) |
| platformdirs 4.12.2 | ≥3.10 | [Release metadata](https://pypi.org/project/platformdirs/4.12.2/) |
| fpdf2 2.8.9 | ≥3.10 | [Release metadata](https://pypi.org/project/fpdf2/2.8.9/) |
| thefuzz 0.22.1 | ≥3.8 | [Release metadata](https://pypi.org/project/thefuzz/0.22.1/) |
| PyCryptodome 3.23.0 | ≥3.7 on Python 3 | [Release metadata](https://pypi.org/project/pycryptodome/3.23.0/) |
| pypdf 6.19.0 | ≥3.9 | [Release metadata](https://pypi.org/project/pypdf/6.19.0/) |
| scikit-learn 1.9.1 | ≥3.11 | [Release metadata](https://pypi.org/project/scikit-learn/1.9.1/) |
| HTTPX 0.28.1 | ≥3.8 | [Release metadata](https://pypi.org/project/httpx/0.28.1/) |
| Pydantic 2.13.5 | ≥3.9 | [Release metadata](https://pypi.org/project/pydantic/2.13.5/) |
| orjson 3.12.0 | ≥3.10 | [Release metadata](https://pypi.org/project/orjson/3.12.0/) |

## Standard-library opportunities

The strongest dependency-only candidates are distributions installed under the same import names as native modules: argparse, asyncio, contextvars, dataclasses, enum34 (`enum`), futures (`concurrent.futures`), pathlib, statistics, and typing. They exist to support older interpreters; the `asyncio` distribution now explicitly contains no implementation. Each entry cites its maintainer's package description and native API documentation.

Import rewrites also remove backports.shutil-get-terminal-size, backports.zoneinfo, backports.functools-lru-cache, selectors34, subprocess32, and functools32 for the documented scope. Native decimal incorporates cdecimal on **CPython**. Platform behavior and interpreter bug fixes still need project tests.

### Floors that need care

| Package / native API | Relevant boundary | Primary evidence |
| --- | --- | --- |
| backports.datetime-fromisoformat | Version 1 matched 3.7; version 2 matches the expanded 3.11 parser. | [Maintainer description](https://pypi.org/project/backports.datetime-fromisoformat/) |
| backports.functools-lru-cache | Basic cache in 3.2; `typed=` in 3.3. | [Python API history](https://docs.python.org/3/library/functools.html#functools.lru_cache) |
| singledispatch | Function in 3.4; method in 3.8; union registration in 3.11. | [Python API history](https://docs.python.org/3/library/functools.html#functools.singledispatch) |
| mock | Module in 3.3; AsyncMock in 3.8; ThreadingMock in 3.13. | [Native mock API](https://docs.python.org/3/library/unittest.mock.html) |
| exceptiongroup | Built-in classes/except* in 3.11; backported suppress behavior from 3.12.1. | [Package scope](https://pypi.org/project/exceptiongroup/) |
| more-itertools | pairwise in 3.10; batched in 3.12; strict batched in 3.13. | [Python iterator API](https://docs.python.org/3/library/itertools.html) |
| uuid6 | Native UUID6/7 generators in 3.14; UUID8 semantics differ. | [Python UUID API](https://docs.python.org/3/library/uuid.html), [package](https://github.com/oittaa/uuid6-python) |

### Rolling backports remain useful

importlib-metadata, importlib-resources, zipp, mock, pathlib2, and singledispatch can expose features or fixes beyond an older interpreter. Their presence alone does not prove an unnecessary dependency. Maintainer tables illustrate why native module introduction is insufficient:

| Backport | Selected mappings to native Python |
| --- | --- |
| importlib-metadata | 1.4 → 3.8; 4.6 → 3.10; 4.13 → 3.11; 6.5 → 3.12; 7.0 → 3.13. |
| importlib-resources | 1.3 → 3.9; 5.0 → 3.10; 5.7 → 3.11; 5.12 → 3.12; 6.0 → 3.13; 7.1 → 3.15. |
| zipp | 1.0 → 3.8; 3.2 → 3.10; 3.5 → 3.11; 3.16 → 3.12; 3.18 → 3.13; 3.21 → 3.15. |

These are maintainer synchronization tables, not guarantees that every later version is equivalent. The 3.15 rows refer to the upcoming interpreter, not a stable baseline for this research. [importlib-metadata table](https://github.com/python/importlib_metadata), [importlib-resources table](https://github.com/python/importlib_resources), [zipp table](https://github.com/jaraco/zipp).

### Surprising differences

- **Tomli:** current 2.4+ parses TOML 1.1; Python 3.14's tomllib documents TOML 1.0. Compiled Tomli wheels may also justify retaining it after measurement. [Tomli scope](https://github.com/hukkin/tomli), [tomllib scope](https://docs.python.org/3/library/tomllib.html).
- **toml:** reading filename arguments or text streams is not the native binary-stream API, and writes/custom hooks are outside tomllib's scope. [Original API](https://github.com/uiri/toml).
- **cached-property:** synchronous caching is the native overlap; async, TTL, and threaded variants need other handling. [Package features](https://pypi.org/project/cached-property/).
- **StrEnum:** package `auto()` keeps capitalization; native StrEnum lowercases it. Preserve protocol and storage values explicitly. [Maintainer warning](https://pypi.org/project/StrEnum/).
- **zoneinfo:** code availability does not guarantee IANA timezone data. Windows applications often still need `tzdata`. [Native data requirements](https://docs.python.org/3/library/zoneinfo.html#data-sources).
- **ipaddress:** native parsing and classifications evolved; leading-zero rejection changed in 3.9.5. [API change notes](https://docs.python.org/3/library/ipaddress.html).

## Documented package successors

| Migration | Evidence and scope |
| --- | --- |
| sklearn → scikit-learn | Deprecated distribution alias; imports stay `sklearn`. [Maintainer notice](https://pypi.org/project/sklearn/). |
| PyPDF2 → pypdf | Projects merged; pypdf 3.1 continues PyPDF2 3.x. Older/current major versions still require API review. [Project history](https://pypdf.readthedocs.io/en/stable/meta/history.html). |
| fpdf → fpdf2 | Maintained successor using the same import namespace; rendering/output compatibility needs tests. [History](https://py-pdf.github.io/fpdf2/History.html). |
| appdirs → platformdirs | Maintained fork with AppDirs compatibility alias, plus path behavior fixes. [Changelog](https://platformdirs.readthedocs.io/en/latest/changelog.html). |
| aioredis → redis.asyncio | Merged into redis-py; the compatible starting scope is aioredis 2.x. [Redis maintainer guidance](https://redis.io/faq/doc/26366kjrif/what-is-the-difference-between-aioredis-v2-0-and-redis-py-asyncio). |
| fuzzywuzzy → thefuzz | Maintainer rename; current RapidFuzz implementation needs score/threshold checks. [Archive notice](https://github.com/seatgeek/fuzzywuzzy), [successor](https://github.com/seatgeek/thefuzz). |
| pycrypto → pycryptodome | Near-compatible Crypto namespace, with documented removed/changed APIs. [Compatibility list](https://pycryptodome.readthedocs.io/en/latest/src/vs_pycrypto.html). |

Avoid coinstalling fpdf/fpdf2 or pycrypto/pycryptodome because each pair shares an import namespace. An alternative namespace such as `Cryptodome` requires separate import rewrites; this catalog recommends the `pycryptodome` distribution's `Crypto` scope. [PyCryptodome installation](https://pycryptodome.readthedocs.io/en/latest/src/installation.html).

## Broader architectural migrations

Seven entries use `code-change`: requests, attrs, ujson, simplejson, pytz, python-dateutil, and more-itertools. They need application rewrites and explicit behavior checks. These do not imply that the original packages are unmaintained. See [MIGRATIONS.md](MIGRATIONS.md) for target selection, primary sources, and concrete examples.

## Not admitted as whole-distribution replacements

- **typing-extensions → typing:** assess each symbol against the minimum interpreter; this rolling backport continues to serve supported Python versions. [Maintainer guidance](https://typing-extensions.readthedocs.io/en/latest/).
- **async-lru → functools.lru_cache:** caching coroutine objects is not reusable async result caching. [async-lru semantics](https://github.com/aio-libs/async-lru).
- **setuptools → importlib:** migrating `pkg_resources` calls does not remove an application's setuptools build backend or every setuptools feature. [Native metadata scope](https://docs.python.org/3/library/importlib.metadata.html).
- **backports.tarfile → tarfile:** a native module alone is insufficient evidence that an older runtime has all fixes used from a current rolling backport. No version mapping verified in this pass. [Backport](https://github.com/jaraco/backports.tarfile).
- **unittest2 → unittest:** promising historical backport removal, but plugin/CLI and old assertion usage need a separately documented scope before admission. [Package scope](https://pypi.org/project/unittest2/).

## Reproducible checks

Run the catalog's stdlib-only validation:

```console
python validate.py
python -m unittest discover -s tests
```

Six targeted probes demonstrate actual mismatches: multiline TOML inline tables, StrEnum auto values, UUID8 signatures/layout, attrs conversion versus dataclass annotations and strict Pydantic validation, HTTPX redirect defaults, and reusable async property values. The probes use a mocked HTTP transport, not a network service. They are examples of compatibility limits, not project-wide migration tests.

```console
uv run --no-project --python 3.14 \
  --with tomli==2.4.1 --with StrEnum==0.4.15 \
  --with uuid6==2025.0.1 --with cached-property==2.0.1 \
  --with attrs==26.1.0 --with pydantic==2.13.5 --with httpx==0.28.1 \
  python research/probes.py
```

The probe dependencies are isolated research tools, not dependencies of this catalog or CLI. Keep the TOML probe on Python 3.14: a later interpreter may deliberately add parser support and invalidate that expected mismatch.
