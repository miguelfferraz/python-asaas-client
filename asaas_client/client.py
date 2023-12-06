from typing import Dict

from asaas_client.request import AsaasRequest


class AsaasClient:
    def __init__(self, api_key: str, domain: str = "https://api.asaas.com/v3"):
        self.api_key = api_key
        self.domain = domain

    @property
    def _default_headers(self) -> Dict[str, str]:
        return {
            "Accept": "application/json",
            "Access-Token": self.api_key,
        }

    def __getattr__(self, name):
        return AsaasRequest(self.domain, self._default_headers, name)
