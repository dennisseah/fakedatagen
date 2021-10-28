"""MetaData Builder for tests."""


class MetaDataBuilder:
    """MetaData Builder."""

    @staticmethod
    def dataframe_simple():
        """Return a simple dataframe metadata."""
        return {
            "columns": [
                {"name": "language", "text": "en_US"},
                {"name": "customer_name", "func": "faker.company()"},
                {"name": "transcript", "func": "' '.join(faker.paragraphs())"},
            ],
            "rows": [{"count": 5, "locale": "en_US", "seed": 1234}],
        }

    @staticmethod
    def json_simple(count=1):
        """Return a simple json metadata."""
        return {
            "type": "json",
            "schema": {
                "first_name": "{{ faker.first_name() }}",
                "last_name": "{{ faker.last_name() }}",
                "address": "{{ faker.address() }}",
                "date_of_birth": "{{ faker.date_of_birth() }}",
                "email_address": "{{ faker.ascii_free_email() }}",
                "phones": [
                    {"type": "cell", "number": "{{ faker.phone_number() }}"},
                    {"type": "home", "number": "{{ faker.phone_number() }}"},
                ],
                "employer": {"company": "{{ faker.company() }}", "job": "{{ faker.job() }}"},
            },
            "count": count,
            "locale": "en_US",
            "seed": 999,
        }

    @staticmethod
    def template_simple(count=1):
        """Return a simple string template metadata."""
        return {
            "type": "str_template",
            "string": "I am {{ faker.first_name() }} {{ faker.last_name() }}. I live in {{ faker.address() }}. I am born in {{ faker.date_of_birth() }}. My email address is {{ faker.ascii_free_email() }} and phone number is {{ faker.phone_number() }}. I work as a {{ faker.job() }} in {{ faker.company() }}. My employee id is {{ faker.bothify('????-########') }}",  # noqa E502
            "count": count,
            "locale": "en_US",
            "seed": 999,
        }
