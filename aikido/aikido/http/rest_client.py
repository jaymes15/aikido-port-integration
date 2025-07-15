import asyncio
import httpx
from logging_config import get_logger
from port_ocean.utils import http_async_client
from port_ocean.context.ocean import ocean
from typing import Optional, Any, Dict

logger = get_logger()


class RestClient:
    def __init__(self, auth, base_url: Optional[str] = None, timeout: float = 30.0):
        self.auth = auth
        self.base_url = f"{base_url or ocean.integration_config['base_url']}/api/public/v1"
        self.client = http_async_client
        self.client.timeout = httpx.Timeout(timeout)

    def _build_headers(self, token: str) -> Dict[str, str]:
        """Build headers for the API request"""
        return {
            "Authorization": f"Bearer {token}",
            "Accept": "application/json",
        }

    async def _send_api_request(
        self,
        method: str,
        url: str,
        params: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
        retry_count: int = 0,
        max_retries: int = 3,
    ) -> httpx.Response:
        """Send an API request to the Aikido API"""
        token = await self.auth.get_token()
        headers = self._build_headers(token.access_token)
        full_url = f"{self.base_url}{url}"

        try:
            response = await self.client.request(
                method=method,
                url=full_url,
                headers=headers,
                params=params,
                json=json,
            )

            if response.status_code == 401:
                logger.warning(f"[RestClient] {method} {full_url} → 401. Retrying with fresh token.")
                await self.auth.invalidate_token()
                token = await self.auth.get_token()
                headers = self._build_headers(token.access_token)
                response = await self.client.request(
                    method=method,
                    url=full_url,
                    headers=headers,
                    params=params,
                    json=json,
                )

            elif response.status_code == 429:
                if retry_count >= max_retries:
                    logger.error(f"[RestClient] {method} {full_url} rate limit exceeded after {max_retries} retries.")
                    response.raise_for_status()

                retry_after = int(response.headers.get("Retry-After", "1"))
                logger.warning(f"[RestClient] {method} {full_url} → 429. Retrying in {retry_after} seconds.")
                await asyncio.sleep(retry_after)
                return await self._send_api_request(method, url, params, json, retry_count + 1)

            response.raise_for_status()
            return response

        except httpx.RequestError as e:
            logger.error(f"[RestClient] {method} {full_url} request failed: {e}", exc_info=True)
            raise
        except httpx.HTTPStatusError as e:
            logger.error(f"[RestClient] {method} {full_url} HTTP error: {e}", exc_info=True)
            raise

    async def get(self, url: str, params: Dict[str, Any] = None):
        """Send a GET request to the Aikido API"""
        return await self._send_api_request("GET", url, params=params)

    async def post(self, url: str, json: Dict[str, Any] = None):
        """Send a POST request to the Aikido API"""
        return await self._send_api_request("POST", url, json=json)

    async def put(self, url: str, json: Dict[str, Any] = None):
        """Send a PUT request to the Aikido API"""
        return await self._send_api_request("PUT", url, json=json)

    async def patch(self, url: str, json: Dict[str, Any] = None):
        """Send a PATCH request to the Aikido API"""
        return await self._send_api_request("PATCH", url, json=json)

    async def delete(self, url: str):
        """Send a DELETE request to the Aikido API"""
        return await self._send_api_request("DELETE", url)
