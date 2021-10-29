"""String template builder."""
import re
from faker import Faker

from fake_data_builder.configuration import DEFAULT_LOCALE, MetadataKey
from fake_data_builder.errors import InvalidMetadataJson

RE_TOKEN = re.compile(r"\{\{\s*(\S+?)\s*\}\}")


class StrTemplate:
    """String template builder."""

    def __init__(self, metadata: dict):
        """Create an instance of builder.

        Args:
            metadata (dict): metadata.
        """
        self.__validate(metadata, "string")
        self.template = metadata["string"]

        self.count = metadata.get(MetadataKey.COUNT.value, 10)
        if self.count < 0:
            self.count = 0

        metadata.setdefault(MetadataKey.LOCALE.value, DEFAULT_LOCALE)
        self.locale = metadata.get(MetadataKey.LOCALE.value)
        self.seed = metadata.get(MetadataKey.SEED.value)

    def __validate(self, metadata: dict, name: str):
        if (
            metadata.get(name) is None
            or not isinstance(metadata[name], str)
            or len(metadata[name].strip()) == 0
        ):
            raise InvalidMetadataJson(f"{name} was missing in metadata")

    def __build(self, faker: Faker):
        result = self.template

        while m := RE_TOKEN.search(result):  # noqa E701 support walrus
            span = m.span()
            result = result[0 : span[0]] + str(eval(m.groups()[0])) + result[span[1] :]

        return result

    def build(self):
        """Build.

        Returns:
            list: List of string
        """
        if self.seed:
            Faker.seed(self.seed)

        faker = Faker(self.locale)

        result = [self.__build(faker) for i in range(0, self.count)]

        if len(result) == 0:
            return None

        return result if len(result) > 1 else result[0]
