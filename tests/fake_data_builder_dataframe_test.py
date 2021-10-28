"""Fake Data Builder DataFrame Tests."""
import json

import pytest

from lib.fake_data_builder import FakeDataBuilder
from lib.errors import InvalidMetadataJson

from tests.metadata_builder import MetaDataBuilder


def _validate_df(metadata, df):
    metadata_col_names = [c["name"] for c in metadata["columns"]]
    assert df.columns.values.tolist() == metadata_col_names
    assert df.shape[0] == metadata["rows"][0].get("count", 10)


def test_sanity(tmp_path):
    """Sanity Test."""
    try:
        metadata = MetaDataBuilder.dataframe_simple()
        p = tmp_path / "simple_df.json"
        p.write_text(json.dumps(metadata))

        bldr = FakeDataBuilder(metadata_filename=p.absolute())
        df = bldr.build()
        _validate_df(metadata, df)
    finally:
        p.unlink()


def test_missing_cols_should_raise_except(tmp_path):
    """Missing columns attribute in metadata."""
    try:
        metadata = MetaDataBuilder.dataframe_simple()
        metadata.pop("columns")
        p = tmp_path / "missing_cols_attr_in_df.json"
        p.write_text(json.dumps(metadata))

        with pytest.raises(InvalidMetadataJson):
            bldr = FakeDataBuilder(metadata_filename=p.absolute())
            bldr.build()
    finally:
        p.unlink()


def test_missing_rows_should_raise_except(tmp_path):
    """Missing rows attribute in metadata."""
    try:
        metadata = MetaDataBuilder.dataframe_simple()
        metadata.pop("rows")
        p = tmp_path / "missing_rows_attr_in_df.json"
        p.write_text(json.dumps(metadata))

        with pytest.raises(InvalidMetadataJson):
            bldr = FakeDataBuilder(metadata_filename=p.absolute())
            bldr.build()
    finally:
        p.unlink()


def test_missing_seed_should_be_ok(tmp_path):
    """Missing seed in rows attribute in metadata."""
    try:
        metadata = MetaDataBuilder.dataframe_simple()
        metadata["rows"][0].pop("seed")

        p = tmp_path / "missing_seed_attr_in_df.json"
        p.write_text(json.dumps(metadata))

        bldr = FakeDataBuilder(metadata_filename=p.absolute())
        df = bldr.build()
        _validate_df(metadata, df)
    finally:
        p.unlink()


def test_missing_count_should_default_count_to_10(tmp_path):
    """Missing count in rows attribute in metadata."""
    try:
        metadata = MetaDataBuilder.dataframe_simple()
        metadata["rows"][0].pop("count")

        p = tmp_path / "missing_count_attr_in_df.json"
        p.write_text(json.dumps(metadata))

        bldr = FakeDataBuilder(metadata_filename=p.absolute())
        df = bldr.build()
        _validate_df(metadata, df)
    finally:
        p.unlink()


def test_missing_locale_should_default_count_to_10(tmp_path):
    """Missing locale in rows attribute in metadata."""
    try:
        metadata = MetaDataBuilder.dataframe_simple()
        metadata["rows"][0].pop("locale")

        p = tmp_path / "missing_locale_attr_in_df.json"
        p.write_text(json.dumps(metadata))

        bldr = FakeDataBuilder(metadata_filename=p.absolute())
        df = bldr.build()
        _validate_df(metadata, df)
    finally:
        p.unlink()


def test_missing_column_name_should_raise_except(tmp_path):
    """Missing column name in rows attribute in metadata."""
    try:
        metadata = MetaDataBuilder.dataframe_simple()
        metadata["columns"][0].pop("name")

        p = tmp_path / "missing_col_name_attr_in_df.json"
        p.write_text(json.dumps(metadata))

        with pytest.raises(InvalidMetadataJson):
            bldr = FakeDataBuilder(metadata_filename=p.absolute())
            bldr.build()
    finally:
        p.unlink()


def test_missing_column_text_should_raise_except(tmp_path):
    """Missing column text in rows attribute in metadata."""
    try:
        metadata = MetaDataBuilder.dataframe_simple()
        metadata["columns"][0].pop("text")

        p = tmp_path / "missing_col_text_attr_in_df.json"
        p.write_text(json.dumps(metadata))

        with pytest.raises(InvalidMetadataJson):
            bldr = FakeDataBuilder(metadata_filename=p.absolute())
            bldr.build()
    finally:
        p.unlink()


def test_missing_column_func_should_raise_except(tmp_path):
    """Missing column func in rows attribute in metadata."""
    try:
        metadata = MetaDataBuilder.dataframe_simple()
        metadata["columns"][1].pop("func")

        p = tmp_path / "missing_col_func_attr_in_df.json"
        p.write_text(json.dumps(metadata))

        with pytest.raises(InvalidMetadataJson):
            bldr = FakeDataBuilder(metadata_filename=p.absolute())
            bldr.build()
    finally:
        p.unlink()


def test_missing_invalid_func_should_raise_except(tmp_path):
    """Missing invalid func in rows attribute in metadata."""
    try:
        metadata = MetaDataBuilder.dataframe_simple()
        metadata["columns"][1]["func"] = "faker.x()"

        p = tmp_path / "missing_col_func_attr_in_df.json"
        p.write_text(json.dumps(metadata))

        with pytest.raises(AttributeError):
            bldr = FakeDataBuilder(metadata_filename=p.absolute())
            bldr.build()
    finally:
        p.unlink()
