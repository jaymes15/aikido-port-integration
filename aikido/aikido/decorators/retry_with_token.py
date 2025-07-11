from functools import wraps
import httpx


def retry_with_token_refresh(func):
    """Decorator that automatically handles token refresh on 401 errors"""

    @wraps(func)
    async def wrapper(self, *args, **kwargs):
        # First attempt - get current token
        token_response = await self.auth.get_token()
        kwargs["token"] = token_response.access_token

        try:
            response = await func(self, *args, **kwargs)
            response.raise_for_status()
            return response
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 401:
                # Token might be expired, invalidate and retry once
                await self.auth.invalidate_token()
                token_response = await self.auth.get_token()
                kwargs["token"] = token_response.access_token

                # Retry the request
                response = await func(self, *args, **kwargs)
                response.raise_for_status()
                return response
            else:
                # Re-raise non-401 errors
                raise
        except Exception:
            # Re-raise other exceptions
            raise

    return wrapper
