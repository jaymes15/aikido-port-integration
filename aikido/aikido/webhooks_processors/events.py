# Aikido webhook events configuration

from enum import StrEnum


class Events(StrEnum):
    """Webhook events."""
    ISSUE_CREATED = "issue.open.created"
