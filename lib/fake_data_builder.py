"""Fake Data Builder."""

import json

from lib.builders.dataframe import Dataframe
from lib.builders.str_template import StrTemplate
from lib.errors import InvalidMetadataJson


class FakeDataBuilder:
    """Fake Data Builder."""

    def __init__(self, metadata_filename: str):
        """Create an instance of builder.

        Args:
            metadata_filename (str): metadata filename (JSON format)
        """
        try:
            with open(metadata_filename) as metadata_file:
                self.metadata = json.load(metadata_file)
                self.metadata.setdefault("type", "dataframe")

                self._builder = self._get_builder()
        except json.decoder.JSONDecodeError as e:
            raise InvalidMetadataJson("Invalid metadata json") from e

    def _get_builder(self):
        """Return builder provider."""
        if self.metadata["type"] == "dataframe":
            return Dataframe(self.metadata)

        if self.metadata["type"] == "str_template":
            return StrTemplate(self.metadata)

        raise InvalidMetadataJson(f"unknown builder type, {self.metadata['type']}")

    def build(self):
        """Build the data set."""
        return self._builder.build()
