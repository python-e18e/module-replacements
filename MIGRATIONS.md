# Migrations requiring code changes

These recipes illustrate limited scopes. Run the project's own tests after rewriting every relevant call site.

## Requests → HTTPX

Requests remains maintained. Choose HTTPX when its client model, async support, or HTTP/2 support fits the project. Changing the dependency and imports alone is insufficient.

```python
# Before
import requests

with requests.Session() as session:
    response = session.get(url, timeout=10)
    response.raise_for_status()
    payload = response.json()

# After: explicitly choose redirect and timeout behavior.
import httpx

with httpx.Client(follow_redirects=True, timeout=10) as client:
    response = client.get(url)
    response.raise_for_status()
    payload = response.json()
```

Rewrite exception handlers, transport adapters, streaming, proxy configuration, and raw request bodies (`content=`). HTTPX URLs are objects; convert with `str()` where callers require strings. Async migrations use `AsyncClient` and `await` throughout the call chain. Timeout semantics need review even with the same numeric argument. [HTTPX compatibility guide](https://www.python-httpx.org/compatibility/), [async guide](https://www.python-httpx.org/async/).

## attrs → dataclasses or Pydantic

attrs remains maintained. Choose dataclasses for plain internal data models and Pydantic for models that should validate external input. Neither is an import-only swap.

For an attrs class with a converter:

```python
from attrs import define, field

@define
class Item:
    count: int = field(converter=int)
```

A dataclass needs an explicit replacement for the conversion:

```python
from dataclasses import dataclass

@dataclass
class Item:
    count: int

    def __post_init__(self):
        self.count = int(self.count)
```

That example only covers construction-time conversion. Audit assignment behavior, validators, factories, slots, hashing, inheritance, `attrs.evolve()`, serialization, and `__attrs_post_init__` hooks individually. [attrs comparison](https://www.attrs.org/en/stable/why.html), [dataclass documentation](https://docs.python.org/3/library/dataclasses.html).

Pydantic changes the input contract and error model:

```python
from pydantic import BaseModel, ConfigDict

class Item(BaseModel):
    model_config = ConfigDict(strict=True)
    count: int

item = Item.model_validate({"count": 1})
payload = item.model_dump()
```

This intentionally rejects a string count; attrs' `int` converter would accept some strings. Choose strictness, coercion, extra-field policy, assignment validation, and serialization deliberately. Pydantic dataclasses also validate input and require migration review. [Model semantics](https://docs.pydantic.dev/latest/concepts/models/), [Pydantic dataclasses](https://docs.pydantic.dev/latest/concepts/dataclasses/).

## JSON encoders → json or orjson

Native `json` can remove a dependency for ordinary JSON. orjson is an option for workloads that benefit from its supported types or measured performance, with a different API.

```python
import orjson

body_bytes = orjson.dumps({"count": 1})
body_text = body_bytes.decode("utf-8")  # Only if the caller requires text.
```

Rewrite file helpers and options. Preserve `Decimal` precision explicitly when leaving simplejson, and test large integers, non-string keys, custom hooks, and non-finite numbers. orjson serializes NaN/infinity as null; simplejson and other encoders have different policies. [orjson documentation](https://github.com/ijl/orjson), [simplejson documentation](https://simplejson.readthedocs.io/en/latest/).

## pytz → zoneinfo

Replace `localize()`/`normalize()` idioms and make ambiguous/nonexistent local time policy explicit. `fold` is not a direct translation of `is_dst`. Test DST boundaries and arithmetic, and retain the timezone database dependency where needed. [Maintainer migration guide](https://pytz-deprecation-shim.readthedocs.io/en/latest/migration.html), [native timezone data requirements](https://docs.python.org/3/library/zoneinfo.html#data-sources).

## Partial standard-library migrations

`python-dateutil` → `datetime`/`zoneinfo` only covers constrained ISO parsing and IANA zones. Define the accepted input grammar; free-form parsing, recurrence rules, and relative calendar arithmetic still need dateutil or an explicit implementation. [Parser contract](https://dateutil.readthedocs.io/en/stable/parser.html).

`more-itertools` → `itertools` only covers helpers with native counterparts. For example, `chunked()` returns lists while `batched()` returns tuples; callers may require `map(list, batched(values, size))`. Inventory every helper before removing the dependency. [more-itertools API](https://more-itertools.readthedocs.io/en/stable/api.html), [itertools API](https://docs.python.org/3/library/itertools.html).
