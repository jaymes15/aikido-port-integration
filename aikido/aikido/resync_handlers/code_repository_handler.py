from typing import Any
from aikido.exporters import AikidoCodeRepositoryExporter


async def resync_code_repositories(kind: str) -> list[dict[str, Any]]:
    """Handle resync for Aikido Code Repositories"""
    print(f"🔄 Starting code repository resync for kind: {kind}")
    
    try:
        exporter = AikidoCodeRepositoryExporter()
        try:
            code_repositories = await exporter.export()
            print(f"📦 Retrieved {len(code_repositories)} code repositories from Aikido")
            print(f"✅ Code repository resync completed successfully. Returning {len(code_repositories)} code repositories")
            return code_repositories
        finally:
            await exporter.close()
            
    except Exception as e:
        print(f"❌ Error during code repository resync: {str(e)}")
        raise 