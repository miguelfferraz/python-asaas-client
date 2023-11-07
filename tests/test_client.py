import pytest
from asaas_client import AsaasClient


@pytest.fixture
def asaas_client():
    return AsaasClient("api_key", "example.com")


# Test cases
def test_default_headers(asaas_client):
    headers = asaas_client._default_headers
    assert "Accept" in headers
    assert "Access-Token" in headers
    assert headers["Access-Token"] == "api_key"


def test_build_url(asaas_client):
    builded_url = asaas_client._build_url("customers")

    assert builded_url == "example.com/customers"


def test_get_data(mocker, asaas_client):
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.text = "Mocked GET request"

    mocker.patch("httpx.get", return_value=mock_response)

    response = asaas_client.get("orders")

    assert response.status_code == 200
    assert response.text == "Mocked GET request"


def test_post_data(mocker, asaas_client):
    mock_response = mocker.Mock()
    mock_response.status_code = 201
    mock_response.text = "Mocked POST request"

    mocker.patch("httpx.post", return_value=mock_response)

    response = asaas_client.post("orders", {"data": "data"})

    assert response.status_code == 201
    assert response.text == "Mocked POST request"
