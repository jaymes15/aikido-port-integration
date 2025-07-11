from typing import Any
from aikido.exporters import AikidoCloudProviderExporter


async def resync_cloud_providers(kind: str) -> list[dict[str, Any]]:
    """Handle resync for Aikido Cloud Providers"""
    print(f"🔄 Starting cloud provider resync for kind: {kind}")

    try:
        exporter = AikidoCloudProviderExporter()
        try:
            cloud_providers = await exporter.export()
            print(f"📦 Retrieved {len(cloud_providers)} cloud providers from Aikido")
            print(
                f"✅ Cloud provider resync completed successfully. Returning {len(cloud_providers)} cloud providers"
            )
            return cloud_providers
        finally:
            await exporter.close()

    except Exception as e:
        print(f"❌ Error during cloud provider resync: {str(e)}")
        raise
