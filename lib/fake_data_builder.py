"""Fake Data Builder."""

import json

from lib.builders.dataframe import Dataframe
from lib.builders.json import Json
from lib.builders.str_template import StrTemplate
from lib.configuration import MetadataKey
from lib.errors import InvalidMetadataJson, InvalidProviderType

PROVIDER_MAP = {
    "dataframe": Dataframe,
    "json": Json,
    "str_template": StrTemplate,
}


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
                self.metadata.setdefault(MetadataKey.TYPE.value, "dataframe")

                self._builder = self._get_builder()
        except json.decoder.JSONDecodeError as e:
            raise InvalidMetadataJson("Invalid metadata json") from e

    def _get_builder(self):
        """Return builder provider."""
        provider_type = self.metadata[MetadataKey.TYPE.value]
        provider = PROVIDER_MAP.get(provider_type)

        if not provider:
            raise InvalidProviderType(f"unknown builder type, {provider_type}")

        return provider(self.metadata)

    def build(self):
        """Build the data set."""
        return self._builder.build()
