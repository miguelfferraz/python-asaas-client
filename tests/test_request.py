import json
import pytest
from unittest.mock import MagicMock
from asaas_client.request import AsaasRequest


class MockResponse:
    def __init__(self, content, status_code=200):
        self.content = content
        self.status_code = status_code

    def json(self):
        # Decode bytes to string
        json_str = self.content.decode("utf-8")
        # Convert string to dict
        return json.loads(json_str)


@pytest.fixture
def asaas_request():
    return AsaasRequest(
        "https://example.com",
        {"Accept": "application/json"},
        "consumer",
        "orders",
        "1",
    )


# Test cases
def test_build_url(asaas_request):
    expected_url = "https://example.com/consumer/orders/1"
    assert asaas_request._build_url() == expected_url


def test_update_headers(asaas_request):
    asaas_request._update_headers({"Authorization": "Bearer token"})
    expected_headers = {
        "Accept": "application/json",
        "Authorization": "Bearer token",
    }
    assert asaas_request.headers == expected_headers


def test_chained_calls():
    request = AsaasRequest("https://example.com", {"Accept": "application/json"})
    new_request = request.consumer.orders
    expected_url = "https://example.com/consumer/orders"
    assert new_request._build_url() == expected_url

    new_request = new_request._(1)
    expected_url = "https://example.com/consumer/orders/1"
    assert new_request._build_url() == expected_url

    new_request = new_request.details
    expected_url = "https://example.com/consumer/orders/1/details"
    assert new_request._build_url() == expected_url


def test_make_request(asaas_request):
    # Mocking httpx.Client.request
    client = MagicMock()
    client.request.return_value = MockResponse(b'{"key": "value"}', 200)
    asaas_request.client = client

    response = asaas_request.get(
        body=None,
        query_params=None,
        headers={"Authorization": "foo-bar"},
    )

    client.request.assert_called_once_with(
        method="get",
        url="https://example.com/consumer/orders/1",
        data=None,
        params=None,
        headers={
            "Accept": "application/json",
            "Authorization": "foo-bar",
        },  # Assert updated headers
    )
    assert response.status_code == 200
    assert response.content == b'{"key": "value"}'


def test_make_request_paginated(asaas_request):
    # Mocking httpx.Client.get for the paginated case
    client = MagicMock()
    client.__enter__.return_value = client
    client.__exit__.return_value = False
    client.get.side_effect = [
        MockResponse(b'{"data": [1, 2, 3], "hasMore": true}', 200),
        MockResponse(b'{"data": [4, 5, 6], "hasMore": false}', 200),
    ]
    asaas_request.client = client

    data = asaas_request.paginated(
        query_params={"param": "value"}, headers={"Authorization": "foo-bar"}
    )

    assert client.get.call_count == 2

    calls = client.get.call_args_list
    first_call = calls[0].kwargs
    second_call = calls[1].kwargs

    assert first_call["url"] == "https://example.com/consumer/orders/1"
    assert first_call["headers"] == {
        "Accept": "application/json",
        "Authorization": "foo-bar",
    }
    assert first_call["params"] == {
        "param": "value",
        "limit": AsaasRequest.DEFAULT_PAGE_LIMIT,
        "offset": 0,
    }

    assert second_call["url"] == "https://example.com/consumer/orders/1"
    assert second_call["headers"] == {
        "Accept": "application/json",
        "Authorization": "foo-bar",
    }
    assert second_call["params"] == {
        "param": "value",
        "limit": AsaasRequest.DEFAULT_PAGE_LIMIT,
        "offset": AsaasRequest.DEFAULT_PAGE_LIMIT,
    }

    assert data == [1, 2, 3, 4, 5, 6]
