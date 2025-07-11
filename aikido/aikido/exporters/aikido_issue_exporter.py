from typing import Any, Dict, List
from aikido.auth import AikidoAuth
from aikido.http.rest_client import RestClient
from aikido.kind import ObjectKind
from logging_config import get_logger
logger = get_logger()


class AikidoIssueExporter:
    KIND = "aikidoIssue"
    """Exporter for Aikido Issues"""
    
    def __init__(self):
        self.auth = AikidoAuth.get_instance()
        self.client = RestClient(self.auth)
    
    async def export(self) -> List[Dict[str, Any]]:
        """
        Export all issues from Aikido API
        
        Returns:
            List of issue dictionaries with the structure expected by Port
        """
        try:
            logger.info(f"[{self.__class__.__name__}] kind={self.KIND} Starting export from Aikido API")
            # Fetch issues from Aikido API
            response = await self.client.get("/issues/export")
            logger.info(f"[{self.__class__.__name__}] kind={self.KIND} API status={response.status_code}")
            response.raise_for_status()
            
            issues = response.json()
            logger.info(f"[{self.__class__.__name__}] kind={self.KIND} Received {len(issues)} items from API")
            
            # Transform the data to match Port's expected format
            transformed_issues = []
            for issue in issues:
                transformed_issue = {
                    "id": issue.get("id"),
                    "group_id": issue.get("group_id"),
                    "attack_surface": issue.get("attack_surface"),
                    "status": issue.get("status"),
                    "severity": issue.get("severity"),
                    "severity_score": issue.get("severity_score"),
                    "type": issue.get("type"),
                    "affected_package": issue.get("affected_package"),
                    "cve_id": issue.get("cve_id"),
                    "affected_file": issue.get("affected_file"),
                    "first_detected_at": issue.get("first_detected_at"),
                    "code_repo_id": issue.get("code_repo_id"),
                    "code_repo_name": issue.get("code_repo_name"),
                    "container_repo_id": issue.get("container_repo_id"),
                    "container_repo_name": issue.get("container_repo_name"),
                    "cloud_id": issue.get("cloud_id"),
                    "cloud_name": issue.get("cloud_name"),
                    "ignored_at": issue.get("ignored_at"),
                    "closed_at": issue.get("closed_at"),
                    "ignored_by": issue.get("ignored_by"),
                    "start_line": issue.get("start_line"),
                    "end_line": issue.get("end_line"),
                    "snooze_until": issue.get("snooze_until"),
                    "cwe_classes": issue.get("cwe_classes", []),
                    "installed_version": issue.get("installed_version"),
                    "patched_versions": issue.get("patched_versions", []),
                    "license_type": issue.get("license_type"),
                    "programming_language": issue.get("programming_language"),
                    "sla_days": issue.get("sla_days"),
                    "sla_remediate_by": issue.get("sla_remediate_by")
                }
                logger.debug(f"[{self.__class__.__name__}] kind={self.KIND} Exported issue | id={transformed_issue['id']} group_id={transformed_issue['group_id']} severity={transformed_issue['severity']}")
                transformed_issues.append(transformed_issue)
            logger.info(f"[{self.__class__.__name__}] kind={self.KIND} Successfully exported {len(transformed_issues)} issues")
            return transformed_issues
            
        except Exception as e:
            logger.error(f"[{self.__class__.__name__}] kind={self.KIND} Failed to export issues | error={e}", exc_info=True)
            # Log the error and return empty list
            return []
    
    async def close(self):
        """Close the HTTP client"""
        await self.client.close() 