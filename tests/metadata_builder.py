"""MetaData Builder for tests."""

from lib.configuration import DEFAULT_LOCALE


class MetaDataBuilder:
    """MetaData Builder."""

    @staticmethod
    def dataframe_simple(count=1):
        """Return a simple dataframe metadata."""
        return {
            "columns": [
                {"name": "language", "text": DEFAULT_LOCALE},
                {"name": "customer_name", "func": "faker.company()"},
                {"name": "transcript", "func": "' '.join(faker.paragraphs())"},
            ],
            "rows": [{"count": count, "locale": DEFAULT_LOCALE, "seed": 1234}],
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
                "email_address": "{{ faker.ascii_free_email() }}",
                "phones": [
                    {"type": "cell", "number": "{{ faker.phone_number() }}"},
                    {"type": "home", "number": "{{ faker.phone_number() }}"},
                ],
                "employer": {"company": "{{ faker.company() }}", "job": "{{ faker.job() }}"},
            },
            "count": count,
            "locale": DEFAULT_LOCALE,
            "seed": 999,
        }

    @staticmethod
    def template_simple(count=1):
        """Return a simple string template metadata."""
        return {
            "type": "str_template",
            "string": "I am {{ faker.first_name() }} {{ faker.last_name() }}. I live in {{ faker.address() }}. My email address is {{ faker.ascii_free_email() }} and phone number is {{ faker.phone_number() }}. I work as a {{ faker.job() }} in {{ faker.company() }}. My employee id is {{ faker.bothify('????-########') }}",  # noqa E502
            "count": count,
            "locale": DEFAULT_LOCALE,
            "seed": 999,
        }
