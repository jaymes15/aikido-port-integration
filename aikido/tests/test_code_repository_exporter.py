import pytest
from aikido.exporters.aikido_code_repository_exporter import (
    AikidoCodeRepositoryExporter,
)


class TestAikidoCodeRepositoryExporter:
    @pytest.mark.asyncio
    async def test_export(self, mocker):
        exporter = AikidoCodeRepositoryExporter()
        mock_response = mocker.Mock()
        mock_response.json.return_value = [
            {
                "id": 300,
                "name": "repo",
                "external_repo_id": "extid",
                "provider": "github",
                "active": True,
                "url": "https://github.com/example/repo",
                "branch": "main",
                "last_scanned_at": 1234567890,
            }
        ]
        mock_response.status_code = 200
        mock_response.raise_for_status.return_value = None
        mocker.patch.object(exporter.client, "get", return_value=mock_response)

        result = await exporter.export()
        assert isinstance(result, list)
        assert result[0]["id"] == 300
        assert result[0]["name"] == "repo"
