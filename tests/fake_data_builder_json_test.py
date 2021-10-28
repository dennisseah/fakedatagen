"""Fake Data Builder DataFrame Tests."""
import json

import pytest

from lib.fake_data_builder import FakeDataBuilder
from lib.errors import InvalidMetadataJson

from tests.metadata_builder import MetaDataBuilder


def _validate_result(result):
    assert (
        json.dumps(result)
        == """{"first_name": "Kimberly", "last_name": "Miller", "address": "2513 Joseph Ports Apt. 463\\nJonestown, SD 66069", "date_of_birth": "1934-03-10", "email_address": "monicarivera@gmail.com", "phones": [{"type": "cell", "number": "+1-975-277-0031"}, {"type": "home", "number": "001-364-850-2716x9823"}], "employer": {"company": "Garcia Inc", "job": "Engineer, maintenance (IT)"}}"""  # noqa E502
    )


def _write_metadata_file(tmp, count=1, drop: str = None):
    metadata = MetaDataBuilder.json_simple(count=count)

    if drop:
        assert metadata.get(drop) is not None
        metadata.pop(drop)
        assert metadata.get(drop) is None

    p = tmp / "simple_json.json"
    p.write_text(json.dumps(metadata))
    return p


def deco(count=1, drop=None):
    """Test decorator.

    Args:
        count (int, optional): count of generate items. Defaults to 1.
        drop ([type], optional): key of metadata to drop. Defaults to None.
    """

    def wrap(f):
        def wrapped_f(tmp_path):
            try:
                p = _write_metadata_file(tmp_path, count=count, drop=drop)
                f(p)
            finally:
                p.unlink()

        return wrapped_f

    return wrap


@deco()
def test_sanity(fp):
    """Sanity Test."""
    bldr = FakeDataBuilder(metadata_filename=fp.absolute())
    result = bldr.build()
    _validate_result(result)


@deco(count=10)
def test_sanity_where_count_eq_10(fp):
    """Sanity Test with count = 10."""
    bldr = FakeDataBuilder(metadata_filename=fp.absolute())
    result = bldr.build()
    assert len(result) == 10


@deco(drop="seed")
def test_sanity_where_seed_is_missing(fp):
    """Test where seed is missing in metadata."""
    bldr = FakeDataBuilder(metadata_filename=fp.absolute())
    assert bldr.build() is not None


@deco(drop="locale")
def test_sanity_where_locale_is_missing_should_default_to_en_us(fp):
    """Test where locale is missing in metadata."""
    bldr = FakeDataBuilder(metadata_filename=fp.absolute())
    assert bldr.metadata.get("locale") == "en_US"
    assert bldr.build() is not None


@deco(drop="count")
def test_sanity_where_count_is_missing_should_default_to_10(fp):
    """Test where count is missing in metadata."""
    bldr = FakeDataBuilder(metadata_filename=fp.absolute())
    assert len(bldr.build()) == 10


@deco(count=-1)
def test_sanity_where_count_is_negative_should_get_no_result(fp):
    """Test where count is negative in metadata."""
    bldr = FakeDataBuilder(metadata_filename=fp.absolute())
    assert bldr.build() is None


@deco(drop="schema")
def test_sanity_where_schema_is_missing_should_raise_except(fp):
    """Test where schema is missing in metadata."""
    with pytest.raises(InvalidMetadataJson):
        FakeDataBuilder(metadata_filename=fp.absolute())