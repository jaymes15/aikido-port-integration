import pytest
from aikido.exporters.aikido_cloud_provider_exporter import AikidoCloudProviderExporter

class TestAikidoCloudProviderExporter:
    @pytest.mark.asyncio
    async def test_export(self, mocker):
        exporter = AikidoCloudProviderExporter()
        mock_response = mocker.Mock()
        mock_response.json.return_value = [
            {
                "id": 1,
                "name": "example-cloud",
                "provider": "aws",
                "environment": "production",
                "external_id": "123456789"
            }
        ]
        mock_response.status_code = 200
        mock_response.raise_for_status.return_value = None
        mocker.patch.object(exporter.client, "get", return_value=mock_response)

        result = await exporter.export()
        assert isinstance(result, list)
        assert len(result) == 1
        assert result[0]["id"] == 1
        assert result[0]["name"] == "example-cloud"
