import pytest
from aikido.exporters.aikido_issue_group_exporter import AikidoIssueGroupExporter

class TestAikidoIssueGroupExporter:
    @pytest.mark.asyncio
    async def test_export(self, mocker):
        exporter = AikidoIssueGroupExporter()
        mock_response = mocker.Mock()
        mock_response.json.return_value = [
            {
                "id": 10,
                "type": "vuln",
                "title": "Test Group",
                "description": "desc",
                "severity_score": 8.5,
                "severity": "high",
                "group_status": "open",
                "time_to_fix_minutes": 120,
                "locations": [],
                "how_to_fix": "fix it",
                "related_cve_ids": []
            }
        ]
        mock_response.status_code = 200
        mock_response.raise_for_status.return_value = None
        mocker.patch.object(exporter.client, "get", return_value=mock_response)

        result = await exporter.export()
        assert isinstance(result, list)
        assert result[0]["id"] == 10
        assert result[0]["title"] == "Test Group" 