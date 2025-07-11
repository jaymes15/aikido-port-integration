from typing import Any, Dict, List
from aikido.auth import AikidoAuth
from aikido.http.rest_client import RestClient
from logging_config import get_logger

logger = get_logger()


class AikidoCloudProviderExporter:
    """Exporter for Aikido Cloud Providers"""

    KIND = "aikidoCloudProvider"

    def __init__(self):
        self.auth = AikidoAuth.get_instance()
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
            transformed_providers = []
            for provider in cloud_providers:
                transformed_provider = {
                    "id": provider.get("id"),
                    "name": provider.get("name"),
                    "provider": provider.get("provider"),
                    "environment": provider.get("environment"),
                    "external_id": provider.get("external_id"),
                }
                logger.debug(
                    f"[{self.__class__.__name__}] kind={self.KIND} Exported provider | id={transformed_provider['id']} name={transformed_provider['name']} environment={transformed_provider['environment']}"
                )
                transformed_providers.append(transformed_provider)
            logger.info(
                f"[{self.__class__.__name__}] kind={self.KIND} Successfully exported {len(transformed_providers)} cloud providers"
            )
            return transformed_providers
        except Exception as e:
            logger.error(
                f"[{self.__class__.__name__}] kind={self.KIND} Failed to export cloud providers | error={e}",
                exc_info=True,
            )
            return []

    async def close(self):
        await self.client.close()
