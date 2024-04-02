import json
from typing import Optional
import aiohttp
from .exceptions import SolusAPIError
from solus_api.models.plan import SolusPlan
from .models.server import Server
from .types import GeneralDict, PlanIDT


class SolusVMAPI:
    def __init__(self, api_key: str, host_url: str, enable_ssl: bool = False) -> None:
        self.access_token = api_key
        self._base_url = host_url + "/api/v1"
        self._session = aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(ssl=enable_ssl)
        )

    def get_headers(self, headers: Optional[GeneralDict] = None) -> GeneralDict:
        if not headers:
            headers = {
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/json",
            }
        return headers

    async def close(self) -> None:
        if not self._session.closed:
            await self._session.close()

    async def _request(
        self,
        method: str,
        path: str,
        data: GeneralDict | str = {},
        headers: Optional[GeneralDict] = None,
        raw: bool = False,
    ) -> GeneralDict | aiohttp.ClientResponse:
        url = self._base_url + path

        data = json.dumps(data)

        async with self._session.request(
            method=method, url=url, headers=self.get_headers(headers), data=data
        ) as resp:
            await resp.read()
            # print(resp.status)

        if raw:
            return resp

        if resp.status not in range(200, 299):
            raise SolusAPIError(f"API Response: {await resp.text()}")

        return await resp.json()

    async def verify_token(self) -> bool:
        path = "/auth"
        resp = await self._request("GET", path, raw=True)
        assert isinstance(resp, aiohttp.ClientResponse)
        return resp.status == 204

    async def get_plans(self) -> list[SolusPlan]:
        path = "/plans"
        resp = await self._request("GET", path)
        assert isinstance(resp, dict)
        plans: list[SolusPlan] = []
        for d in resp["data"]:
            plans.append(SolusPlan(d))

        return plans

    async def get_plan(self, plan_id: PlanIDT) -> SolusPlan:
        path = f"/plans/{plan_id}"
        resp = await self._request("GET", path)
        assert isinstance(resp, dict)

        return SolusPlan(resp["data"])

    async def create_server(
        self,
        hostname: str,
        plan_id: PlanIDT,
        os_id: int,
        location_id: Optional[int] = None,
    ) -> Server:
        path = "/servers"
        payload = {
            "name": hostname,
            "plan": plan_id,
            "os": os_id,
            # "ip_types": ["IPv4"],
            # "primary_ip": primary_ip,
            "compute_resource": 2,
        }
        if location_id:
            payload.update({"location": location_id})
        resp = await self._request("POST", path=path, data=payload)

        assert isinstance(resp, dict)

        return Server(resp["data"])

    async def retrieve_server(self, server_id: int) -> Server:

        path = f"/servers/{server_id}"
        resp = await self._request("GET", path=path)

        assert isinstance(resp, dict)

        return Server(resp["data"])

    async def reinstall_server(
        self,
        server_id: int,
        os_id: int,
        application_data: list[str] = [],
    ) -> Server:
        """Reinstall a server with different os or application"""
        path = f"/servers/{server_id}/reinstall"
        payload = {
            "os": os_id,
            "application_data": application_data,
        }
        resp = await self._request("POST", path=path, data=payload)
        assert isinstance(resp, dict)
        return Server(resp["data"])

    async def restart_server(self, server_id: int, force: bool = True) -> GeneralDict:
        """Restart a server"""
        path = f"/servers/{server_id}/restart"
        payload = {"force": force}
        resp = await self._request("POST", path=path, data=payload)
        assert isinstance(resp, dict)
        return resp

    async def stop_server(self, server_id: int, force: bool = True) -> GeneralDict:
        """Stops a server"""
        path = f"/servers/{server_id}/stop"
        payload = {"force": force}
        resp = await self._request("POST", path=path, data=payload)
        assert isinstance(resp, dict)
        return resp

    async def start_server(self, server_id: int, force: bool = True) -> GeneralDict:
        """Start a server"""
        path = f"/servers/{server_id}/start"
        payload = {"force": force}
        resp = await self._request("POST", path=path, data=payload)
        assert isinstance(resp, dict)
        return resp

    async def suspend_server(self, server_id: int) -> GeneralDict:
        """Suspend a server"""
        path = f"/servers/{server_id}/suspend"
        resp = await self._request("POST", path=path)
        assert isinstance(resp, dict)
        return resp

    async def resume_server(self, server_id: int) -> GeneralDict:
        """Resume a stopped/suspended server"""
        path = f"/servers/{server_id}/resume"
        resp = await self._request("POST", path=path)
        assert isinstance(resp, dict)
        return resp

    async def reset_root_password(self, server_id: int) -> bool:
        path = f"/servers/{server_id}/reset_password"
        payload = {"send_password_to_current_user": True}

        resp = await self._request("POST", path=path, data=payload, raw=True)

        assert isinstance(resp, aiohttp.ClientResponse)
        return resp.status == 200
