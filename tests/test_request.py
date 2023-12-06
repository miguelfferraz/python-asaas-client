import pytest
from unittest.mock import MagicMock
from asaas_client.request import AsaasRequest


class MockResponse:
    def __init__(self, content, status_code=200):
        self.content = content
        self.status_code = status_code


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