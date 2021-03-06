"""Fake Data Builder DataFrame Tests."""
import json

import pytest

from fake_data_builder.fake_data_builder import FakeDataBuilder
from fake_data_builder.configuration import MetadataKey
from fake_data_builder.errors import InvalidMetadataJson

from tests.metadata_builder import MetaDataBuilder
from tests.commons import write_metadata_file


def _validate_df(metadata, df):
    metadata_col_names = [c["name"] for c in metadata["columns"]]
    assert df.columns.values.tolist() == metadata_col_names
    assert df.shape[0] == metadata["rows"][0].get(MetadataKey.COUNT.value, 10)


def deco(count=5, drop=None):
    """Test decorator.

    Args:
        count (int, optional): count of generate items. Defaults to 5.
        drop ([type], optional): key of metadata to drop. Defaults to None.
    """

    def wrap(f):
        def wrapped_f(tmp_path):
            try:
                md, p = write_metadata_file(
                    tmp_path, MetaDataBuilder.dataframe_simple, count=count, drop=drop
                )
                f(md, p)
            finally:
                p.unlink()

        return wrapped_f

    return wrap


@deco()
def test_sanity(metadata, fp):
    """Sanity Test.

    Args:
        metadata (dict): metadata
        fp (Path): Path where metadata file resides.
    """
    bldr = FakeDataBuilder(metadata_filename=fp.absolute())
    df = bldr.build()
    _validate_df(metadata, df)


@deco(drop="columns")
def test_missing_cols_should_raise_except(metadata, fp):
    """Missing columns attribute in metadata.

    Args:
        metadata (dict): metadata
        fp (Path): Path where metadata file resides.
    """
    with pytest.raises(InvalidMetadataJson):
        bldr = FakeDataBuilder(metadata_filename=fp.absolute())
        bldr.build()


@deco(drop="rows")
def test_missing_rows_should_raise_except(metadata, fp):
    """Missing rows attribute in metadata.

    Args:
        metadata (dict): metadata
        fp (Path): Path where metadata file resides.
    """
    with pytest.raises(InvalidMetadataJson):
        bldr = FakeDataBuilder(metadata_filename=fp.absolute())
        bldr.build()


@deco(drop="/rows/0/seed")
def test_missing_seed_should_be_ok(metadata, fp):
    """Missing seed in rows attribute in metadata.

    Args:
        metadata (dict): metadata
        fp (Path): Path where metadata file resides.
    """
    bldr = FakeDataBuilder(metadata_filename=fp.absolute())
    df = bldr.build()
    _validate_df(metadata, df)


@deco(count=-1)
def test_negative_count(metadata, fp):
    """Negative count in rows attribute in metadata.

    Args:
        metadata (dict): metadata
        fp (Path): Path where metadata file resides.
    """
    bldr = FakeDataBuilder(metadata_filename=fp.absolute())
    df = bldr.build()
    assert df.shape[0] == 0


@deco(drop="/rows/0/count")
def test_missing_count_should_default_count_to_10(metadata, fp):
    """Missing count in rows attribute in metadata.

    Args:
        metadata (dict): metadata
        fp (Path): Path where metadata file resides.
    """
    bldr = FakeDataBuilder(metadata_filename=fp.absolute())
    df = bldr.build()
    _validate_df(metadata, df)


@deco(drop="/rows/0/locale")
def test_missing_locale_should_default_count_to_10(metadata, fp):
    """Missing count in locale attribute in metadata.

    Args:
        metadata (dict): metadata
        fp (Path): Path where metadata file resides.
    """
    bldr = FakeDataBuilder(metadata_filename=fp.absolute())
    df = bldr.build()
    _validate_df(metadata, df)


@deco(drop="/columns/0/name")
def test_missing_column_name_should_raise_except(metadata, fp):
    """Missing column name in rows attribute in metadata.

    Args:
        metadata (dict): metadata
        fp (Path): Path where metadata file resides.
    """
    with pytest.raises(InvalidMetadataJson):
        bldr = FakeDataBuilder(metadata_filename=fp.absolute())
        bldr.build()


@deco(drop="/columns/0/text")
def test_missing_column_text_should_raise_except(metadata, fp):
    """Missing column text in rows attribute in metadata.

    Args:
        metadata (dict): metadata
        fp (Path): Path where metadata file resides.
    """
    with pytest.raises(InvalidMetadataJson):
        bldr = FakeDataBuilder(metadata_filename=fp.absolute())
        bldr.build()


@deco(drop="/columns/1/func")
def test_missing_column_func_should_raise_except(metadata, fp):
    """Missing column func in rows attribute in metadata.

    Args:
        metadata (dict): metadata
        fp (Path): Path where metadata file resides.
    """
    with pytest.raises(InvalidMetadataJson):
        bldr = FakeDataBuilder(metadata_filename=fp.absolute())
        bldr.build()


def test_missing_invalid_func_should_raise_except(tmp_path):
    """Missing invalid func in rows attribute in metadata.

    Args:
        tmp_path (Path): Temporary path.
    """
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
