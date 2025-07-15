from typing import Any
from loguru import logger
from aikido.exporters import IssueGroupExporter


async def resync_issue_groups(kind: str) -> list[dict[str, Any]]:
    """Handle resync for Aikido Issue Groups"""
    logger.info(f"🔄 Starting issue group resync for kind: {kind}")

    try:
        exporter = IssueGroupExporter()
        
        issue_groups = await exporter.export()
        logger.info(f"📦 Retrieved {len(issue_groups)} issue groups from Aikido")
        logger.info(
            f"✅ Issue group resync completed successfully. Returning {len(issue_groups)} issue groups"
        )
        return issue_groups
  

    except Exception as e:
        logger.error(f"❌ Error during issue group resync: {str(e)}", exc_info=True)
        raise
