"""Pandas dataframe builder."""
import pandas as pd
from faker import Faker

from lib.errors import InvalidMetadataJson
from lib.configuration import DEFAULT_LOCALE, MetadataKey


class Dataframe:
    """Pandas dataframe builder."""

    def __init__(self, metadata: dict):
        """Create an instance of builder.

        Args:
            metadata (dict): metadata.
        """
        self.__validate(metadata, "rows")
        self.rows = metadata["rows"]

        self.__validate(metadata, "columns")
        self.columns = metadata["columns"]

    def __validate(self, metadata: dict, name: str):
        if (
            metadata.get(name) is None
            or not isinstance(metadata[name], list)
            or len(metadata[name]) == 0
        ):
            raise InvalidMetadataJson(f"{name} was missing in metadata")

    def __build_rows(
        self,
        df: pd.DataFrame,
        count: int,
        column_generator: dict,
        locale: str,
        seed: int,
    ):
        if not locale:
            locale = DEFAULT_LOCALE

        faker = Faker(locale)
        Faker.seed(seed)

        for _ in range(count):
            df = df.append(
                self.__build_row(faker, column_generator),
                ignore_index=True,
            )

        return df

    def __get_column_val(
        self,
        faker: Faker,
        col: dict,
        column_generator: dict,
    ):
        col_name = col["name"]
        coln = (
            column_generator.get(col_name)
            if column_generator and column_generator.get(col_name)
            else col
        )

        return coln.get("text") if coln.get("text") else eval(coln["func"])

    def __build_row(self, faker, column_generator: dict):
        data = {}
        for col in self.columns:
            try:
                data[col["name"]] = self.__get_column_val(
                    faker,
                    col,
                    column_generator,
                )
            except AttributeError:
                raise AttributeError(f"Unrecognized column func, {col['func']}.")
        return data

    def build(self):
        """Build the dataframe.

        Returns:
            pandas.dataframe: Pandas dataframe containing the data.
        """
        if not all(c.get("name") for c in self.columns):
            raise InvalidMetadataJson("Column name is required.")

        if not all(c.get("func") or c.get("text") for c in self.columns):
            raise InvalidMetadataJson("Column func or text is required.")

        column_names = [x["name"] for x in self.columns]
        df = pd.DataFrame(columns=column_names)

        for row in self.rows:
            df = self.__build_rows(
                df,
                row.get(MetadataKey.COUNT.value, 10),
                row.get("columns"),
                row.get(MetadataKey.LOCALE.value),
                row.get(MetadataKey.SEED.value),
            )

        return df
