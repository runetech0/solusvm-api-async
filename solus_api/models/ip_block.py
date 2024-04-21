from ..types import GeneralDict
from typing import Dict, Union


class IpBlock:
    def __init__(self, data: GeneralDict):
        self.id: int = data.get("id", 0)
        self.name: str = data.get("name", "")
        self.gateway: str = data.get("gateway", "")
        self.netmask: str = data.get("netmask", "")
        self.ns_1: str = data.get("ns_1", "")
        self.ns_2: str = data.get("ns_2", "")
        self.from_: str = data.get(
            "from", ""
        )  # "from" is a reserved keyword in Python, so using "from_" instead
        self.to: str = data.get("to", "")
        self.type: str = data.get("type", "")
        self.list_type: str = data.get("list_type", "")
        self.range: int = data.get("range", 0)
        self.subnet: int = data.get("subnet", 0)
        self.reserved_ips_count: int = data.get("reserved_ips_count", 0)
        self.total_ips_count: str = data.get("total_ips_count", "")
        self.reverse_dns: Dict[str, Union[str, bool]] = data.get("reverse_dns", {})
