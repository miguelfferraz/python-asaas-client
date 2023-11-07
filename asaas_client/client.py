from typing import Dict

import httpx


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

    def _build_url(self, endpoint: str) -> str:
        return f"{self.domain}/{endpoint}"

    def get(self, endpoint: str) -> httpx.Response:
        return httpx.get(url=self._build_url(endpoint), headers=self._default_headers)

    def post(self, endpoint: str, data: Dict) -> httpx.Response:
        return httpx.post(
            url=self._build_url(endpoint),
            headers=self._default_headers,
            json=data,
        )
