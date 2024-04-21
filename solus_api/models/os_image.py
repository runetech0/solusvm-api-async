# from pprint import pprint
from typing import Dict


class OsImage:
    def __init__(self, data: Dict[str, str]):
        self.cloud_init_version: str = data.get("cloud_init_version", "")
        self.icon: str = data.get("icon", "")
        self.name: str = data.get("name", "")
        self.type: str = data.get("type", "")
        self.url: str = data.get("url", "")
