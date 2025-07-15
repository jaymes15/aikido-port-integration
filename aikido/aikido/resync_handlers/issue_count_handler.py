from typing import Any
from loguru import logger
from aikido.exporters import IssueCountExporter


async def resync_issue_counts(kind: str) -> list[dict[str, Any]]:
    """Handle resync for Aikido Issue Counts"""
    logger.info(f"🔄 Starting issue count resync for kind: {kind}")

    try:
        exporter = IssueCountExporter()
   
        issue_counts = await exporter.export()
        logger.info("📊 Retrieved issue count data from Aikido")
        logger.info("✅ Issue count resync completed successfully")
        return issue_counts
        

    except Exception as e:
        logger.error(f"❌ Error during issue count resync: {str(e)}", exc_info=True)
        raise
