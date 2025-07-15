import asyncio
import httpx
from logging_config import get_logger
from typing import Optional
from port_ocean.context.ocean import ocean
from aikido.auth.enums import AikidoTokenResponse

logger = get_logger()

class AikidoAuth:
    _instance = None
    _lock = asyncio.Lock()

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        
        self.client_id = ocean.integration_config["client_id"]
        self.client_secret = ocean.integration_config["client_secret"]
        self.base_url = ocean.integration_config["base_url"]
        self.token_url = f"{self.base_url}/api/oauth/token"
    
        self._token: Optional[AikidoTokenResponse] = None
        self._token_lock = asyncio.Lock()
        self._initialized = True

    async def get_token(self) -> AikidoTokenResponse:
        """Get a valid token, refreshing if necessary"""
        async with self._token_lock:
            # Return cached token if not expired
            if self._token and not self._token.is_expired():
                return self._token

            # Refresh token
            await self._refresh_token()
            return self._token

    async def _refresh_token(self):
        """Refresh the access token"""
        import base64

        # Create Basic Auth header
        credentials = f"{self.client_id}:{self.client_secret}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()

        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.token_url,
                json={
                    "grant_type": "client_credentials",
                },
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Basic {encoded_credentials}",
                },
            )
            try:
                response.raise_for_status()
                data = response.json()
                self._token = AikidoTokenResponse(**data).with_expiry()
            except Exception as e:
                logger.error(f"Error refreshing token: {e}")
                raise

    async def invalidate_token(self):
        """Invalidate the current token to force refresh"""
        async with self._token_lock:
            self._token = None

    @classmethod
    def get_instance(cls) -> "AikidoAuth":
        """Get the singleton instance"""
        return cls()

    @classmethod
    def reset_instance(cls):
        """Reset the singleton instance (useful for testing)"""
        cls._instance = None
