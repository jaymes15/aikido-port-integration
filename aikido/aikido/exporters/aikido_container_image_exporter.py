from typing import Any, Dict, List
from aikido.auth import AikidoAuth
from aikido.http.rest_client import RestClient
from logging_config import get_logger

logger = get_logger()


class AikidoContainerImageExporter:
    KIND = "aikidoContainerImage"
    """Exporter for Aikido Container Images"""

    def __init__(self):
        self.auth = AikidoAuth.get_instance()
        self.client = RestClient(self.auth)

    async def export(self) -> List[Dict[str, Any]]:
        """
        Export all container images from Aikido API

        Returns:
            List of container image dictionaries with the structure expected by Port
        """
        try:
            logger.info(
                f"[{self.__class__.__name__}] kind={self.KIND} Starting export from Aikido API"
            )
            # Fetch container images from Aikido API
            response = await self.client.get("/containers")
            logger.info(
                f"[{self.__class__.__name__}] kind={self.KIND} API status={response.status_code}"
            )
            response.raise_for_status()

            container_images = response.json()
            logger.info(
                f"[{self.__class__.__name__}] kind={self.KIND} Received {len(container_images)} items from API"
            )

            # Transform the data to match Port's expected format
            transformed_images = []
            for image in container_images:
                transformed_image = {
                    "id": image.get("id"),
                    "name": image.get("name"),
                    "provider": image.get("provider"),
                    "registry_name": image.get("registry_name"),
                    "tag": image.get("tag"),
                    "last_scanned_at": image.get("last_scanned_at"),
                    "last_scanned_tag": image.get("last_scanned_tag"),
                }
                logger.debug(
                    f"[{self.__class__.__name__}] kind={self.KIND} Exported image | id={transformed_image['id']} name={transformed_image['name']} tag={transformed_image['tag']}"
                )
                transformed_images.append(transformed_image)
            logger.info(
                f"[{self.__class__.__name__}] kind={self.KIND} Successfully exported {len(transformed_images)} container images"
            )
            return transformed_images

        except Exception as e:
            logger.error(
                f"[{self.__class__.__name__}] kind={self.KIND} Failed to export container images | error={e}",
                exc_info=True,
            )
            # Return mock data for testing
            return []

    async def close(self):
        """Close the HTTP client"""
        await self.client.close()
