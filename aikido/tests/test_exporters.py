import pytest
from unittest.mock import AsyncMock, patch
from aikido.exporters import (
    AikidoIssueGroupExporter,
    AikidoIssueExporter,
    AikidoIssueCountExporter
)


class TestAikidoIssueGroupExporter:
    """Test the AikidoIssueGroupExporter class"""
    
    @pytest.mark.asyncio
    async def test_exporter_initialization(self):
        """Test that the exporter can be initialized"""
        with patch('aikido.exporters.aikido_issue_group_exporter.AikidoAuth.get_instance'):
            with patch('aikido.exporters.aikido_issue_group_exporter.RestClient'):
                exporter = AikidoIssueGroupExporter()
                assert exporter is not None
                assert hasattr(exporter, 'export')
                assert hasattr(exporter, 'close')
    
    @pytest.mark.asyncio
    async def test_export_method_exists(self):
        """Test that the export method exists and is callable"""
        with patch('aikido.exporters.aikido_issue_group_exporter.AikidoAuth.get_instance'):
            with patch('aikido.exporters.aikido_issue_group_exporter.RestClient'):
                exporter = AikidoIssueGroupExporter()
                assert callable(exporter.export)


class TestAikidoIssueExporter:
    """Test the AikidoIssueExporter class"""
    
    @pytest.mark.asyncio
    async def test_exporter_initialization(self):
        """Test that the exporter can be initialized"""
        with patch('aikido.exporters.aikido_issue_exporter.AikidoAuth.get_instance'):
            with patch('aikido.exporters.aikido_issue_exporter.RestClient'):
                exporter = AikidoIssueExporter()
                assert exporter is not None
                assert hasattr(exporter, 'export')
                assert hasattr(exporter, 'close')
    
    @pytest.mark.asyncio
    async def test_export_method_exists(self):
        """Test that the export method exists and is callable"""
        with patch('aikido.exporters.aikido_issue_exporter.AikidoAuth.get_instance'):
            with patch('aikido.exporters.aikido_issue_exporter.RestClient'):
                exporter = AikidoIssueExporter()
                assert callable(exporter.export)


class TestAikidoIssueCountExporter:
    """Test the AikidoIssueCountExporter class"""
    
    @pytest.mark.asyncio
    async def test_exporter_initialization(self):
        """Test that the exporter can be initialized"""
        with patch('aikido.exporters.aikido_issue_count_exporter.AikidoAuth.get_instance'):
            with patch('aikido.exporters.aikido_issue_count_exporter.RestClient'):
                exporter = AikidoIssueCountExporter()
                assert exporter is not None
                assert hasattr(exporter, 'export')
                assert hasattr(exporter, 'close')
    
    @pytest.mark.asyncio
    async def test_export_method_exists(self):
        """Test that the export method exists and is callable"""
        with patch('aikido.exporters.aikido_issue_count_exporter.AikidoAuth.get_instance'):
            with patch('aikido.exporters.aikido_issue_count_exporter.RestClient'):
                exporter = AikidoIssueCountExporter()
                assert callable(exporter.export) 