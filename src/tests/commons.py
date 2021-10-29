"""Common tests library."""

import json
import uuid
from pathlib import Path


def write_metadata_file(tmp: Path, md_fn, count: int = 1, drop: str = None):
    """Write metadata to file.

    Args:
        tmp (Path): Temporary Path.
        md_fn ([type]): test metadata generator function
        count (int, optional): number of items. Defaults to 1.
        drop (str, optional): key in metadata to be dropped. Defaults to None.

    Returns:
        (dict, Path): metadata and path
    """
    metadata = md_fn(count=count)

    if drop:
        tokens = [x for x in drop.split("/") if x]

        current = metadata
        for x in range(0, len(tokens) - 1):
            idx = int(tokens[x]) if tokens[x].isdigit() else tokens[x]
            current = current[idx]

        assert current.get(tokens[-1]) is not None
        current.pop(tokens[-1])
        assert current.get(tokens[-1]) is None

    file_name = str(uuid.uuid4()).replace("-", "")
    p = tmp / f"{file_name}.json"
    p.write_text(json.dumps(metadata))
    return metadata, p
