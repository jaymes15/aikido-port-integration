from typing import Any
from port_ocean.context.ocean import ocean
from aikido.kind import ObjectKind
from aikido.resync_handlers import (
    resync_issue_groups,
    resync_issues,
    resync_issue_counts,
    resync_cloud_providers,
    resync_code_repositories,
    resync_container_images,
)
from logging_config import get_logger
from aikido.webhooks.registry import register_webhook_processors


logger = get_logger()

# Initialize the Aikido client
client = None


@ocean.on_resync(ObjectKind.ISSUE_GROUP.value)
async def on_resync_issue_group(kind: str) -> list[dict[str, Any]]:
    """Handle resync events for issue groups"""
    logger.info(f"[main] Resync event received for kind={kind}")
    result = await resync_issue_groups(kind)
    logger.info(f"[main] Resync for kind={kind} returned {len(result)} items.")
    return result


@ocean.on_resync(ObjectKind.ISSUE_COUNT.value)
async def on_resync_issue_count(kind: str) -> list[dict[str, Any]]:
    """Handle resync events for issue counts"""
    logger.info(f"[main] Resync event received for kind={kind}")
    result = await resync_issue_counts(kind)
    logger.info(f"[main] Resync for kind={kind} returned {len(result)} items.")
    return result


@ocean.on_resync(ObjectKind.CLOUD_PROVIDER.value)
async def on_resync_cloud_provider(kind: str) -> list[dict[str, Any]]:
    """Handle resync events for cloud providers"""
    logger.info(f"[main] Resync event received for kind={kind}")
    result = await resync_cloud_providers(kind)
    logger.info(f"[main] Resync for kind={kind} returned {len(result)} items.")
    return result


@ocean.on_resync(ObjectKind.CODE_REPOSITORY.value)
async def on_resync_code_repository(kind: str) -> list[dict[str, Any]]:
    """Handle resync events for code repositories"""
    logger.info(f"[main] Resync event received for kind={kind}")
    result = await resync_code_repositories(kind)
    logger.info(f"[main] Resync for kind={kind} returned {len(result)} items.")
    return result


@ocean.on_resync(ObjectKind.CONTAINER_IMAGE.value)
async def on_resync_container_image(kind: str) -> list[dict[str, Any]]:
    """Handle resync events for container images"""
    logger.info(f"[main] Resync event received for kind={kind}")
    result = await resync_container_images(kind)
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