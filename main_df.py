"""Test code."""

from lib.fake_data_builder import FakeDataBuilder

builder = FakeDataBuilder("./metadata.json")
df = builder.build()
print(df)
