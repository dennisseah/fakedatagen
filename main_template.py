"""Test code."""

from lib.fake_data_builder import FakeDataBuilder

builder = FakeDataBuilder("./metadata_template.json")
df = builder.build()
print(df)
