from typing import Any, Dict, List
from aikido.auth import AikidoAuth
from aikido.http.rest_client import RestClient
from logging_config import get_logger

logger = get_logger()


class AikidoIssueGroupExporter:
    KIND = "aikidoIssueGroup"
    """Exporter for Aikido Issue Groups"""

    def __init__(self):
        self.auth = AikidoAuth.get_instance()
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

            # Transform the data to match Port's expected format
            transformed_groups = []
            for group in issue_groups:
                transformed_group = {
                    "id": group.get("id"),
                    "type": group.get("type"),
                    "title": group.get("title"),
                    "description": group.get("description"),
                    "severity_score": group.get("severity_score"),
                    "severity": group.get("severity"),
                    "group_status": group.get("group_status"),
                    "time_to_fix_minutes": group.get("time_to_fix_minutes"),
                    "locations": group.get("locations", []),
                    "how_to_fix": group.get("how_to_fix"),
                    "related_cve_ids": group.get("related_cve_ids", []),
                }
                logger.debug(
                    f"[{self.__class__.__name__}] kind={self.KIND} Exported group | id={transformed_group['id']} title={transformed_group['title']} severity={transformed_group['severity']}"
                )
                transformed_groups.append(transformed_group)
            logger.info(
                f"[{self.__class__.__name__}] kind={self.KIND} Successfully exported {len(transformed_groups)} issue groups"
            )
            return transformed_groups

        except Exception as e:
            logger.error(
                f"[{self.__class__.__name__}] kind={self.KIND} Failed to export issue groups | error={e}",
                exc_info=True,
            )
            return []

    async def close(self):
        """Close the HTTP client"""
        await self.client.close()
