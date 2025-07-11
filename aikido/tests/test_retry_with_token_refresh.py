import pytest
import httpx
from aikido.decorators.retry_with_token import retry_with_token_refresh


class DummyAuth:
    def __init__(self):
        self.token_calls = 0
        self.invalidate_calls = 0

    async def get_token(self):
        self.token_calls += 1

        class Token:
            access_token = f"token{self.token_calls}"

        return Token()

    async def invalidate_token(self):
        self.invalidate_calls += 1


class DummyClient:
    def __init__(self):
        self.auth = DummyAuth()
        self.call_count = 0

    @retry_with_token_refresh
    async def do_request(self, token=None):
        self.call_count += 1
        if self.call_count == 1:
            # Simulate 401 on first call
            response = httpx.Response(401)
            raise httpx.HTTPStatusError(
                "401 Unauthorized", request=None, response=response
            )

        # Success on retry
        class Response:
            def raise_for_status(self):
                return None

        return Response()


class TestRetryWithTokenRefresh:
    @pytest.mark.asyncio
    async def test_retry_on_401_and_refresh(self):
        client = DummyClient()
        await client.do_request()
        assert client.call_count == 2
        assert client.auth.token_calls == 2
        assert client.auth.invalidate_calls == 1
