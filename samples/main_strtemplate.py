"""Test code."""

from lib.fake_data_builder import FakeDataBuilder

builder = FakeDataBuilder("./samples/data/metadata_template.json")
result = builder.build()
print(result)
