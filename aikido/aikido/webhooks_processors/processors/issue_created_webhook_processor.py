from aikido.kind.object_kind import ObjectKind
from logging_config import get_logger
from aikido.webhooks_processors.processors._aikido_abstract_webhook_processor import BaseWebhookProcessorMixin
from port_ocean.core.handlers.webhook.webhook_event import (
    EventHeaders,
    EventPayload,
    WebhookEvent,
    WebhookEventRawResults,
)
from port_ocean.core.handlers.port_app_config.models import ResourceConfig
from aikido.webhooks_processors.events import Events

logger = get_logger()
WEBHOOK_NAME = "IssueWebhook"

class AikidoIssueCreatedWebhookProcessor(BaseWebhookProcessorMixin):
    async def should_process_event(self, event: WebhookEvent) -> bool:
        logger.info(f"[{WEBHOOK_NAME}] Should process event")
        event_type = event.payload.get("event_type")   
        # Match issue events - be more flexible
        if not event_type:
            logger.warning(f"[{WEBHOOK_NAME}] No event_type found in event")
            return False
        logger.info(f"[{WEBHOOK_NAME}] Event type: {event_type}")
        if event_type != Events.ISSUE_CREATED.value:
            logger.warning(f"[{WEBHOOK_NAME}] Event type: {event_type} is not issue.open.created")
            return False
        logger.info(f"[{WEBHOOK_NAME}] Event type: {event_type} is issue.open.created") 
        return True

    async def get_matching_kinds(self, event: WebhookEvent) -> list[str]:
        kinds = [ObjectKind.ISSUE.value]  
        event_type = event.payload.get("event_type")
        logger.info(f"[{WEBHOOK_NAME}] Matching kinds for event '{event_type}': {kinds}")
        return kinds

    async def validate_payload(self, payload: EventPayload) -> bool:
        # Validate the required keys are present
        issue_data = payload.get("payload", {})
        logger.info(f"[{WEBHOOK_NAME}] Validating payload")
        
        # Check for required fields in the nested payload
        required_fields = {"issue_id", "issue_group_id", "severity_score", "severity", "status", "type"}
        payload_keys = set(issue_data.keys())
        
        missing_fields = required_fields - payload_keys
        if missing_fields:
            logger.warning(f"[{WEBHOOK_NAME}] Payload validation failed. Missing fields: {missing_fields}")
            return False
        
        logger.info(f"[{WEBHOOK_NAME}] Payload validation successful - all required fields present")
        return True

    async def handle_event(
        self, payload: EventPayload, resource_config: ResourceConfig
    ) -> WebhookEventRawResults:
        logger.info(f"[{WEBHOOK_NAME}] Handling event")
        issue_data = payload.get("payload", {})
        issue_id = issue_data.get("issue_id")
        logger.info(f"[{WEBHOOK_NAME}] Processing issue with ID: {issue_id}")

        result = WebhookEventRawResults(
            updated_raw_results=[
                issue_data
            ],
            deleted_raw_results=[]
        )
        
        logger.info(f"[{WEBHOOK_NAME}] Event processing complete. Updated: {len(result.updated_raw_results)}")
        logger.debug(f"[{WEBHOOK_NAME}] Result: {result}")
        
        return result
