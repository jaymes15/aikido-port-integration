from typing import Any
from loguru import logger
from aikido.exporters import AikidoIssueExporter


async def resync_issues(kind: str) -> list[dict[str, Any]]:
    """Handle resync for Aikido Issues"""
    logger.info(f"🔄 Starting issue resync for kind: {kind}")

    try:
        exporter = AikidoIssueExporter()
 
        issues = await exporter.export()
        logger.info(f"📦 Retrieved {len(issues)} issues from Aikido")
        logger.info(
            f"✅ Issue resync completed successfully. Returning {len(issues)} issues"
        )
        return issues


    except Exception as e:
        logger.error(f"❌ Error during issue resync: {str(e)}", exc_info=True)
        raise
