from port_ocean.context.ocean import ocean
from aikido.webhooks.webhook_processors.issue_count_webhook_processor import AikidoIssueCountWebhookProcessor


def register_webhook_processors(path: str ="/webhook")->None:
    """
    Register webhook processors for the given path.
    """
    ocean.add_webhook_processor(path, AikidoIssueCountWebhookProcessor)