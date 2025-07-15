import pytest
import httpx
from unittest.mock import Mock
from aikido.http.rest_client import RestClient


class DummyAuth:
    async def get_token(self):
        class Token:
            access_token = "dummy-token"

        return Token()
    
    async def invalidate_token(self):
        pass


@pytest.fixture
def mock_http_client(mocker):
    """Mock the http_async_client to avoid PortOcean context issues"""
    mock_client = Mock(spec=httpx.AsyncClient)
    mocker.patch("aikido.http.rest_client.http_async_client", mock_client)
    return mock_client


@pytest.fixture
def mock_ocean(mocker):
    """Mock the ocean context to avoid initialization issues"""
    mock_ocean = Mock()
    mock_ocean.integration_config = {"base_url": "https://api.example.com"}
    mocker.patch("aikido.http.rest_client.ocean", mock_ocean)
    return mock_ocean


@pytest.mark.asyncio
async def test_rest_client_get(mocker, mock_http_client, mock_ocean):
    auth = DummyAuth()
    rest_client = RestClient(auth, base_url="https://api.example.com")
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.text = '{"ok": true}'
    mock_response.raise_for_status.return_value = None

    mock_http_client.request.return_value = mock_response

    response = await rest_client.get("/test-get", params={"foo": "bar"})
    mock_http_client.request.assert_called_once_with(
        method="GET",
        url="https://api.example.com/api/public/v1/test-get",
        headers={"Accept": "application/json", "Authorization": "Bearer dummy-token"},
        params={"foo": "bar"},
        json=None,
    )
    assert response.status_code == 200
    assert response.text == '{"ok": true}'


@pytest.mark.asyncio
async def test_rest_client_post(mocker, mock_http_client, mock_ocean):
    auth = DummyAuth()
    rest_client = RestClient(auth, base_url="https://api.example.com")
    mock_response = mocker.Mock()
    mock_response.status_code = 201
    mock_response.text = '{"created": true}'
    mock_response.raise_for_status.return_value = None

    mock_http_client.request.return_value = mock_response

    response = await rest_client.post("/test-post", json={"foo": "bar"})
    mock_http_client.request.assert_called_once_with(
        method="POST",
        url="https://api.example.com/api/public/v1/test-post",
        headers={"Accept": "application/json", "Authorization": "Bearer dummy-token"},
        params=None,
        json={"foo": "bar"},
    )
    assert response.status_code == 201
    assert response.text == '{"created": true}'


@pytest.mark.asyncio
async def test_rest_client_put(mocker, mock_http_client, mock_ocean):
    auth = DummyAuth()
    rest_client = RestClient(auth, base_url="https://api.example.com")
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.text = '{"updated": true}'
    mock_response.raise_for_status.return_value = None

    mock_http_client.request.return_value = mock_response

    response = await rest_client.put("/test-put", json={"foo": "baz"})
    mock_http_client.request.assert_called_once_with(
        method="PUT",
        url="https://api.example.com/api/public/v1/test-put",
        headers={"Accept": "application/json", "Authorization": "Bearer dummy-token"},
        params=None,
        json={"foo": "baz"},
    )
    assert response.status_code == 200
    assert response.text == '{"updated": true}'


@pytest.mark.asyncio
async def test_rest_client_patch(mocker, mock_http_client, mock_ocean):
    auth = DummyAuth()
    rest_client = RestClient(auth, base_url="https://api.example.com")
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.text = '{"patched": true}'
    mock_response.raise_for_status.return_value = None

    mock_http_client.request.return_value = mock_response

    response = await rest_client.patch("/test-patch", json={"foo": "updated"})
    mock_http_client.request.assert_called_once_with(
        method="PATCH",
        url="https://api.example.com/api/public/v1/test-patch",
        headers={"Accept": "application/json", "Authorization": "Bearer dummy-token"},
        params=None,
        json={"foo": "updated"},
    )
    assert response.status_code == 200
    assert response.text == '{"patched": true}'


@pytest.mark.asyncio
async def test_rest_client_delete(mocker, mock_http_client, mock_ocean):
    auth = DummyAuth()
    rest_client = RestClient(auth, base_url="https://api.example.com")
    mock_response = mocker.Mock()
    mock_response.status_code = 204
    mock_response.text = ""
    mock_response.raise_for_status.return_value = None

    mock_http_client.request.return_value = mock_response

    response = await rest_client.delete("/test-delete")
    mock_http_client.request.assert_called_once_with(
        method="DELETE",
        url="https://api.example.com/api/public/v1/test-delete",
        headers={"Accept": "application/json", "Authorization": "Bearer dummy-token"},
        params=None,
        json=None,
    )
    assert response.status_code == 204
    assert response.text == ""


@pytest.mark.asyncio
async def test_rest_client_401_retry(mocker, mock_http_client, mock_ocean):
    auth = DummyAuth()
    rest_client = RestClient(auth, base_url="https://api.example.com")
    
    # First call returns 401, second call succeeds
    mock_response_401 = mocker.Mock()
    mock_response_401.status_code = 401
    
    mock_response_success = mocker.Mock()
    mock_response_success.status_code = 200
    mock_response_success.text = '{"ok": true}'
    mock_response_success.raise_for_status.return_value = None

    mock_http_client.request.side_effect = [mock_response_401, mock_response_success]
    mocker.patch.object(auth, "invalidate_token")

    response = await rest_client.get("/test-get")
    
    # Should have called request twice
    assert mock_http_client.request.call_count == 2
    auth.invalidate_token.assert_called_once()
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_rest_client_429_retry(mocker, mock_http_client, mock_ocean):
    auth = DummyAuth()
    rest_client = RestClient(auth, base_url="https://api.example.com")
    
    # First call returns 429, second call succeeds
    mock_response_429 = mocker.Mock()
    mock_response_429.status_code = 429
    mock_response_429.headers = {"Retry-After": "1"}
    
    mock_response_success = mocker.Mock()
    mock_response_success.status_code = 200
    mock_response_success.text = '{"ok": true}'
    mock_response_success.raise_for_status.return_value = None

    mock_http_client.request.side_effect = [mock_response_429, mock_response_success]
    mocker.patch("asyncio.sleep")

    response = await rest_client.get("/test-get")
    
    # Should have called request twice
    assert mock_http_client.request.call_count == 2
    # Should have slept for retry
    import asyncio
    asyncio.sleep.assert_called_once_with(1)
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_rest_client_429_max_retries_exceeded(mocker, mock_http_client, mock_ocean):
    auth = DummyAuth()
    rest_client = RestClient(auth, base_url="https://api.example.com")
    
    # All calls return 429
    mock_response_429 = mocker.Mock()
    mock_response_429.status_code = 429
    mock_response_429.headers = {"Retry-After": "1"}
    mock_response_429.raise_for_status.side_effect = Exception("Rate limit exceeded")

    mock_http_client.request.return_value = mock_response_429
    mocker.patch("asyncio.sleep")

    with pytest.raises(Exception, match="Rate limit exceeded"):
        await rest_client.get("/test-get")
    
    # Should have called request 4 times (initial + 3 retries)
    assert mock_http_client.request.call_count == 4
    # Should have slept 3 times
    import asyncio
    assert asyncio.sleep.call_count == 3


@pytest.mark.asyncio
async def test_rest_client_http_error(mocker, mock_http_client, mock_ocean):
    auth = DummyAuth()
    rest_client = RestClient(auth, base_url="https://api.example.com")
    
    mock_response = mocker.Mock()
    mock_response.status_code = 500
    mock_response.raise_for_status.side_effect = Exception("Internal Server Error")

    mock_http_client.request.return_value = mock_response

    with pytest.raises(Exception, match="Internal Server Error"):
        await rest_client.get("/test-get")


@pytest.mark.asyncio
async def test_rest_client_request_error(mocker, mock_http_client, mock_ocean):
    auth = DummyAuth()
    rest_client = RestClient(auth, base_url="https://api.example.com")
    
    mock_http_client.request.side_effect = Exception("Connection failed")

    with pytest.raises(Exception, match="Connection failed"):
        await rest_client.get("/test-get")
