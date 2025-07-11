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


# Initialize the Aikido client
client = None

@ocean.on_start()
async def on_start():
    """Initialize the Aikido integration"""
    global client
    
    print("🚀 Aikido integration starting up...")
    print(f"🔧 Integration type: {ocean.config.integration.type}")
    print(f"🆔 Integration identifier: {ocean.config.integration.identifier}")
    print(f"🌐 Port base URL: {ocean.config.port.base_url}")
    print(f"📊 Event listener type: {ocean.config.event_listener.type}")
    
    # Log configuration details
    if hasattr(ocean.config.event_listener, 'interval'):
        print(f"⏰ Polling interval: {ocean.config.event_listener.interval} seconds")
    
    # Initialize authentication
    AikidoAuth.get_instance()
    print("✅ Aikido integration started successfully")

@ocean.on_resync()
async def on_resync(kind: str) -> list[dict[str, Any]]:
    """Handle resync events for different Aikido resource kinds"""
    
    if kind == ObjectKind.AIKIDO_ISSUE_GROUP.value:
        print(f"🔄 Handling issue groups resync")
        return await resync_issue_groups(kind)
    
    elif kind == ObjectKind.AIKIDO_ISSUE.value:
        print(f"🔄 Handling issues resync")
        return await resync_issues(kind)
    
    elif kind == ObjectKind.AIKIDO_ISSUE_COUNT.value:
        print(f"🔄 Handling issue counts resync")
        return await resync_issue_counts(kind)
    
    elif kind == ObjectKind.AIKIDO_CLOUD_PROVIDER.value:
        print(f"🔄 Handling cloud providers resync")
        return await resync_cloud_providers(kind)
    
    elif kind == ObjectKind.AIKIDO_CODE_REPOSITORY.value:
        print(f"🔄 Handling code repositories resync")
        return await resync_code_repositories(kind)
    
    elif kind == ObjectKind.AIKIDO_CONTAINER_IMAGE.value:
        print(f"🔄 Handling container images resync")
        return await resync_container_images(kind)
    
    else:
        print(f"⚠️ Unsupported kind requested: {kind}")
        print(f"Available kinds: {ObjectKind.AIKIDO_ISSUE_GROUP.value}, {ObjectKind.AIKIDO_ISSUE.value}, {ObjectKind.AIKIDO_ISSUE_COUNT.value}, {ObjectKind.AIKIDO_CLOUD_PROVIDER.value}, {ObjectKind.AIKIDO_CODE_REPOSITORY.value}, {ObjectKind.AIKIDO_CONTAINER_IMAGE.value}")
        return []


