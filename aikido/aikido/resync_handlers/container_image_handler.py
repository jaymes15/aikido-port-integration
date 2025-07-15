from typing import Any
from loguru import logger
from aikido.exporters import ContainerImageExporter


async def resync_container_images(kind: str) -> list[dict[str, Any]]:
    """Handle resync for Aikido Container Images"""
    logger.info(f"🔄 Starting container image resync for kind: {kind}")

    try:
        exporter = ContainerImageExporter()
    
        container_images = await exporter.export()
        logger.info(f"📦 Retrieved {len(container_images)} container images from Aikido")
        logger.info(
            f"✅ Container image resync completed successfully. Returning {len(container_images)} container images"
        )
        return container_images
      

    except Exception as e:
        logger.error(f"❌ Error during container image resync: {str(e)}", exc_info=True)
        raise
