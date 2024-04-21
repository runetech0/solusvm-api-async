from typing import Dict, List, Optional
from ..types import GeneralDict
from .ip_block import IpBlock


class Location:
    def __init__(self, data: GeneralDict):
        self.id: int = data.get("id", 0)
        self.name: str = data.get("name", "")
        self.description: str = data.get("description", "")
        self.icon: Dict[str, str] = data.get("icon", {})
        self.is_default: bool = data.get("is_default", False)
        self.is_visible: bool = data.get("is_visible", False)
        self.position: float = data.get("position", 0.0)


class Storage:
    def __init__(self, data: GeneralDict):
        self.id: int = data.get("id", 0)
        self.name: Optional[str] = data.get("name", None)
        self.type: Dict[str, List[str]] = data.get("type", {})
        self.mount: str = data.get("mount", "")
        self.path: str = data.get("path", "")
        self.thin_pool: Optional[str] = data.get("thin_pool", None)
        self.is_available_for_balancing: bool = data.get(
            "is_available_for_balancing", False
        )
        self.credentials: Optional[str] = data.get("credentials", None)
        self.free_space: float = data.get("free_space", 0.0)


class Capabilities:
    def __init__(self, data: GeneralDict):
        self.kvm: bool = data.get("kvm", False)
        self.vz: bool = data.get("vz", False)
        self.is_management_node: bool = data.get("is_management_node", False)
        self.is_mem_balloon_free_page_reporting_supported: bool = data.get(
            "is_mem_balloon_free_page_reporting_supported", False
        )
        self.is_virtio_discard_supported: bool = data.get(
            "is_virtio_discard_supported", False
        )


class Limits:
    def __init__(self, data: GeneralDict):
        self.vm: Dict[str, bool] = data.get("vm", {})
        self.hdd: Dict[str, bool] = data.get("hdd", {})
        self.ram: Dict[str, bool] = data.get("ram", {})
        self.vcpu: Dict[str, bool] = data.get("vcpu", {})


class Network:
    def __init__(self, data: GeneralDict):
        self.bridges: List[Dict[str, str]] = data.get("bridges", [])
        self.type: str = data.get("type", "")
        self.ip_for_vpc_network: Optional[str] = data.get("ip_for_vpc_network", None)


class Settings:
    def __init__(self, data: GeneralDict):
        self.cache_path: str = data.get("cache_path", "")
        self.iso_path: str = data.get("iso_path", "")
        self.backup_tmp_path: str = data.get("backup_tmp_path", "")
        self.vnc_proxy_port: int = data.get("vnc_proxy_port", 0)
        self.limits: Limits = Limits(data.get("limits", {}))
        self.balance_strategy: str = data.get("balance_strategy", "")
        self.network: Network = Network(data.get("network", {}))
        self.arch: str = data.get("arch", "")
        self.virtualization_types: List[str] = data.get("virtualization_types", [])
        self.vs_disk_cache_mode: Optional[str] = data.get("vs_disk_cache_mode", None)
        self.concurrent_backups: Dict[str, int] = data.get("concurrent_backups", {})


class Metrics:
    def __init__(self, data: GeneralDict):
        self.network: Dict[str, bool] = data.get("network", {})


class ComputeResource:
    def __init__(self, data: GeneralDict):
        self.id: int = data.get("id", 0)
        self.name: str = data.get("name", "")
        self.host: str = data.get("host", "")
        self.agent_port: int = data.get("agent_port", 0)
        self.version: str = data.get("version", "")
        self.status: str = data.get("status", "")
        self.locations: List[Location] = [
            Location(location) for location in data.get("locations", [])
        ]
        self.ip_blocks: List[IpBlock] = [
            IpBlock(ip_block) for ip_block in data.get("ip_blocks", [])
        ]
        self.storages: List[Storage] = [
            Storage(storage) for storage in data.get("storages", [])
        ]
        self.capabilities: Capabilities = Capabilities(data.get("capabilities", {}))
        self.is_locked: bool = data.get("is_locked", False)
        self.vms_count: int = data.get("vms_count", 0)
        self.settings: Settings = Settings(data.get("settings", {}))
        self.metrics: Metrics = Metrics(data.get("metrics", {}))
