from typing import Any, Dict, List
from aikido.auth import Auth
from aikido.http.rest_client import RestClient
from logging_config import get_logger
from aikido.kind import ObjectKind

logger = get_logger()


class IssueGroupExporter:
    """Exporter for Aikido Issue Groups"""

    KIND = ObjectKind.ISSUE_GROUP.value

    def __init__(self):
        self.auth = Auth.get_instance()
        self.client = RestClient(self.auth)

    async def export(self) -> List[Dict[str, Any]]:
        """
        Export all issue groups from Aikido API

        Returns:
            List of issue group dictionaries with the structure expected by Port
        """
        try:
            logger.info(
                f"[{self.__class__.__name__}] kind={self.KIND} Starting export from Aikido API"
            )
            # Fetch issue groups from Aikido API
            response = await self.client.get("/issues/export")

            logger.info(
                f"[{self.__class__.__name__}] kind={self.KIND} API status={response.status_code}"
            )
            response.raise_for_status()

            issue_groups = response.json()
            logger.info(
                f"[{self.__class__.__name__}] kind={self.KIND} Received {len(issue_groups)} items from API"
            )

            return issue_groups

        except Exception as e:
            logger.error(
                f"[{self.__class__.__name__}] kind={self.KIND} Failed to export issue groups | error={e}",
                exc_info=True,
            )
            return []   

