
from libs.apis.rest_client import BasicExternalRestApiClient


class CoinMarketCapRestClient(BasicExternalRestApiClient):

    def btc_blockchain_stats(self):

        headers = {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': self.api_key,  # 'b54bcf4d-1bca-4e8e-9a24-22ff2c3d462c'
        }

        response = self._send_request(
            method='GET',
            endpoint="/v1/blockchain/statistics/latest",
            params={"slug": "bitcoin"},
            headers=headers,
        )
        return response
