import os
import httpx
from typing import Optional, Dict, Any, TYPE_CHECKING
from aikido.decorators import retry_with_token_refresh
from logging_config import get_logger

logger = get_logger()

if TYPE_CHECKING:
    from aikido.auth import AikidoAuth


class RestClient:
    def __init__(
        self, auth: "AikidoAuth", base_url: Optional[str] = None, timeout: float = 10.0
    ):
        self.auth = auth
        self.base_url = base_url or os.getenv(
            "OCEAN__INTEGRATION__CONFIG__BASE_URL",
            "https://app.aikido.dev/api/public/v1",
        )
        self.client = httpx.AsyncClient(base_url=self.base_url, timeout=timeout)

    def _build_headers(self, token: str) -> Dict[str, str]:
        headers = {"Accept": "application/json"}
        if token:
            headers["Authorization"] = f"Bearer {token}"
        return headers

    @retry_with_token_refresh
    async def get(
        self,
        url: str,
        params: Optional[Dict[str, Any]] = None,
        token: Optional[str] = None,
    ) -> httpx.Response:
        headers = self._build_headers(token)
        full_url = f"{self.base_url}{url}"
        logger.info(f"[RestClient] GET {full_url}")
        logger.debug(f"[RestClient] GET headers={headers} params={params}")
        try:
            response = await self.client.get(full_url, params=params, headers=headers)
            logger.debug(
                f"[RestClient] GET {full_url} status={response.status_code} body={response.text[:300]}"
            )
            return response
        except Exception as e:
            logger.error(f"[RestClient] GET {full_url} failed: {e}", exc_info=True)
            raise

    @retry_with_token_refresh
    async def post(
        self,
        url: str,
        json: Optional[Dict[str, Any]] = None,
        token: Optional[str] = None,
    ) -> httpx.Response:
        headers = self._build_headers(token)
        full_url = f"{self.base_url}{url}"
        logger.info(f"[RestClient] POST {full_url}")
        logger.debug(f"[RestClient] POST headers={headers} json={json}")
        try:
            response = await self.client.post(full_url, json=json, headers=headers)
            logger.debug(
                f"[RestClient] POST {full_url} status={response.status_code} body={response.text[:300]}"
            )
            return response
        except Exception as e:
            logger.error(f"[RestClient] POST {full_url} failed: {e}", exc_info=True)
            raise

    @retry_with_token_refresh
    async def put(
        self,
        url: str,
        json: Optional[Dict[str, Any]] = None,
        token: Optional[str] = None,
    ) -> httpx.Response:
        headers = self._build_headers(token)
        full_url = f"{self.base_url}{url}"
        logger.info(f"[RestClient] PUT {full_url}")
        logger.debug(f"[RestClient] PUT headers={headers} json={json}")
        try:
            response = await self.client.put(full_url, json=json, headers=headers)
            logger.debug(
                f"[RestClient] PUT {full_url} status={response.status_code} body={response.text[:300]}"
            )
            return response
        except Exception as e:
            logger.error(f"[RestClient] PUT {full_url} failed: {e}", exc_info=True)
            raise

    @retry_with_token_refresh
    async def delete(self, url: str, token: Optional[str] = None) -> httpx.Response:
        headers = self._build_headers(token)
        full_url = f"{self.base_url}{url}"
        logger.info(f"[RestClient] DELETE {full_url}")
        logger.debug(f"[RestClient] DELETE headers={headers}")
        try:
            response = await self.client.delete(full_url, headers=headers)
            logger.debug(
                f"[RestClient] DELETE {full_url} status={response.status_code} body={response.text[:300]}"
            )
            return response
        except Exception as e:
            logger.error(f"[RestClient] DELETE {full_url} failed: {e}", exc_info=True)
            raise

    async def close(self):
        """Close the HTTP client"""
        await self.client.aclose()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
