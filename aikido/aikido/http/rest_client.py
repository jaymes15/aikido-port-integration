import os
import httpx
from typing import Optional, Dict, Any, TYPE_CHECKING
from aikido.decorators import retry_with_token_refresh

if TYPE_CHECKING:
    from aikido.auth import AikidoAuth

class RestClient:
    def __init__(self, auth: "AikidoAuth", base_url: Optional[str] = None, timeout: float = 10.0):
        self.auth = auth
        self.base_url = base_url or os.getenv("OCEAN__INTEGRATION__CONFIG__BASE_URL", "https://app.aikido.dev/api/public/v1")
        print("::::::BASE URL::::::", self.base_url)
        self.client = httpx.AsyncClient(base_url=self.base_url, timeout=timeout)
        print("::::::CLIENT CREATED::::::")

    def _build_headers(self, token: str) -> Dict[str, str]:
        headers = {"Accept": "application/json"}
        if token:
            headers["Authorization"] = f"Bearer {token}"
        return headers

    @retry_with_token_refresh
    async def get(self, url: str, params: Optional[Dict[str, Any]] = None, token: Optional[str] = None) -> httpx.Response:
        headers = self._build_headers(token)
        url = f"{self.base_url}{url}"
        print(":::::FULL URL::::::", url)
        
        try:
            response = await self.client.get(url, params=params, headers=headers)
            print(":::::RESPONSE STATUS::::::", response.status_code)
            print(":::::RESPONSE TEXT::::::", response.text[:500])  # First 500 chars
            return response
        except Exception as e:
            print(":::::HTTP ERROR::::::", e)
            raise

    @retry_with_token_refresh
    async def post(self, url: str, json: Optional[Dict[str, Any]] = None, token: Optional[str] = None) -> httpx.Response:
        headers = self._build_headers(token)
        url = f"{self.base_url}{url}"
        return await self.client.post(url, json=json, headers=headers)

    @retry_with_token_refresh
    async def put(self, url: str, json: Optional[Dict[str, Any]] = None, token: Optional[str] = None) -> httpx.Response:
        url = f"{self.base_url}{url}"
        headers = self._build_headers(token)
        return await self.client.put(url, json=json, headers=headers)

    @retry_with_token_refresh
    async def delete(self, url: str, token: Optional[str] = None) -> httpx.Response:
        url = f"{self.base_url}{url}"
        headers = self._build_headers(token)
        return await self.client.delete(url, headers=headers)

    async def close(self):
        """Close the HTTP client"""
        await self.client.aclose()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
