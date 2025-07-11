from typing import Any
from aikido.exporters import AikidoContainerImageExporter


async def resync_container_images(kind: str) -> list[dict[str, Any]]:
    """Handle resync for Aikido Container Images"""
    print(f"🔄 Starting container image resync for kind: {kind}")
    
    try:
        exporter = AikidoContainerImageExporter()
        try:
            container_images = await exporter.export()
            print(f"📦 Retrieved {len(container_images)} container images from Aikido")
            print(f"✅ Container image resync completed successfully. Returning {len(container_images)} container images")
            return container_images
        finally:
            await exporter.close()
            
    except Exception as e:
        print(f"❌ Error during container image resync: {str(e)}")
        raise 