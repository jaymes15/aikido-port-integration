import pytest
from unittest.mock import Mock, patch, AsyncMock
from aikido.exporters.issue_count_exporter import IssueCountExporter


class TestIssueCountExporter:
    @pytest.mark.asyncio
    async def test_export_success(self, mocker):
        # Mock the dependencies at module level before instantiation
        mock_auth = Mock()
        mock_client = Mock()
        mock_response = Mock()
        
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
        
        # Make the get method async
        mock_client.get = AsyncMock(return_value=mock_response)
        
        with patch("aikido.exporters.issue_count_exporter.Auth.get_instance", return_value=mock_auth), \
             patch("aikido.exporters.issue_count_exporter.RestClient", return_value=mock_client):
            
            exporter = IssueCountExporter()
            result = await exporter.export()
        
        assert isinstance(result, list)
        assert len(result) == 1
        assert result[0]["issue_groups"]["critical"] == 1
        assert result[0]["issue_groups"]["high"] == 2
        assert result[0]["issue_groups"]["medium"] == 3
        assert result[0]["issue_groups"]["low"] == 4
        assert result[0]["issue_groups"]["all"] == 10
        assert result[0]["issues"]["critical"] == 5
        assert result[0]["issues"]["high"] == 6
        assert result[0]["issues"]["medium"] == 7
        assert result[0]["issues"]["low"] == 8
        assert result[0]["issues"]["all"] == 26
        
        mock_client.get.assert_called_once_with("/issues/counts")

    @pytest.mark.asyncio
    async def test_export_failure(self, mocker):
        # Mock the dependencies at module level before instantiation
        mock_auth = Mock()
        mock_client = Mock()
        
        # Make the get method async and raise an exception
        mock_client.get = AsyncMock(side_effect=Exception("API Error"))
        
        with patch("aikido.exporters.issue_count_exporter.Auth.get_instance", return_value=mock_auth), \
             patch("aikido.exporters.issue_count_exporter.RestClient", return_value=mock_client):
            
            exporter = IssueCountExporter()
            result = await exporter.export()
        
        assert isinstance(result, list)
        assert len(result) == 0  # Should return empty list on error
        mock_client.get.assert_called_once_with("/issues/counts")

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
        
        with patch("aikido.exporters.issue_count_exporter.Auth.get_instance", return_value=mock_auth), \
             patch("aikido.exporters.issue_count_exporter.RestClient", return_value=mock_client):
            
            exporter = IssueCountExporter()
            result = await exporter.export()
        
        assert isinstance(result, list)
        assert len(result) == 0  # Should return empty list on HTTP error
        mock_client.get.assert_called_once_with("/issues/counts")
