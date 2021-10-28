"""Fake Data Builder DataFrame Tests."""
import json

import pytest

from lib.fake_data_builder import FakeDataBuilder
from lib.errors import InvalidMetadataJson

from tests.metadata_builder import MetaDataBuilder


def _validate_result(result):
    assert (
        result
        == "I am Kimberly Miller. I live in 2513 Joseph Ports Apt. 463\nJonestown, SD 66069. I am born in 1934-03-10. My email address is monicarivera@gmail.com and phone number is +1-975-277-0031. I work as a Exercise physiologist in Pope-Hill. My employee id is JYkn-85027169"  # noqa E501
    )


def _write_metadata_file(tmp, count: int = 1, drop: str = None):
    metadata = MetaDataBuilder.template_simple(count=count)

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
    _validate_result(bldr.build())


@deco(count=10)
def test_sanity_count_10(fp):
    """Sanity Test with count = 10.

    Args:
        tmp_path (Path): Temporary Path.
    """
    bldr = FakeDataBuilder(metadata_filename=fp.absolute())
    result = bldr.build()
    assert isinstance(result, list)
    assert len(result) == 10


@deco(count=-1)
def test_sanity_count_negative(fp):
    """Sanity Test with count = -1.

    Args:
        tmp_path (Path): Temporary Path.
    """
    bldr = FakeDataBuilder(metadata_filename=fp.absolute())
    result = bldr.build()
    assert result is None


@deco(drop="string")
def test_without_template_should_raise_except(fp):
    """Test without string template.

    Args:
        tmp_path (Path): Temporary Path.
    """
    with pytest.raises(InvalidMetadataJson):
        FakeDataBuilder(metadata_filename=fp.absolute())


@deco(drop="seed")
def test_without_seed(fp):
    """Test without random seed.

    Args:
        tmp_path (Path): Temporary Path.
    """
    bldr = FakeDataBuilder(metadata_filename=fp.absolute())
    assert bldr.metadata.get("seed") is None
    assert isinstance(bldr.build(), str)


@deco(drop="locale")
def test_without_locale_should_default_to_en_us(fp):
    """Test without locale. Builder will default it to en_US.

    Args:
        tmp_path (Path): Temporary Path.
    """
    bldr = FakeDataBuilder(metadata_filename=fp.absolute())
    assert bldr.metadata["locale"] == "en_US"
    result = bldr.build()
    assert isinstance(result, str)
