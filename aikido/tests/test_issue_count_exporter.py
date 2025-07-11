import pytest
from aikido.exporters.aikido_issue_count_exporter import AikidoIssueCountExporter


class TestAikidoIssueCountExporter:
    @pytest.mark.asyncio
    async def test_export(self, mocker):
        exporter = AikidoIssueCountExporter()
        mock_response = mocker.Mock()
        mock_response.json.return_value = {
            "issue_groups": {
                "critical": 1,
                "high": 2,
                "medium": 3,
                "low": 4,
                "all": 10,
            },
            "issues": {"critical": 5, "high": 6, "medium": 7, "low": 8, "all": 26},
        }
        mock_response.status_code = 200
        mock_response.raise_for_status.return_value = None
        mocker.patch.object(exporter.client, "get", return_value=mock_response)

        result = await exporter.export()
        assert isinstance(result, list)
        assert result[0]["issue_groups"]["critical"] == 1
        assert result[0]["issues"]["all"] == 26
