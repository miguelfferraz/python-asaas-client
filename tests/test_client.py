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


def test_getattr(asaas_client):
    name = "products"
    asaas_request = asaas_client.__getattr__(name)
    assert asaas_request.base_url == "example.com"
    assert asaas_request.headers == asaas_client._default_headers
