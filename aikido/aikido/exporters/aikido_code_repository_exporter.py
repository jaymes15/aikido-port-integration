from typing import Any, Dict, List
from aikido.auth import AikidoAuth
from aikido.http.rest_client import RestClient
from logging_config import get_logger

logger = get_logger()


class AikidoCodeRepositoryExporter:
    KIND = "aikidoCodeRepository"
    """Exporter for Aikido Code Repositories"""

    def __init__(self):
        self.auth = AikidoAuth.get_instance()
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

            # Transform the data to match Port's expected format
            transformed_repos = []
            for repo in code_repositories:
                transformed_repo = {
                    "id": repo.get("id"),
                    "name": repo.get("name"),
                    "external_repo_id": repo.get("external_repo_id"),
                    "provider": repo.get("provider"),
                    "active": repo.get("active"),
                    "url": repo.get("url"),
                    "branch": repo.get("branch"),
                    "last_scanned_at": repo.get("last_scanned_at"),
                }
                logger.debug(
                    f"[{self.__class__.__name__}] kind={self.KIND} Exported repo | id={transformed_repo['id']} name={transformed_repo['name']} provider={transformed_repo['provider']}"
                )
                transformed_repos.append(transformed_repo)
            logger.info(
                f"[{self.__class__.__name__}] kind={self.KIND} Successfully exported {len(transformed_repos)} code repositories"
            )
            return transformed_repos

        except Exception as e:
            logger.error(
                f"[{self.__class__.__name__}] kind={self.KIND} Failed to export code repositories | error={e}",
                exc_info=True,
            )
            return []

    async def close(self):
        """Close the HTTP client"""
        await self.client.close()
