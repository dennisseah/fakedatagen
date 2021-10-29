"""Test code."""
from fake_data_builder.fake_data_builder import FakeDataBuilder


builder = FakeDataBuilder("./samples/data/metadata.json")
df = builder.build()
print(df)
