from typing import Any
from aikido.exporters import AikidoIssueExporter


async def resync_issues(kind: str) -> list[dict[str, Any]]:
    """Handle resync for Aikido Issues"""
    print(f"🔄 Starting issue resync for kind: {kind}")
    
    try:
        exporter = AikidoIssueExporter()
        try:
            issues = await exporter.export()
            print(f"📦 Retrieved {len(issues)} issues from Aikido")
            print(f"✅ Issue resync completed successfully. Returning {len(issues)} issues")
            return issues
        finally:
            await exporter.close()
            
    except Exception as e:
        print(f"❌ Error during issue resync: {str(e)}")
        raise 