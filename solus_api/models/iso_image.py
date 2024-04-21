# from pprint import pprint
from ..types import GeneralDict


class IsoImage:
    def __init__(self, data: GeneralDict):
        self.name: str = data.get("name", "")
        self.icon: str = data.get("icon", "")
        self.os_type: str = data.get("os_type", "")
        self.iso_url: str = data.get("iso_url", "")
        self.use_tls: bool = data.get("use_tls", False)
        self.checksum_method: str = data.get("checksum_method", "")
        self.checksum: str = data.get("checksum", "")
        self.show_url_and_checksum: bool = data.get("show_url_and_checksum", False)
        self.show_tls: bool = data.get("show_tls", False)
