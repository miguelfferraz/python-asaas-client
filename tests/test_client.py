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
