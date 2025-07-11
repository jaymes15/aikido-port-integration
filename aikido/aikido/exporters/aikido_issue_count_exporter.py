from typing import Any, Dict, List
from aikido.auth import AikidoAuth
from aikido.http.rest_client import RestClient
from aikido.kind import ObjectKind
from logging_config import get_logger
logger = get_logger()


class AikidoIssueCountExporter:
    KIND = "aikidoIssueCount"
    """Exporter for Aikido Issue Counts"""
    
    def __init__(self):
        self.auth = AikidoAuth.get_instance()
        self.client = RestClient(self.auth)
    
    async def export(self) -> List[Dict[str, Any]]:
        """
        Export issue counts from Aikido API
        
        Returns:
            List containing a single issue count dictionary with the structure expected by Port
        """
        try:
            logger.info(f"[{self.__class__.__name__}] kind={self.KIND} Starting export from Aikido API")
            # Fetch issue counts from Aikido API
            response = await self.client.get("/issues/counts")
            logger.info(f"[{self.__class__.__name__}] kind={self.KIND} API status={response.status_code}")
            response.raise_for_status()
            
            issue_count = response.json()
           
            # Transform the data to match Port's expected format
            # The API might return counts directly or we might need to aggregate them

            transformed_count = {
                    "issue_groups": issue_count.get("issue_groups", {}),
                    "issues": issue_count.get("issues", {})
            }
            logger.debug(f"[{self.__class__.__name__}] kind={self.KIND} Exported count | issue_groups={transformed_count['issue_groups']} issues={transformed_count['issues']}")
            logger.info(f"[{self.__class__.__name__}] kind={self.KIND} Successfully exported issue counts")
            return [transformed_count]
            
        except Exception as e:
            logger.error(f"[{self.__class__.__name__}] kind={self.KIND} Failed to export issue counts | error={e}", exc_info=True)
            # Return mock data for testing
            return []
    
    async def close(self):
        """Close the HTTP client"""
        await self.client.close() 