import pytest
import asyncio
from unittest.mock import AsyncMock, patch
from port_ocean.context.ocean import ocean
from aikido.main import on_start, on_resync
from aikido.kind import ObjectKind


class TestAikidoIntegration:
    """Integration tests for the Aikido integration"""

    @pytest.mark.asyncio
    async def test_on_start_initialization(self):
        """Test that the integration starts up correctly"""
        with patch('aikido.auth.AikidoAuth.get_instance') as mock_auth:
            mock_auth.return_value = AsyncMock()
            
            # Mock ocean config
            with patch.object(ocean.config, 'integration') as mock_integration:
                mock_integration.type = "aikido"
                mock_integration.identifier = "test-aikido"
                
                with patch.object(ocean.config, 'port') as mock_port:
                    mock_port.base_url = "https://test.port.io"
                    
                    with patch.object(ocean.config, 'event_listener') as mock_listener:
                        mock_listener.type = "POLLING"
                        mock_listener.interval = 300
                        
                        # Mock integration config
                        with patch.object(ocean, 'integration_config') as mock_config:
                            mock_config.get.side_effect = lambda key: {
                                "aikidoClientId": "test-client-id",
                                "aikidoClientSecret": "test-client-secret"
                            }.get(key)
                            
                            await on_start()
                            
                            # Verify auth was initialized
                            mock_auth.assert_called_once()

    @pytest.mark.asyncio
    async def test_resync_issue_groups(self):
        """Test resync for issue groups"""
        with patch('aikido.resync_handlers.resync_issue_groups') as mock_resync:
            mock_resync.return_value = [{"id": "1", "title": "Test Group"}]
            
            result = await on_resync(ObjectKind.AIKIDO_ISSUE_GROUP.value)
            
            assert len(result) == 1
            assert result[0]["id"] == "1"
            mock_resync.assert_called_once_with(ObjectKind.AIKIDO_ISSUE_GROUP.value)

    @pytest.mark.asyncio
    async def test_resync_issues(self):
        """Test resync for issues"""
        with patch('aikido.resync_handlers.resync_issues') as mock_resync:
            mock_resync.return_value = [{"id": "1", "type": "vulnerability"}]
            
            result = await on_resync(ObjectKind.AIKIDO_ISSUE.value)
            
            assert len(result) == 1
            assert result[0]["id"] == "1"
            mock_resync.assert_called_once_with(ObjectKind.AIKIDO_ISSUE.value)

    @pytest.mark.asyncio
    async def test_resync_unsupported_kind(self):
        """Test resync for unsupported kind returns empty list"""
        result = await on_resync("unsupported-kind")
        
        assert result == []

    @pytest.mark.asyncio
    async def test_resync_exception_handling(self):
        """Test that exceptions during resync are handled gracefully"""
        with patch('aikido.resync_handlers.resync_issues') as mock_resync:
            mock_resync.side_effect = Exception("API Error")
            
            result = await on_resync(ObjectKind.AIKIDO_ISSUE.value)
            
            assert result == []


class TestWebhookIntegration:
    """Integration tests for webhook functionality"""

    @pytest.mark.asyncio
    async def test_webhook_processor_registration(self):
        """Test that webhook processors are registered correctly"""
        from aikido.webhooks.registry import register_webhook_processors
        
        # This should not raise an exception
        register_webhook_processors(path="/webhook")

    @pytest.mark.asyncio
    async def test_webhook_event_processing(self):
        """Test webhook event processing"""
        from aikido.webhooks.webhook_processors.issue_created_webhook_processor import AikidoIssueCreatedWebhookProcessor
        from port_ocean.core.handlers.webhook.webhook_event import WebhookEvent, EventPayload, EventHeaders
        
        processor = AikidoIssueCreatedWebhookProcessor()
        
        # Test event that should be processed
        event = WebhookEvent(
            payload={
                "event_type": "issue.open.created",
                "payload": {
                    "issue_id": "123",
                    "issue_group_id": "456",
                    "severity_score": 8.5,
                    "severity": "high",
                    "status": "open",
                    "type": "vulnerability"
                }
            },
            headers={},
            raw_body=b""
        )
        
        # Test should_process_event
        should_process = await processor.should_process_event(event)
        assert should_process is True
        
        # Test get_matching_kinds
        kinds = await processor.get_matching_kinds(event)
        assert ObjectKind.AIKIDO_ISSUE.value in kinds
        
        # Test validate_payload
        is_valid = await processor.validate_payload(event.payload)
        assert is_valid is True 