"""Test code."""

from lib.fake_data_builder import FakeDataBuilder

builder = FakeDataBuilder("./metadata_json.json")
result = builder.build()
print(result)
