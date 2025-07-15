from typing import Any, Dict, List
from aikido.auth import Auth
from aikido.http.rest_client import RestClient
from logging_config import get_logger
from aikido.kind import ObjectKind

logger = get_logger()


class IssueCountExporter:
    """Exporter for Aikido Issue Counts"""
    KIND = ObjectKind.ISSUE_COUNT.value

    def __init__(self):
        self.auth = Auth.get_instance()
        self.client = RestClient(self.auth)

    async def export(self) -> List[Dict[str, Any]]:
        """
        Export issue counts from Aikido API

        Returns:
            List containing a single issue count dictionary with the structure expected by Port
        """
        try:
            logger.info(
                f"[{self.__class__.__name__}] kind={self.KIND} Starting export from Aikido API"
            )
            # Fetch issue counts from Aikido API
            response = await self.client.get("/issues/counts")
            logger.info(
                f"[{self.__class__.__name__}] kind={self.KIND} API status={response.status_code}"
            )
            response.raise_for_status()

            issue_count = response.json()

            return [issue_count]

        except Exception as e:
            logger.error(
                f"[{self.__class__.__name__}] kind={self.KIND} Failed to export issue counts | error={e}",
                exc_info=True,
            )
            # Return mock data for testing
            return []


