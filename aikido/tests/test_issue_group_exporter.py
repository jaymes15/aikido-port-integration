import pytest
from unittest.mock import Mock, patch, AsyncMock
from aikido.exporters.issue_group_exporter import IssueGroupExporter


class TestIssueGroupExporter:
    @pytest.mark.asyncio
    async def test_export_success(self, mocker):
        # Mock the dependencies at module level before instantiation
        mock_auth = Mock()
        mock_client = Mock()
        mock_response = Mock()
        
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
                "related_cve_ids": [],
            }
        ]
        mock_response.status_code = 200
        mock_response.raise_for_status.return_value = None
        
        # Make the get method async
        mock_client.get = AsyncMock(return_value=mock_response)
        
        with patch("aikido.exporters.issue_group_exporter.Auth.get_instance", return_value=mock_auth), \
             patch("aikido.exporters.issue_group_exporter.RestClient", return_value=mock_client):
            
            exporter = IssueGroupExporter()
            result = await exporter.export()
        
        assert isinstance(result, list)
        assert len(result) == 1
        assert result[0]["id"] == 10
        assert result[0]["type"] == "vuln"
        assert result[0]["title"] == "Test Group"
        assert result[0]["description"] == "desc"
        assert result[0]["severity_score"] == 8.5
        assert result[0]["severity"] == "high"
        assert result[0]["group_status"] == "open"
        assert result[0]["time_to_fix_minutes"] == 120
        assert result[0]["locations"] == []
        assert result[0]["how_to_fix"] == "fix it"
        assert result[0]["related_cve_ids"] == []
        
        mock_client.get.assert_called_once_with("/issues/export")

    @pytest.mark.asyncio
    async def test_export_failure(self, mocker):
        # Mock the dependencies at module level before instantiation
        mock_auth = Mock()
        mock_client = Mock()
        
        # Make the get method async and raise an exception
        mock_client.get = AsyncMock(side_effect=Exception("API Error"))
        
        with patch("aikido.exporters.issue_group_exporter.Auth.get_instance", return_value=mock_auth), \
             patch("aikido.exporters.issue_group_exporter.RestClient", return_value=mock_client):
            
            exporter = IssueGroupExporter()
            result = await exporter.export()
        
        assert isinstance(result, list)
        assert len(result) == 0  # Should return empty list on error
        mock_client.get.assert_called_once_with("/issues/export")

    @pytest.mark.asyncio
    async def test_export_http_error(self, mocker):
        # Mock the dependencies at module level before instantiation
        mock_auth = Mock()
        mock_client = Mock()
        mock_response = Mock()
        
        mock_response.status_code = 500
        mock_response.raise_for_status.side_effect = Exception("HTTP Error")
        
        # Make the get method async
        mock_client.get = AsyncMock(return_value=mock_response)
        
        with patch("aikido.exporters.issue_group_exporter.Auth.get_instance", return_value=mock_auth), \
             patch("aikido.exporters.issue_group_exporter.RestClient", return_value=mock_client):
            
            exporter = IssueGroupExporter()
            result = await exporter.export()
        
        assert isinstance(result, list)
        assert len(result) == 0  # Should return empty list on HTTP error
        mock_client.get.assert_called_once_with("/issues/export")
