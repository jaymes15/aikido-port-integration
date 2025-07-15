from typing import Any, Dict, List
from aikido.auth import Auth
from aikido.http.rest_client import RestClient
from logging_config import get_logger
from aikido.kind import ObjectKind

logger = get_logger()


class CloudProviderExporter:
    """Exporter for Aikido Cloud Providers"""

    KIND = ObjectKind.CLOUD_PROVIDER.value

    def __init__(self):
        self.auth = Auth.get_instance()
        self.client = RestClient(self.auth)

    async def export(self) -> List[Dict[str, Any]]:
        try:
            logger.info(
                f"[{self.__class__.__name__}] kind={self.KIND} Starting export from Aikido API"
            )
            response = await self.client.get("/clouds")
            logger.info(
                f"[{self.__class__.__name__}] kind={self.KIND} API status={response.status_code}"
            )
            response.raise_for_status()
            cloud_providers = response.json()
            logger.info(
                f"[{self.__class__.__name__}] kind={self.KIND} Received {len(cloud_providers)} items from API"
            )
         
            return cloud_providers
        except Exception as e:
            logger.error(
                f"[{self.__class__.__name__}] kind={self.KIND} Failed to export cloud providers | error={e}",
                exc_info=True,
            )
            return []
