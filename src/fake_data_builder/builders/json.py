"""String template builder."""

import copy
import re
import uuid

from faker import Faker

from fake_data_builder.configuration import DEFAULT_LOCALE, MetadataKey
from fake_data_builder.errors import InvalidMetadataJson
from faker_ex import FakerEx

RE_TOKEN = re.compile(r"\{\{\s*(\S+?)\s*\}\}")


class Json:
    """JSON data builder."""

    def __init__(self, metadata: dict):
        """Create an instance of builder.

        Args:
            metadata (dict): metadata.
        """
        self.__validate(metadata, "schema")
        self.schema = metadata["schema"]

        self.count = metadata.get(MetadataKey.COUNT.value, 10)
        if self.count < 0:
            self.count = 0

        metadata.setdefault(MetadataKey.LOCALE.value, DEFAULT_LOCALE)
        self.locale = metadata.get(MetadataKey.LOCALE.value)
        self.seed = metadata.get(MetadataKey.SEED.value)

    def __validate(self, metadata: dict, name: str):
        if metadata.get(name) is None or not isinstance(metadata[name], dict):
            raise InvalidMetadataJson(f"{name} was missing in metadata")

    def __eval_val(self, obj, faker):
        if isinstance(obj, str):
            while m := RE_TOKEN.search(obj):  # noqa E701 support walrus
                span = m.span()
                obj = (
                    str(uuid.uuid4())
                    if m.groups()[0] == "faker.uuid()"
                    else obj[0 : span[0]] + str(eval(m.groups()[0])) + obj[span[1] :]
                )
            return obj

        if isinstance(obj, list):
            return [self.__eval_val(x, faker) for x in obj]

        if isinstance(obj, dict):
            for k in obj:
                obj[k] = self.__eval_val(obj[k], faker)
            return obj

    def __build(self, faker: Faker):
        schema = copy.deepcopy(self.schema)
        return self.__eval_val(schema, faker)

    def build(self):
        """Build.

        Returns:
            list: List of string
        """
        faker = FakerEx.get_faker(self.locale, self.seed)

        result = [self.__build(faker) for i in range(0, self.count)]

        if len(result) == 0:
            return None

        return result if len(result) > 1 else result[0]
