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

            # Transform the data to match Port's expected format
            transformed_issues = []
            for issue in issues:
                transformed_issue = {
                    "id": issue.get("id"),
                    "group_id": issue.get("group_id", 0),
                    "attack_surface": issue.get("attack_surface") or "",
                    "status": issue.get("status") or "",
                    "severity": issue.get("severity") or "",
                    "severity_score": issue.get("severity_score", 0),
                    "type": issue.get("type") or "",
                    "affected_package": issue.get("affected_package") or "",
                    "cve_id": issue.get("cve_id") or "",
                    "affected_file": issue.get("affected_file") or "",
                    "first_detected_at": issue.get("first_detected_at", 0),
                    "code_repo_id": issue.get("code_repo_id", 0),
                    "code_repo_name": issue.get("code_repo_name") or "",
                    "container_repo_id": issue.get("container_repo_id", 0),
                    "container_repo_name": issue.get("container_repo_name") or "",
                    "cloud_id": issue.get("cloud_id", 0),
                    "cloud_name": issue.get("cloud_name") or "",
                    "ignored_at": issue.get("ignored_at") or "",
                    "closed_at": issue.get("closed_at") or "",
                    "ignored_by": issue.get("ignored_by") or "",
                    "start_line": issue.get("start_line", 0),
                    "end_line": issue.get("end_line", 0),
                    "snooze_until": issue.get("snooze_until") or "",
                    "cwe_classes": issue.get("cwe_classes", []),
                    "installed_version": issue.get("installed_version") or "",
                    "patched_versions": issue.get("patched_versions", []),
                    "license_type": issue.get("license_type") or "",
                    "programming_language": issue.get("programming_language") or "",
                    "sla_days": issue.get("sla_days", 0),
                    "sla_remediate_by": issue.get("sla_remediate_by") or "",
                }
                logger.debug(
                    f"[{self.__class__.__name__}] kind={self.KIND} Exported issue | id={transformed_issue['id']} group_id={transformed_issue['group_id']} severity={transformed_issue['severity']}"
                )
                transformed_issues.append(transformed_issue)
            logger.info(
                f"[{self.__class__.__name__}] kind={self.KIND} Successfully exported {len(transformed_issues)} issues"
            )
            return transformed_issues

        except Exception as e:
            logger.error(
                f"[{self.__class__.__name__}] kind={self.KIND} Failed to export issues | error={e}",
                exc_info=True,
            )
            # Log the error and return empty list
            return []

