from typing import Any
from aikido.exporters import AikidoIssueCountExporter


async def resync_issue_counts(kind: str) -> list[dict[str, Any]]:
    """Handle resync for Aikido Issue Counts"""
    print(f"🔄 Starting issue count resync for kind: {kind}")

    try:
        exporter = AikidoIssueCountExporter()
        try:
            issue_counts = await exporter.export()
            print("📊 Retrieved issue count data from Aikido")
            print("✅ Issue count resync completed successfully")
            return issue_counts
        finally:
            await exporter.close()

    except Exception as e:
        print(f"❌ Error during issue count resync: {str(e)}")
        raise
