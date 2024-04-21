import json
from typing import Optional
import aiohttp

from .models.resouce import ComputeResource

# from .utils import dump_json
from .exceptions import NotFound, SolusAPIError
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
    ) -> aiohttp.ClientResponse:
        url = self._base_url + path

        data = json.dumps(data)

        async with self._session.request(
            method=method, url=url, headers=self.get_headers(headers), data=data
        ) as resp:
            await resp.read()

        await self._raise_exception(resp)

        if resp.status not in range(200, 299):
            raise SolusAPIError(f"API Response: {await resp.text()}")

        return resp

    async def _raise_exception(self, resp: aiohttp.ClientResponse) -> None:
        if resp.status in range(200, 299):
            return
        if resp.status == 404:
            raise NotFound(
                f"Status: {resp.status} | Reason: {resp.reason} | Response: {await resp.text()}"
            )

    async def _parse_resp_data(self, resp: aiohttp.ClientResponse) -> GeneralDict:
        return await resp.json()

    async def verify_token(self) -> bool:
        path = "/auth"
        resp = await self._request("GET", path)
        return resp.status == 204

    async def get_plans(self) -> list[SolusPlan]:
        path = "/plans"
        resp = await self._request("GET", path)
        rjs = await self._parse_resp_data(resp)
        plans: list[SolusPlan] = []
        for d in rjs["data"]:
            plans.append(SolusPlan(d))

        return plans

    async def get_plan(self, plan_id: PlanIDT) -> SolusPlan:
        path = f"/plans/{plan_id}"
        resp = await self._request("GET", path)
        rjs = await self._parse_resp_data(resp)

        return SolusPlan(rjs["data"])

    async def create_server(
        self,
        hostname: str,
        password: str,
        plan_id: PlanIDT,
        os_id: int,
        location_id: Optional[int] = None,
    ) -> Server:
        path = "/servers"
        payload = {
            "name": hostname,
            "plan": plan_id,
            "os": os_id,
            "password": password,
        }
        if location_id:
            payload.update({"location": location_id})

        resp = await self._request("POST", path=path, data=payload)
        rjs = await self._parse_resp_data(resp)

        return Server(rjs["data"])

    async def retrieve_server(self, server_id: int) -> Server:

        path = f"/servers/{server_id}"
        resp = await self._request("GET", path=path)

        rjs = await self._parse_resp_data(resp)

        return Server(rjs["data"])

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
        rjs = await self._parse_resp_data(resp)
        return Server(rjs["data"])

    async def restart_server(self, server_id: int, force: bool = True) -> GeneralDict:
        """Restart a server"""
        path = f"/servers/{server_id}/restart"
        payload = {"force": force}
        resp = await self._request("POST", path=path, data=payload)
        return await self._parse_resp_data(resp)

    async def stop_server(self, server_id: int, force: bool = True) -> GeneralDict:
        """Stops a server"""
        path = f"/servers/{server_id}/stop"
        payload = {"force": force}
        resp = await self._request("POST", path=path, data=payload)
        return await self._parse_resp_data(resp)

    async def start_server(self, server_id: int, force: bool = True) -> GeneralDict:
        """Start a server"""
        path = f"/servers/{server_id}/start"
        payload = {"force": force}
        resp = await self._request("POST", path=path, data=payload)
        return await self._parse_resp_data(resp)

    async def suspend_server(self, server_id: int) -> GeneralDict:
        """Suspend a server"""
        path = f"/servers/{server_id}/suspend"
        resp = await self._request("POST", path=path)
        return await self._parse_resp_data(resp)

    async def resume_server(self, server_id: int) -> GeneralDict:
        """Resume a stopped/suspended server"""
        path = f"/servers/{server_id}/resume"
        resp = await self._request("POST", path=path)
        return await self._parse_resp_data(resp)

    async def delete_server(self, server_id: int) -> GeneralDict:
        path = f"/servers/{server_id}"
        resp = await self._request("DELETE", path=path)
        return await self._parse_resp_data(resp)

    async def reset_root_password(self, server_id: int) -> bool:
        path = f"/servers/{server_id}/reset_password"
        payload = {"send_password_to_current_user": True}

        resp = await self._request("POST", path=path, data=payload)

        return resp.status == 200

    # Compute resources
    async def list_all_compute_resources(self) -> list[ComputeResource]:
        path = "/compute_resources"
        resp = await self._request("GET", path=path)
        rjs = await self._parse_resp_data(resp)

        ress: list[ComputeResource] = []
        for res in rjs["data"]:
            ress.append(ComputeResource(res))

        return ress

    async def retrieve_compute_resource(self, resource_id: int) -> ComputeResource:
        path = f"/compute_resources/{resource_id}"
        resp = await self._request("GET", path=path)
        rjs = await self._parse_resp_data(resp)
        return ComputeResource(rjs["data"])

    async def retrieve_compute_resouces_usage(self, resource_id: int) -> GeneralDict:
        path = f"/compute_resources/{resource_id}/usage"
        resp = await self._request("GET", path=path)
        rjs = await self._parse_resp_data(resp)
        return rjs

    async def create_server_under_compute_resource(
        self,
        resource_id: int,
        name: str,
        password: str,
        plan_id: int,
        os_image_version_id: int,
        user_id: int = 1,
        project_id: int = 1,
    ) -> Server:
        path = f"/compute_resources/{resource_id}/servers"
        resp = await self._request(
            "POST",
            path=path,
            data={
                "name": name,
                "password": password,
                "plan_id": plan_id,
                "os_image_version_id": os_image_version_id,
                "user_id": user_id,
                "project_id": project_id,
            },
        )
        rjs = await self._parse_resp_data(resp)
        return Server(rjs["data"])

    async def list_all_users(self) -> GeneralDict:
        path = "/users"
        resp = await self._request("GET", path=path)
        rjs = await self._parse_resp_data(resp)
        return rjs

    async def list_all_projects(self) -> GeneralDict:
        path = "/projects"
        resp = await self._request("GET", path=path)
        rjs = await self._parse_resp_data(resp)
        return rjs
