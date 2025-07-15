from typing import Any
from port_ocean.context.ocean import ocean
from aikido.kind import ObjectKind
from aikido.resync_handlers import (
    resync_issues,
    resync_issue_counts,

)
from logging_config import get_logger
from aikido.webhooks.registry import register_webhook_processors


logger = get_logger()

# Initialize the Aikido client
client = None


@ocean.on_resync(ObjectKind.ISSUE_COUNT.value)
async def on_resync_issue_count(kind: str) -> list[dict[str, Any]]:
    """Handle resync events for issue counts"""
    logger.info(f"[main] Resync event received for kind={kind}")
    result = await resync_issue_counts(kind)
    logger.info(f"[main] Resync for kind={kind} returned {len(result)} items.")
    return result


@ocean.on_resync(ObjectKind.ISSUE.value)
async def on_resync_issue(kind: str) -> list[dict[str, Any]]:
    """Handle resync events for issues"""
    logger.info(f"[main] Resync event received for kind={kind}")
    result = await resync_issues(kind)
    logger.info(f"[main] Resync for kind={kind} returned {len(result)} items.")
    return result







# Register webhook processors
register_webhook_processors(path="/webhook") 