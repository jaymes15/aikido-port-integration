from typing import Any
from loguru import logger
from aikido.exporters import AikidoCloudProviderExporter


async def resync_cloud_providers(kind: str) -> list[dict[str, Any]]:
    """Handle resync for Aikido Cloud Providers"""
    logger.info(f"🔄 Starting cloud provider resync for kind: {kind}")

    try:
        exporter = AikidoCloudProviderExporter()
        try:
            cloud_providers = await exporter.export()
            logger.info(f"📦 Retrieved {len(cloud_providers)} cloud providers from Aikido")
            logger.info(
                f"✅ Cloud provider resync completed successfully. Returning {len(cloud_providers)} cloud providers"
            )
            return cloud_providers
        finally:
            await exporter.close()

    except Exception as e:
        logger.error(f"❌ Error during cloud provider resync: {str(e)}", exc_info=True)
        raise
