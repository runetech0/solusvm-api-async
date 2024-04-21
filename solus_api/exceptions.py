class SolusAPIError(Exception):
    """Base exception for the SolusVM API"""


class NotFound(SolusAPIError):
    """When an item is not found. 404"""
