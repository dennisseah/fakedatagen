from faker import Faker

from providers.ontology_provider import OntologyProvider


class FakerEx:
    @staticmethod
    def get_faker(locale: str, seed: int = None):
        if seed:
            Faker.seed(seed)

        faker = Faker(locale)
        faker.add_provider(OntologyProvider)

        return faker
