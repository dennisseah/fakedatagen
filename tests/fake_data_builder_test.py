"""Fake Data Builder Tests."""
import json
import pytest

from lib.fake_data_builder import FakeDataBuilder
from lib.errors import InvalidMetadataJson, InvalidProviderType

from tests.metadata_builder import MetaDataBuilder


def test_invalid_metadata_file_should_throw_except():
    """Provide an invalid metadata file path.

    Invalid metadata file path to FakeDataBuilder constructor,
    and expecting FileNotFoundError exception.
    """
    with pytest.raises(FileNotFoundError):
        FakeDataBuilder(metadata_filename="invalid.json")


def test_invalid_metadata_json_should_throw_except(tmp_path):
    """Provide an invalid metadata json.

    Invalid metadata json to FakeDataBuilder constructor,
    and expecting InvalidMetadataJson exception.

    Args:
        tmp_path (Path): Temporary Path
    """
    p = tmp_path / "invalid.json"
    p.write_text("{")

    try:
        with pytest.raises(InvalidMetadataJson):
            FakeDataBuilder(metadata_filename=p.absolute())
    finally:
        p.unlink()


def test_missing_type_metadata_json_should_default_type_to_dataframe(tmp_path):
    """Provide an valid metadata json with missing type attribute.

    Args:
        tmp_path (Path): Temporary Path
    """
    p = tmp_path / "missing_type.json"
    metadata = MetaDataBuilder.dataframe_simple()
    p.write_text(json.dumps(metadata))

    try:
        builder = FakeDataBuilder(metadata_filename=p.absolute())
        assert builder.metadata["type"] == "dataframe"
    finally:
        p.unlink()


def test_invalid_type_metadata_json_should_raise_exception(tmp_path):
    """Provide an valid metadata json with missing type attribute.

    Args:
        tmp_path (Path): Temporary Path
    """
    p = tmp_path / "missing_type.json"
    metadata = MetaDataBuilder.dataframe_simple()
    metadata["type"] = "invalid"
    p.write_text(json.dumps(metadata))

    try:
        with pytest.raises(InvalidProviderType):
            FakeDataBuilder(metadata_filename=p.absolute())
    finally:
        p.unlink()
