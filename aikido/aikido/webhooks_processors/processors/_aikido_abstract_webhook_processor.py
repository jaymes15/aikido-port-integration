from logging_config import get_logger
from port_ocean.core.handlers.webhook.abstract_webhook_processor import AbstractWebhookProcessor
from port_ocean.core.handlers.webhook.webhook_event import (
    EventHeaders,
    EventPayload,
)

logger = get_logger()


class BaseWebhookProcessorMixin(AbstractWebhookProcessor):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def authenticate(self, payload: EventPayload, headers: EventHeaders) -> bool:
        logger.info(f"[{self.__class__.__name__}] Authenticating event")
        # TODO: Implement authentication
        return True