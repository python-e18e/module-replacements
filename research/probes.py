"""Reproduce compatibility limits; isolated dependencies are documented in RESEARCH.md."""

import asyncio
import dataclasses
import enum
import functools
import inspect
import tomllib
import uuid

import attrs
import cached_property
import httpx2
import pydantic
import strenum
import tomli
import uuid6


def probe():
    # TOML 1.1 allows multiline inline tables; Python 3.14 tomllib does not.
    document = "item = {\n count = 1,\n}\n"
    assert tomli.loads(document) == {"item": {"count": 1}}
    try:
        tomllib.loads(document)
    except tomllib.TOMLDecodeError:
        pass
    else:
        raise AssertionError("Recheck the native TOML version and catalog guidance")

    class PackageEnum(strenum.StrEnum):
        GET = enum.auto()

    class NativeEnum(enum.StrEnum):
        GET = enum.auto()

    assert PackageEnum.GET.value == "GET"
    assert NativeEnum.GET.value == "get"
    assert not inspect.signature(uuid6.uuid8).parameters
    assert {"a", "b", "c"} <= set(inspect.signature(uuid.uuid8).parameters)
    assert uuid.uuid8(0, 0, 0).int == (8 << 76) | (2 << 62)

    @attrs.define
    class AttrsItem:
        count: int = attrs.field(converter=int)

    @dataclasses.dataclass
    class NativeItem:
        count: int

    class ValidatedItem(pydantic.BaseModel):
        model_config = pydantic.ConfigDict(strict=True)
        count: int

    assert AttrsItem("1").count == 1
    assert NativeItem("1").count == "1"  # An annotation does not validate.
    try:
        ValidatedItem(count="1")
    except pydantic.ValidationError:
        pass
    else:
        raise AssertionError("Strict model unexpectedly accepted a string")

    def redirect(request):
        if request.url.path == "/start":
            return httpx2.Response(302, headers={"location": "/end"})
        return httpx2.Response(200)

    with httpx2.Client(transport=httpx2.MockTransport(redirect)) as client:
        assert client.get("https://example.test/start").status_code == 302
        assert client.get("https://example.test/start", follow_redirects=True).status_code == 200

    asyncio.run(probe_async_cache())
    print(
        "Confirmed six compatibility limits: TOML, StrEnum, UUID8, models, "
        "HTTP redirects, async cache."
    )


async def probe_async_cache():
    class PackageProperty:
        @cached_property.cached_property
        async def value(self):
            return 1

    class NativeProperty:
        @functools.cached_property
        async def value(self):
            return 1

    package = PackageProperty()
    assert await package.value == await package.value == 1
    native = NativeProperty()
    assert await native.value == 1
    try:
        await native.value
    except RuntimeError:
        pass
    else:
        raise AssertionError("Native property unexpectedly cached a reusable task")


if __name__ == "__main__":
    probe()
