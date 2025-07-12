from aikido.kind.object_kind import ObjectKind
from logging_config import get_logger
from port_ocean.core.handlers.webhook.abstract_webhook_processor import AbstractWebhookProcessor
from port_ocean.core.handlers.webhook.webhook_event import (
    EventHeaders,
    EventPayload,
    WebhookEvent,
    WebhookEventRawResults,
)
from port_ocean.core.handlers.port_app_config.models import ResourceConfig


logger = get_logger()
WEBHOOK_NAME = "IssueWebhook"

class AikidoIssueCreatedWebhookProcessor(AbstractWebhookProcessor):
    async def should_process_event(self, event: WebhookEvent) -> bool:
        logger.info(f"[{WEBHOOK_NAME}] Should process event")
        event_type = event.payload.get("event_type")   
        # Match issue events - be more flexible
        if not event_type:
            logger.warning(f"[{WEBHOOK_NAME}] No event_type found in event")
            return False
        logger.info(f"[{WEBHOOK_NAME}] Event type: {event_type}")
        if event_type != "issue.open.created":
            logger.warning(f"[{WEBHOOK_NAME}] Event type: {event_type} is not issue.open.created")
            return False
        logger.info(f"[{WEBHOOK_NAME}] Event type: {event_type} is issue.open.created")
        return True

    async def get_matching_kinds(self, event: WebhookEvent) -> list[str]:
        kinds = [ObjectKind.AIKIDO_ISSUE]  
        event_type = event.payload.get("event_type")
        logger.info(f"[{WEBHOOK_NAME}] Matching kinds for event '{event_type}': {kinds}")
        return kinds
    
    async def authenticate(self, payload: EventPayload, headers: EventHeaders) -> bool:
        return True

    async def validate_payload(self, payload: EventPayload) -> bool:
        # Validate the required keys are present
        issue_data = payload.get("payload", {})
        logger.info(f"[{WEBHOOK_NAME}] Validating payload")
        logger.info(f"[{WEBHOOK_NAME}] Payload keys: {list(payload.keys())}")
        logger.info(f"[{WEBHOOK_NAME}] Issue data keys: {list(issue_data.keys())}")
        
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
        logger.info(f"[{WEBHOOK_NAME}] Event payload: {payload}")

        # Extract the nested payload data
        issue_data = payload.get("payload", {})
        
        # Extract issue_id from the nested payload
        issue_id = issue_data.get("issue_id")
    
        logger.info(f"[{WEBHOOK_NAME}] Processing issue with ID: {issue_id}")

        logger.info(f"[{WEBHOOK_NAME}] Processing upsert event")
        data = {
            "id": issue_id,
            "kind": ObjectKind.AIKIDO_ISSUE.value,
            "severity_score": issue_data.get("severity_score", 0),
            "severity": issue_data.get("severity", "").lower(),
            "status": issue_data.get("status", ""),
        }

        result = WebhookEventRawResults(
            updated_raw_results=[
                data
            ],
            deleted_raw_results=[]
        )
        
        logger.info(f"[{WEBHOOK_NAME}] Event processing complete. Updated: {len(result.updated_raw_results)}")
        logger.debug(f"[{WEBHOOK_NAME}] Result: {result}")
        
        return result
