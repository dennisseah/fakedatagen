"""Fake Data Builder."""

import json
from lib.builders.dataframe import Dataframe
from lib.builders.str_template import StrTemplate


class FakeDataBuilder:
    """Fake Data Builder."""

    def __init__(self, metadata_filename: str):
        """Create an instance of builder.

        Args:
            metadata_filename (str): metadata filename (JSON format)
        """
        with open(metadata_filename) as metadata_file:
            self.metadata = json.load(metadata_file)
            if not self.metadata.get("type"):
                self.metadata["type"] = "dataframe"

    def build(self):
        """Build the data set."""
        if self.metadata["type"] == "dataframe":
            df = Dataframe(self.metadata)
            return df.build()

        if self.metadata["type"] == "str_template":
            df = StrTemplate(self.metadata)
            return df.build()

        raise AttributeError(f"unknown builder type, {self.metadata['type']}")
