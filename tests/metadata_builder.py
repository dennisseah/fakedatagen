"""MetaData Builder for tests."""


class MetaDataBuilder:
    """MetaData Builder."""

    @staticmethod
    def dataframe_simple():
        """Return a simple dataframe metadata to path."""
        data = {
            "columns": [
                {"name": "language", "text": "en_US"},
                {"name": "customer_name", "func": "faker.company()"},
                {"name": "transcript", "func": "' '.join(faker.paragraphs())"},
            ],
            "rows": [{"count": 5, "locale": "en_US", "seed": 1234}],
        }

        return data

    @staticmethod
    def template_simple(count=1):
        """Return a simple string templaate metadata to path."""
        data = {
            "type": "str_template",
            "string": "I am {{ faker.first_name() }} {{ faker.last_name() }}. I live in {{ faker.address() }}. I am born in {{ faker.date_of_birth() }}. My email address is {{ faker.ascii_free_email() }} and phone number is {{ faker.phone_number() }}. I work as a {{ faker.job() }} in {{ faker.company() }}. My employee id is {{ faker.bothify('????-########') }}",
            "count": count,
            "locale": "en_US",
            "seed": 999,
        }

        return data
