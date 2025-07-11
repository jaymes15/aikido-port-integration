from typing import Any
from aikido.exporters import AikidoIssueGroupExporter


async def resync_issue_groups(kind: str) -> list[dict[str, Any]]:
    """Handle resync for Aikido Issue Groups"""
    print(f"🔄 Starting issue group resync for kind: {kind}")

    try:
        exporter = AikidoIssueGroupExporter()
        try:
            issue_groups = await exporter.export()
            print(f"📦 Retrieved {len(issue_groups)} issue groups from Aikido")
            print(
                f"✅ Issue group resync completed successfully. Returning {len(issue_groups)} issue groups"
            )
            return issue_groups
        finally:
            await exporter.close()

    except Exception as e:
        print(f"❌ Error during issue group resync: {str(e)}")
        raise
