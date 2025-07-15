from typing import Any, Dict, List
from aikido.auth import Auth
from aikido.http.rest_client import RestClient
from logging_config import get_logger
from aikido.kind import ObjectKind

logger = get_logger()


class ContainerImageExporter:
    """Exporter for Aikido Container Images"""
    KIND = ObjectKind.CONTAINER_IMAGE.value

    def __init__(self):
        self.auth = Auth.get_instance()
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

            return container_images

        except Exception as e:
            logger.error(
                f"[{self.__class__.__name__}] kind={self.KIND} Failed to export container images | error={e}",
                exc_info=True,
            )
            return []



