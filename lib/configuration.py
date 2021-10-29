"""Configurations and Defaults."""

from enum import Enum

DEFAULT_LOCALE = "en_US"


class MetadataKey(Enum):
    """Metadata Keys."""

    TYPE = "type"
    LOCALE = "locale"
    SEED = "seed"
    COUNT = "count"
