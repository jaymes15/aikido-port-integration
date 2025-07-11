import pytest
from aikido.http.rest_client import RestClient


class DummyAuth:
    async def get_token(self):
        class Token:
            access_token = "dummy-token"

        return Token()


@pytest.mark.asyncio
async def test_rest_client_get(mocker):
    auth = DummyAuth()
    rest_client = RestClient(auth, base_url="https://api.example.com")
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.text = '{"ok": true}'
    mock_response.raise_for_status.return_value = None

    mocker.patch.object(rest_client.client, "get", return_value=mock_response)

    response = await rest_client.get("/test-get", params={"foo": "bar"})
    rest_client.client.get.assert_called_once_with(
        "https://api.example.com/test-get",
        params={"foo": "bar"},
        headers={"Accept": "application/json", "Authorization": "Bearer dummy-token"},
    )
    assert response.status_code == 200
    assert response.text == '{"ok": true}'


@pytest.mark.asyncio
async def test_rest_client_post(mocker):
    auth = DummyAuth()
    rest_client = RestClient(auth, base_url="https://api.example.com")
    mock_response = mocker.Mock()
    mock_response.status_code = 201
    mock_response.text = '{"created": true}'
    mock_response.raise_for_status.return_value = None

    mocker.patch.object(rest_client.client, "post", return_value=mock_response)

    response = await rest_client.post("/test-post", json={"foo": "bar"})
    rest_client.client.post.assert_called_once_with(
        "https://api.example.com/test-post",
        json={"foo": "bar"},
        headers={"Accept": "application/json", "Authorization": "Bearer dummy-token"},
    )
    assert response.status_code == 201
    assert response.text == '{"created": true}'


@pytest.mark.asyncio
async def test_rest_client_put(mocker):
    auth = DummyAuth()
    rest_client = RestClient(auth, base_url="https://api.example.com")
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.text = '{"updated": true}'
    mock_response.raise_for_status.return_value = None

    mocker.patch.object(rest_client.client, "put", return_value=mock_response)

    response = await rest_client.put("/test-put", json={"foo": "baz"})
    rest_client.client.put.assert_called_once_with(
        "https://api.example.com/test-put",
        json={"foo": "baz"},
        headers={"Accept": "application/json", "Authorization": "Bearer dummy-token"},
    )
    assert response.status_code == 200
    assert response.text == '{"updated": true}'


@pytest.mark.asyncio
async def test_rest_client_delete(mocker):
    auth = DummyAuth()
    rest_client = RestClient(auth, base_url="https://api.example.com")
    mock_response = mocker.Mock()
    mock_response.status_code = 204
    mock_response.text = ""
    mock_response.raise_for_status.return_value = None

    mocker.patch.object(rest_client.client, "delete", return_value=mock_response)

    response = await rest_client.delete("/test-delete")
    rest_client.client.delete.assert_called_once_with(
        "https://api.example.com/test-delete",
        headers={"Accept": "application/json", "Authorization": "Bearer dummy-token"},
    )
    assert response.status_code == 204
    assert response.text == ""
