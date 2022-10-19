"""Test code."""

import json

from fake_data_builder.fake_data_builder import FakeDataBuilder

builder = FakeDataBuilder("./samples/data/metadata_json.json")
result = builder.build()
print(json.dumps(result, indent=2))
