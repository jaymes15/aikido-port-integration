from enum import StrEnum


class ObjectKind(StrEnum):
    """Enum for Aikido resource kinds."""
    ISSUE = "issue"
    ISSUE_COUNT = "issue-count"
