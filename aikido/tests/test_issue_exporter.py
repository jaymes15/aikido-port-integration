import pytest
from aikido.exporters.aikido_issue_exporter import AikidoIssueExporter


class TestAikidoIssueExporter:
    @pytest.mark.asyncio
    async def test_export(self, mocker):
        exporter = AikidoIssueExporter()
        mock_response = mocker.Mock()
        mock_response.json.return_value = [
            {
                "id": 100,
                "group_id": 10,
                "status": "open",
                "severity": "high",
                "type": "vuln",
                "title": "Test Issue",
            }
        ]
        mock_response.status_code = 200
        mock_response.raise_for_status.return_value = None
        mocker.patch.object(exporter.client, "get", return_value=mock_response)

        result = await exporter.export()
        assert isinstance(result, list)
        assert result[0]["id"] == 100
        assert result[0]["group_id"] == 10
