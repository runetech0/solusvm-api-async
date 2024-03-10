# from pprint import pprint
from ..types import GeneralDict
from typing import List, Dict, Optional, Union
from .plan import SolusPlan


class OsImage:
    def __init__(self, data: Dict[str, str]):
        self.cloud_init_version: str = data.get("cloud_init_version", "")
        self.icon: str = data.get("icon", "")
        self.name: str = data.get("name", "")
        self.type: str = data.get("type", "")
        self.url: str = data.get("url", "")


class ApplicationLoginLink:
    def __init__(self, data: Dict[str, str]):
        print(data)
        self.type: str = data.get("type", "")
        self.content: str = data.get("content", "")


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


class ReverseDns:
    def __init__(self, data: GeneralDict):
        self.id: int = data.get("id", 0)
        self.ip_id: int = data.get("ip_id", 0)
        self.ip: str = data.get("ip", "")
        self.domain: str = data.get("domain", "")
        self.is_primary: bool = data.get("is_primary", False)


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


class Ip:
    def __init__(self, data: GeneralDict):
        self.id: int = data.get("id", 0)
        self.ip: str = data.get("ip", "")
        self.is_primary: bool = data.get("is_primary", False)
        self.is_reverse_dns_enabled: bool = data.get("is_reverse_dns_enabled", False)
        reverse_dns_data: GeneralDict | list[GeneralDict] = data.get("reverse_dns", {})
        if isinstance(reverse_dns_data, dict):
            self.reverse_dns = [ReverseDns(reverse_dns_data)]
        else:
            self.reverse_dns: List[ReverseDns] = [
                ReverseDns(entry) for entry in data.get("reverse_dns", [])
            ]
        self.user: Dict[str, str] = data.get("user", {})
        self.server: Dict[str, Union[int, str]] = data.get("server", {})
        self.ip_block: IpBlock = IpBlock(data.get("ip_block", {}))
        self.comment: str = data.get("comment", "")
        self.issued_for: str = data.get("issued_for", "")


class Location:
    def __init__(self, data: GeneralDict):
        self.id: int = data.get("id", 0)
        self.name: str = data.get("name", "")
        self.icon: Dict[str, str] = data.get("icon", {})
        self.description: str = data.get("description", "")
        self.is_default: bool = data.get("is_default", False)
        self.is_visible: bool = data.get("is_visible", False)
        self.position: int = data.get("position", 0)
        self.available_plans: List[Dict[str, Union[int, str]]] = data.get(
            "available_plans", []
        )


class LimitGroup:
    def __init__(self, data: GeneralDict):
        self.id: int = data.get("id", 0)
        self.name: str = data.get("name", "")
        self.vms: int = data.get("vms", 0)
        self.running_vms: int = data.get("running_vms", 0)
        self.additional_ips: int = data.get("additional_ips", 0)
        self.additional_ipv6: int = data.get("additional_ipv6", 0)
        self.iso_images: int = data.get("iso_images", 0)
        self.iso_images_size: int = data.get("iso_images_size", 0)
        self.users_count: int = data.get("users_count", 0)


class LimitUsage:
    def __init__(self, data: GeneralDict):
        self.servers: int = data.get("servers", 0)
        self.running_servers: int = data.get("running_servers", 0)
        self.additional_ips: int = data.get("additional_ips", 0)
        self.iso_images: int = data.get("iso_images", 0)
        self.iso_images_size: int = data.get("iso_images_size", 0)


class Language:
    def __init__(self, data: GeneralDict):
        self.id: int = data.get("id", 0)
        self.name: str = data.get("name", "")
        self.locale: str = data.get("locale", "")
        self.country: str = data.get("country", "")
        self.icon: Dict[str, str] = data.get("icon", {})
        self.is_default: bool = data.get("is_default", False)
        self.is_visible: bool = data.get("is_visible", False)
        self.users_count: int = data.get("users_count", 0)
        self.allowed_ips: List[str] = data.get("allowed_ips", [])
        self.is_two_factor_auth_enabled: bool = data.get(
            "is_two_factor_auth_enabled", False
        )
        self.two_factor_auth_recovery_code_count: int = data.get(
            "two_factor_auth_recovery_code_count", 0
        )


class Role:
    def __init__(self, data: GeneralDict):
        self.id: str = data.get("id", "")
        self.name: str = data.get("name", "")
        self.is_default: bool = data.get("is_default", False)
        self.permissions: List[Dict[str, Union[int, str]]] = data.get("permissions", [])


class User:
    def __init__(self, data: GeneralDict):
        self.id: str = data.get("id", "")
        self.email: str = data.get("email", "")
        self.billing_user_id: str = data.get("billing_user_id", "")
        self.billing_token: str = data.get("billing_token", "")
        self.email_verified_at: str = data.get("email_verified_at", "")
        self.created_at: Dict[str, Union[str, int]] = data.get("created_at", {})
        self.roles: List[Role] = [Role(role) for role in data.get("roles[]", [])]
        limit_group_data: GeneralDict = data.get("limit_group", {})
        self.limit_group: Optional[LimitGroup] = None
        if limit_group_data:
            self.limit_group = LimitGroup(limit_group_data)
        self.limit_usage: LimitUsage = LimitUsage(data.get("limit_usage", {}))
        self.status: str = data.get("status", "")
        self.has_verified_email: bool = data.get("has_verified_email", False)
        self.language: Language = Language(data.get("language", {}))
        self.allowed_ips: List[str] = data.get("allowed_ips", [])
        self.is_two_factor_auth_enabled: bool = data.get(
            "is_two_factor_auth_enabled", False
        )
        self.two_factor_auth_recovery_code_count: int = data.get(
            "two_factor_auth_recovery_code_count", 0
        )


class TokenPricing:
    def __init__(self, data: GeneralDict):
        self.unit_cost: int = data.get("unit_cost", 0)
        self.currency_code: str = data.get("currency_code", "")
        self.currency_decimals: int = data.get("currency_decimals", 0)
        self.currency_decimals_separator: str = data.get(
            "currency_decimals_separator", ""
        )
        self.currency_prefix: str = data.get("currency_prefix", "")
        self.currency_suffix: str = data.get("currency_suffix", "")
        self.currency_thousands_separator: str = data.get(
            "currency_thousands_separator", ""
        )
        self.taxes_inclusive: bool = data.get("taxes_inclusive", False)
        self.taxes: List[Dict[str, Union[int, str]]] = data.get("taxes", [])


class Project:
    def __init__(self, data: GeneralDict):
        self.id: int = data.get("id", 0)
        self.name: str = data.get("name", "")
        self.description: str = data.get("description", "")
        self.is_default: bool = data.get("is_default", False)
        self.is_owner: bool = data.get("is_owner", False)
        self.owner: User = User(data.get("owner", {}))
        self.members: int = data.get("members", 0)
        self.servers: int = data.get("servers", 0)
        self.token_pricing: TokenPricing = TokenPricing(data.get("token_pricing", {}))


class BackupSchedule:
    def __init__(self, data: GeneralDict):
        self.type: str = data.get("type", "")
        self.time: Dict[str, int] = data.get("time", {})
        self.days: List[int] = data.get("days", [])


class BackupLimit:
    def __init__(self, data: GeneralDict):
        self.limit: int = data.get("limit", 0)
        self.is_enabled: bool = data.get("is_enabled", False)
        self.unit: str = data.get("unit", "")


class BackupSettings:
    def __init__(self, data: GeneralDict):
        self.enabled: bool = data.get("enabled", False)
        self.schedule: BackupSchedule = BackupSchedule(data.get("schedule", {}))
        self.limit: BackupLimit = BackupLimit(data.get("limit", {}))


class Usage:
    def __init__(self, data: GeneralDict):
        self.cpu: int = data.get("cpu", 0)
        self.network: Dict[str, int] = data.get("network", {})
        self.disk: Dict[str, int] = data.get("disk", {})


class ComputeCapability:
    def __init__(self, data: Dict[str, bool]):
        self.kvm: bool = data.get("kvm", False)
        self.vz: bool = data.get("vz", False)
        self.is_management_node: bool = data.get("is_management_node", False)
        self.is_mem_balloon_free_page_reporting_supported: bool = data.get(
            "is_mem_balloon_free_page_reporting_supported", False
        )
        self.is_virtio_discard_supported: bool = data.get(
            "is_virtio_discard_supported", False
        )


class ComputeResource:
    def __init__(self, data: GeneralDict):
        self.id: int = data.get("id", 0)
        self.name: str = data.get("name", "")
        self.host: str = data.get("host", "")
        self.capabilities: ComputeCapability = ComputeCapability(
            data.get("capabilities", {})
        )


class Settings:
    def __init__(self, data: GeneralDict):
        self.disk_cache_mode: str = data.get("disk_cache_mode", "")
        self.disk_driver: str = data.get("disk_driver", "")
        self.guest_agent_available: bool = data.get("guest_agent_available", False)
        self.guest_tools_installed: bool = data.get("guest_tools_installed", False)
        self.mac_address: str = data.get("mac_address", "")
        self.user: str = data.get("user", "")
        self.vnc_enabled: bool = data.get("vnc_enabled", False)
        self.vnc_password: str = data.get("vnc_password", "")
        self.os_image: OsImage = OsImage(data.get("os_image", {}))
        self.application_login_link: list[ApplicationLoginLink] = [
            ApplicationLoginLink(d) for d in data.get("application_login_link", [])
        ]


class Server:
    def __init__(self, data: GeneralDict):
        self.id: int = data.get("id", 0)
        self.name: str = data.get("name", "")
        self.description: str = data.get("description", "")
        self.uuid: str = data.get("uuid", "")
        self.os_type: str = data.get("os_type", "")
        self.specifications: Dict[str, int] = data.get("specifications", {})
        self.plan = SolusPlan(data.get("plan", {}))
        self.settings: Settings = Settings(data.get("settings", {}))
        self.status: str = data.get("status", "")
        self.real_status: str = data.get("real_status", "")
        self.virtualization_type: str = data.get("virtualization_type", "")
        self.ips: List[Ip] = [Ip(ip_data) for ip_data in data.get("ips", [])]
        self.fqdns: List[str] = data.get("fqdns", [])
        self.boot_mode: str = data.get("boot_mode", "")
        self.is_suspended: bool = data.get("is_suspended", False)
        self.is_processing: bool = data.get("is_processing", False)
        self.progress: int = data.get("progress", 0)
        self.user: User = User(data.get("user", {}))
        self.backup_settings: BackupSettings = BackupSettings(
            data.get("backup_settings", {})
        )
        self.next_scheduled_backup_at: str = data.get("next_scheduled_backup_at", "")
        self.ssh_keys: List[Dict[str, str]] = data.get("ssh_keys", [])
        self.created_at: str = data.get("created_at", "")
        self.has_incremental_backups: bool = data.get("has_incremental_backups", False)
        self.vnc_url: str = data.get("vnc_url", "")
        self.compute_resource: ComputeResource = ComputeResource(
            data.get("compute_resource", {})
        )
        self.os_image: OsImage = OsImage(data.get("os_image", {}))
        self.application_login_link: ApplicationLoginLink = ApplicationLoginLink(
            data.get("application_login_link", {})
        )
        self.iso_image: IsoImage = IsoImage(data.get("iso_image", {}))
        self.ip_addresses: Dict[str, List[Ip]] = {
            "ipv4": [
                Ip(ip_data) for ip_data in data.get("ip_addresses", {}).get("ipv4", [])
            ],
            "ipv6": [
                Ip(ip_data) for ip_data in data.get("ip_addresses", {}).get("ipv6", [])
            ],
        }
        self.location: Location = Location(data.get("location", {}))
        self.project: Project = Project(data.get("project", {}))
        self.backup_settings: BackupSettings = BackupSettings(
            data.get("backup_settings", {})
        )
        self.usage: Usage = Usage(data.get("usage", {}))
        self.compute_resource: ComputeResource = ComputeResource(
            data.get("compute_resource", {})
        )

    def get_ip(self) -> str:
        return self.ips[0].ip
