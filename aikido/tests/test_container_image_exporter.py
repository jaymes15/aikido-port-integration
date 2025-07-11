import pytest
from aikido.exporters.aikido_container_image_exporter import (
    AikidoContainerImageExporter,
)


class TestAikidoContainerImageExporter:
    @pytest.mark.asyncio
    async def test_export(self, mocker):
        exporter = AikidoContainerImageExporter()
        mock_response = mocker.Mock()
        mock_response.json.return_value = [
            {
                "id": 200,
                "name": "nginx",
                "provider": "docker-hub",
                "registry_name": None,
                "tag": "latest",
                "last_scanned_at": 1234567890,
                "last_scanned_tag": "latest",
            }
        ]
        mock_response.status_code = 200
        mock_response.raise_for_status.return_value = None
        mocker.patch.object(exporter.client, "get", return_value=mock_response)

        result = await exporter.export()
        assert isinstance(result, list)
        assert result[0]["id"] == 200
        assert result[0]["name"] == "nginx"
