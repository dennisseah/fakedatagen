"""Error Classes."""


class InvalidMetadataJson(Exception):
    """Invalid Metadata where it has invalid JSON format."""

    pass


class InvalidProviderType(Exception):
    """Invalid Provider Type. The supported types are dataframe and str_template."""

    pass
