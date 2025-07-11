from enum import StrEnum


class ObjectKind(StrEnum):
    """Enum for Aikido resource kinds."""

    AIKIDO_ISSUE_GROUP = "aikido-issue-group"
    AIKIDO_ISSUE = "aikido-issue"
    AIKIDO_CLOUD_PROVIDER = "aikido-cloud-provider"
    AIKIDO_CODE_REPOSITORY = "aikido-code-repository"
    AIKIDO_CONTAINER_IMAGE = "aikido-container-image"
    AIKIDO_ISSUE_COUNT = "aikido-issue-count"
