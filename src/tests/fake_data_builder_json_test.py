"""Fake Data Builder Json Tests."""
import json

import pytest

from fake_data_builder.configuration import DEFAULT_LOCALE, MetadataKey
from fake_data_builder.errors import InvalidMetadataJson
from fake_data_builder.fake_data_builder import FakeDataBuilder

from tests.metadata_builder import MetaDataBuilder
from tests.commons import write_metadata_file


def _validate_result(result):
    assert (
        json.dumps(result)
        == """{"first_name": "Kimberly", "last_name": "Miller", "address": "2513 Joseph Ports Apt. 463\\nJonestown, SD 66069", "email_address": "jacobleonard@gmail.com", "phones": [{"type": "cell", "number": "897-527-7003"}, {"type": "home", "number": "364-850-2716"}], "employer": {"company": "Tran, Jackson and Perez", "job": "Biochemist, clinical"}}"""  # noqa E502
    )


def deco(count=1, drop=None):
    """Test decorator.

    Args:
        count (int, optional): count of generate items. Defaults to 1.
        drop ([type], optional): key of metadata to drop. Defaults to None.
    """

    def wrap(f):
        def wrapped_f(tmp_path):
            try:
                _, p = write_metadata_file(
                    tmp_path, MetaDataBuilder.json_simple, count=count, drop=drop
                )
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
    assert bldr.metadata.get(MetadataKey.LOCALE.value) == DEFAULT_LOCALE
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
