from typing import Any, Dict, List
from aikido.auth import Auth
from aikido.http.rest_client import RestClient
from logging_config import get_logger
from aikido.kind import ObjectKind

logger = get_logger()


class CodeRepositoryExporter:
    """Exporter for Aikido Code Repositories"""

    KIND = ObjectKind.CODE_REPOSITORY.value

    def __init__(self):
        self.auth = Auth.get_instance()
        self.client = RestClient(self.auth)

    async def export(self) -> List[Dict[str, Any]]:
        """
        Export all code repositories from Aikido API

        Returns:
            List of code repository dictionaries with the structure expected by Port
        """
        try:
            logger.info(
                f"[{self.__class__.__name__}] kind={self.KIND} Starting export from Aikido API"
            )
            # Fetch code repositories from Aikido API
            response = await self.client.get("/repositories/code")
            logger.info(
                f"[{self.__class__.__name__}] kind={self.KIND} API status={response.status_code}"
            )
            response.raise_for_status()

            code_repositories = response.json()
            logger.info(
                f"[{self.__class__.__name__}] kind={self.KIND} Received {len(code_repositories)} items from API"
            )

            return code_repositories

        except Exception as e:
            logger.error(
                f"[{self.__class__.__name__}] kind={self.KIND} Failed to export code repositories | error={e}",
                exc_info=True,
            )
            return []

