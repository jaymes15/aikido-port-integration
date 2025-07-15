from typing import Any, Dict, List
from aikido.auth import AikidoAuth
from aikido.http.rest_client import RestClient
from logging_config import get_logger
from aikido.kind import ObjectKind

logger = get_logger()


class AikidoIssueGroupExporter:
    """Exporter for Aikido Issue Groups"""

    KIND = ObjectKind.ISSUE_GROUP.value

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
                    "type": group.get("type", ""),
                    "title": group.get("title") or "",  # Convert null to empty string
                    "description": group.get("description") or "",  # Convert null to empty string
                    "severity_score": group.get("severity_score", 0),
                    "severity": group.get("severity", ""),
                    "group_status": group.get("group_status") or "",  # Convert null to empty string
                    "time_to_fix_minutes": group.get("time_to_fix_minutes", 0),  # Convert null to 0
                    "locations": group.get("locations", []),
                    "how_to_fix": group.get("how_to_fix") or "",  # Convert null to empty string
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

