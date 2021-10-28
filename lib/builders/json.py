"""String template builder."""
import copy
import re
from faker import Faker

from lib.errors import InvalidMetadataJson

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

        self.count = metadata.get("count", 10)
        if self.count < 0:
            self.count = 0

        metadata.setdefault("locale", "en_US")
        self.locale = metadata.get("locale")
        self.seed = metadata.get("seed")

    def __validate(self, metadata: dict, name: str):
        if metadata.get(name) is None or not isinstance(metadata[name], dict):
            raise InvalidMetadataJson(f"{name} was missing in metadata")

    def __eval_val(self, obj, faker):
        if isinstance(obj, str):
            while m := RE_TOKEN.search(obj):  # noqa E701 support walrus
                span = m.span()
                obj = obj[0 : span[0]] + str(eval(m.groups()[0])) + obj[span[1] :]
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
        if self.seed:
            Faker.seed(self.seed)

        faker = Faker(self.locale)

        result = [self.__build(faker) for i in range(0, self.count)]

        if len(result) == 0:
            return None

        return result if len(result) > 1 else result[0]
