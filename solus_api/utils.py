import json


from .types import GeneralDict


def dump_json(filename: str, obj: GeneralDict) -> None:
    with open(filename, "w") as f:
        json.dump(obj, f)
