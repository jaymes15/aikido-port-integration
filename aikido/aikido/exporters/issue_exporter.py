from typing import Any, Dict, List
from aikido.auth import Auth
from aikido.http.rest_client import RestClient
from logging_config import get_logger
from aikido.kind import ObjectKind

logger = get_logger()


class IssueExporter:
    """Exporter for Aikido Issues"""
    KIND = ObjectKind.ISSUE.value

    def __init__(self):
        self.auth = Auth.get_instance()
        self.client = RestClient(self.auth)

    async def export(self) -> List[Dict[str, Any]]:
        """
        Export all issues from Aikido API

        Returns:
            List of issue dictionaries with the structure expected by Port
        """
        try:
            logger.info(
                f"[{self.__class__.__name__}] kind={self.KIND} Starting export from Aikido API"
            )
            # Fetch issues from Aikido API
            response = await self.client.get("/issues/export")
            logger.info(
                f"[{self.__class__.__name__}] kind={self.KIND} API status={response.status_code}"
            )
            response.raise_for_status()

            issues = response.json()
            logger.info(
                f"[{self.__class__.__name__}] kind={self.KIND} Received {len(issues)} items from API"
            )

            return issues

        except Exception as e:
            logger.error(
                f"[{self.__class__.__name__}] kind={self.KIND} Failed to export issues | error={e}",
                exc_info=True,
            )
            return []









