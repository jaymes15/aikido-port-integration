import os
from typing import Any
from port_ocean.context.ocean import ocean
from aikido.kind import ObjectKind
from aikido.auth import AikidoAuth
from aikido.resync_handlers import (
    resync_issue_groups,
    resync_issues,
    resync_issue_counts,
    resync_cloud_providers,
    resync_code_repositories,
    resync_container_images
)
from logging_config import get_logger
logger = get_logger()


# Initialize the Aikido client
client = None

@ocean.on_start()
async def on_start():
    """Initialize the Aikido integration"""
    global client
    logger.info("[main] 🚀 Aikido integration starting up...")
    logger.info(f"[main] 🔧 Integration type: {ocean.config.integration.type}")
    logger.info(f"[main] 🆔 Integration identifier: {ocean.config.integration.identifier}")
    logger.info(f"[main] 🌐 Port base URL: {ocean.config.port.base_url}")
    logger.info(f"[main] 📊 Event listener type: {ocean.config.event_listener.type}")
    if hasattr(ocean.config.event_listener, 'interval'):
        logger.info(f"[main] ⏰ Polling interval: {ocean.config.event_listener.interval} seconds")
    AikidoAuth.get_instance()
    logger.info("[main] ✅ Aikido integration started successfully")

@ocean.on_resync()
async def on_resync(kind: str) -> list[dict[str, Any]]:
    """Handle resync events for different Aikido resource kinds"""
    logger.info(f"[main] Resync event received for kind={kind}")
    try:
        if kind == ObjectKind.AIKIDO_ISSUE_GROUP.value:
            logger.info(f"[main] Handling issue groups resync for kind={kind}")
            result = await resync_issue_groups(kind)
            logger.info(f"[main] Resync for kind={kind} returned {len(result)} items.")
            return result
        elif kind == ObjectKind.AIKIDO_ISSUE_COUNT.value:
            logger.info(f"[main] Handling issue counts resync for kind={kind}")
            result = await resync_issue_counts(kind)
            logger.info(f"[main] Resync for kind={kind} returned {len(result)} items.")
            return result
        elif kind == ObjectKind.AIKIDO_CLOUD_PROVIDER.value:
            logger.info(f"[main] Handling cloud providers resync for kind={kind}")
            result = await resync_cloud_providers(kind)
            logger.info(f"[main] Resync for kind={kind} returned {len(result)} items.")
            return result
        elif kind == ObjectKind.AIKIDO_CODE_REPOSITORY.value:
            logger.info(f"[main] Handling code repositories resync for kind={kind}")
            result = await resync_code_repositories(kind)
            logger.info(f"[main] Resync for kind={kind} returned {len(result)} items.")
            return result
        elif kind == ObjectKind.AIKIDO_CONTAINER_IMAGE.value:
            logger.info(f"[main] Handling container images resync for kind={kind}")
            result = await resync_container_images(kind)
            logger.info(f"[main] Resync for kind={kind} returned {len(result)} items.")
            return result
        elif kind == ObjectKind.AIKIDO_ISSUE.value:
            logger.info(f"[main] Handling issues resync for kind={kind}")
            result = await resync_issues(kind)
            logger.info(f"[main] Resync for kind={kind} returned {len(result)} items.")
            return result
        else:
            logger.warning(f"[main] ⚠️ Unsupported kind requested: {kind}")
            logger.warning(f"[main] Available kinds: {ObjectKind.AIKIDO_ISSUE_GROUP.value}, {ObjectKind.AIKIDO_ISSUE_COUNT.value}, {ObjectKind.AIKIDO_ISSUE.value}, {ObjectKind.AIKIDO_CLOUD_PROVIDER.value}, {ObjectKind.AIKIDO_CODE_REPOSITORY.value}, {ObjectKind.AIKIDO_CONTAINER_IMAGE.value}")
            return []
    except Exception as e:
        logger.error(f"[main] Exception during resync for kind={kind}: {e}", exc_info=True)
        return []


