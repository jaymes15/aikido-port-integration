from port_ocean.context.ocean import AbstractWebhookProcessor, WebhookEvent, WebhookEventRawResults
from aikido.kind.object_kind import ObjectKind 

class AikidoIssueCountWebhookProcessor(AbstractWebhookProcessor):
    async def should_process_event(self, event: WebhookEvent) -> bool:
        # Check if this event is relevant to issue counts
        return event.payload.get("type") == "issue_count_updated"

    async def get_matching_kinds(self, event: WebhookEvent) -> list[str]:
        return [ObjectKind.AIKIDO_ISSUE_COUNT]

    async def authenticate(self, headers: dict, payload: dict) -> bool:
        # Implement Aikido webhook verification if applicable
        return True  # Stub: allow all for now

    async def validate_payload(self, payload: dict) -> bool:
        # Basic validation to make sure needed fields are present
        return "issue_groups" in payload and "issues" in payload

    async def handle_event(self, event: WebhookEvent) -> WebhookEventRawResults:
       
        issue_count_data = await self.client.get(f"/issues/counts")
        
        return WebhookEventRawResults(
            updated_raw_results=[{
                "identifier": '"aikido-issue-count"',
                "properties": issue_count_data,
                "kind": ObjectKind.AIKIDO_ISSUE_COUNT,
            }],
            deleted_raw_results=[]
        )
