from typing import List, Dict, Union
from ..types import GeneralDict
import math


class BackupSettings:
    def __init__(self, data: GeneralDict):
        self.is_incremental_backup_enabled: bool = data.get(
            "is_incremental_backup_enabled", False
        )
        self.incremental_backups_limit: int = data.get("incremental_backups_limit", 0)


class Limit:
    def __init__(self, data: GeneralDict):
        self.unit: str = data.get("unit", "")
        self.limit: Union[str, int] = data.get("limit", 0)
        self.is_enabled: bool = data.get("is_enabled", False)


class Params:
    def __init__(self, data: GeneralDict):
        self.data = data
        self.vcpu: int = data.get("vcpu", "")
        self.ram: int = data.get("ram", "")
        self.disk: int = data.get("disk", "")

    @property
    def ram_converted(self) -> float:
        if self.ram == 0:
            return 0.0
        i = int(math.floor(math.log(self.ram, 1024)))
        p = math.pow(1024, i)
        s = round(self.ram / p, 2)
        return s


class SolusPlan:
    def __init__(self, data: GeneralDict):
        self.id: int = data.get("id", 0)
        self.name: str = data.get("name", "")
        self.params: Params = Params(data.get("params", {}))
        self.virtualization_type: str = data.get("virtualization_type", "")
        self.storage_type: str = data.get("storage_type", "")
        self.image_format: str = data.get("image_format", "")
        self.is_default: bool = data.get("is_default", False)
        self.is_snapshot_available: bool = data.get("is_snapshot_available", False)
        self.is_snapshots_enabled: bool = data.get("is_snapshots_enabled", False)
        self.is_backup_available: bool = data.get("is_backup_available", False)
        self.backup_settings: BackupSettings = BackupSettings(
            data.get("backup_settings", {})
        )
        self.is_additional_ips_available: bool = data.get(
            "is_additional_ips_available", False
        )
        self.is_visible: bool = data.get("is_visible", False)
        self.is_thin_provisioned: bool = data.get("is_thin_provisioned", False)
        self.is_custom: bool = data.get("is_custom", False)
        self.position: int = data.get("position", 0)
        self.reset_limit_policy: str = data.get("reset_limit_policy", "")
        self.network_traffic_limit_type: str = data.get(
            "network_traffic_limit_type", ""
        )
        self.limits: Dict[str, Limit] = {
            key: Limit(val) for key, val in data.get("limits", {}).items()
        }
        self.available_os_image_versions: List[GeneralDict] = data.get(
            "available_os_image_versions", []
        )
        self.available_locations: List[Dict[str, Union[int, str]]] = data.get(
            "available_locations", []
        )
        self.available_applications: List[Dict[str, Union[int, str]]] = data.get(
            "available_applications", []
        )
        self.tokens_per_hour: int = data.get("tokens_per_hour", 0)
        self.tokens_per_month: int = data.get("tokens_per_month", 0)
        self.ip_tokens_per_month: int = data.get("ip_tokens_per_month", 0)
        self.ip_tokens_per_hour: int = data.get("ip_tokens_per_hour", 0)
        self.iso_image_tokens_per_hour: int = data.get("iso_image_tokens_per_hour", 0)
        self.iso_image_tokens_per_month: int = data.get("iso_image_tokens_per_month", 0)
        self.backup_price: int = data.get("backup_price", 0)

    def basic_details(self, with_os: bool = False) -> str:
        msg = f"""

{self.name}
VCPUs: {self.params.vcpu}
RAM: {self.params.ram}
Disk: {self.params.disk}
"""
        if with_os:
            msg = f"""
{msg}
Availabls OSs: {", ".join([n["name".__str__()] for n in self.available_os_image_versions])}
"""

        return msg

    def selected_details_message(self, os_id: int) -> str:
        os_name = ""
        for os in self.available_os_image_versions:
            if int(os.get("id", "")) == os_id:
                os_name = os.get("name")
        return f"""
{self.basic_details()}
Selected OS: {os_name}
"""
