from typing import Any
from loguru import logger
from aikido.exporters import CodeRepositoryExporter


async def resync_code_repositories(kind: str) -> list[dict[str, Any]]:
    """Handle resync for Aikido Code Repositories"""
    logger.info(f"🔄 Starting code repository resync for kind: {kind}")

    try:
        exporter = CodeRepositoryExporter()
   
        code_repositories = await exporter.export()
        logger.info(
                f"📦 Retrieved {len(code_repositories)} code repositories from Aikido"
            )
        logger.info(
                f"✅ Code repository resync completed successfully. Returning {len(code_repositories)} code repositories"
            )
        return code_repositories
  

    except Exception as e:
        logger.error(f"❌ Error during code repository resync: {str(e)}", exc_info=True)
        raise
