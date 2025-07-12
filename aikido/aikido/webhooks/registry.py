from port_ocean.context.ocean import ocean
from aikido.webhooks.webhook_processors import AikidoIssueCreatedWebhookProcessor
from logging_config import get_logger

logger = get_logger()


def register_webhook_processors(path: str = "/webhook") -> None:
    """
    Register all webhook processors for the given path.
    """
    logger.info(f"Registering webhook processors")
    ocean.add_webhook_processor(path, AikidoIssueCreatedWebhookProcessor)
