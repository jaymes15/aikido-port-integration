from enum import StrEnum


class ObjectKind(StrEnum):
    """Enum for Aikido resource kinds."""

    ISSUE_GROUP = "issue-group"
    ISSUE = "issue"
    CLOUD_PROVIDER = "cloud-provider"
    CODE_REPOSITORY = "code-repository"
    CONTAINER_IMAGE = "container-image"
    ISSUE_COUNT = "issue-count"
