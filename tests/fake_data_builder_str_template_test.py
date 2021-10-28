"""Fake Data Builder DataFrame Tests."""
import json

import pytest

from lib.fake_data_builder import FakeDataBuilder
from lib.errors import InvalidMetadataJson

from tests.metadata_builder import MetaDataBuilder


def _validate_result(result):
    return (
        result
        == "I am Kimberly Miller. I live in 2513 Joseph Ports Apt. 463\nJonestown, SD 66069. I am born in 1934-03-09. My email address is monicarivera@gmail.com and phone number is +1-975-277-0031. I work as a Exercise physiologist in Pope-Hill. My employee id is JYkn-85027169"  # noqa E501
    )


def test_sanity(tmp_path):
    """Sanity Test."""
    try:
        metadata = MetaDataBuilder.template_simple()
        p = tmp_path / "simple_str_template.json"
        p.write_text(json.dumps(metadata))

        bldr = FakeDataBuilder(metadata_filename=p.absolute())
        result = bldr.build()
        _validate_result(result)
    finally:
        p.unlink()


def test_sanity_count_10(tmp_path):
    """Sanity Test with count = 10.

    Args:
        tmp_path (Path): Temporary Path.
    """
    try:
        metadata = MetaDataBuilder.template_simple(count=10)
        p = tmp_path / "simple_str_template.json"
        p.write_text(json.dumps(metadata))

        bldr = FakeDataBuilder(metadata_filename=p.absolute())
        result = bldr.build()
        assert isinstance(result, list)
        assert len(result) == 10
    finally:
        p.unlink()


def test_sanity_count_negative(tmp_path):
    """Sanity Test with count = -1.

    Args:
        tmp_path (Path): Temporary Path.
    """
    try:
        metadata = MetaDataBuilder.template_simple(count=-1)
        p = tmp_path / "simple_str_template.json"
        p.write_text(json.dumps(metadata))

        bldr = FakeDataBuilder(metadata_filename=p.absolute())
        result = bldr.build()
        assert result is None
    finally:
        p.unlink()


def test_without_template_should_raise_except(tmp_path):
    """Test without string template.

    Args:
        tmp_path (Path): Temporary Path.
    """
    try:
        metadata = MetaDataBuilder.template_simple()
        metadata.pop("string")

        p = tmp_path / "simple_str_template.json"
        p.write_text(json.dumps(metadata))

        with pytest.raises(InvalidMetadataJson):
            FakeDataBuilder(metadata_filename=p.absolute())
    finally:
        p.unlink()


def test_without_seed(tmp_path):
    """Test without random seed.

    Args:
        tmp_path (Path): Temporary Path.
    """
    try:
        metadata = MetaDataBuilder.template_simple()
        metadata.pop("seed")
        assert metadata.get("seed") is None

        p = tmp_path / "simple_str_template.json"
        p.write_text(json.dumps(metadata))

        bldr = FakeDataBuilder(metadata_filename=p.absolute())
        assert bldr.metadata.get("seed") is None
        result = bldr.build()
        assert isinstance(result, str)
    finally:
        p.unlink()


def test_without_locale_should_default_to_en_us(tmp_path):
    """Test without locale. Builder will default it to en_US.

    Args:
        tmp_path (Path): Temporary Path.
    """
    try:
        metadata = MetaDataBuilder.template_simple()
        metadata.pop("locale")
        assert metadata.get("locale") is None

        p = tmp_path / "simple_str_template.json"
        p.write_text(json.dumps(metadata))

        bldr = FakeDataBuilder(metadata_filename=p.absolute())
        assert bldr.metadata["locale"] == "en_US"
        result = bldr.build()
        assert isinstance(result, str)
    finally:
        p.unlink()
