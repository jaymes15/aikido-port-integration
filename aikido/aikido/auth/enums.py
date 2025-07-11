from pydantic import BaseModel, Field
from datetime import datetime, timedelta, timezone


class AikidoTokenResponse(BaseModel):
    access_token: str
    token_type: str
    expires_in: int
    expires_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    def with_expiry(self) -> "AikidoTokenResponse":
        self.expires_at = datetime.now(timezone.utc) + timedelta(
            seconds=self.expires_in
        )
        return self

    def is_expired(self) -> bool:
        return datetime.now(timezone.utc) >= self.expires_at
