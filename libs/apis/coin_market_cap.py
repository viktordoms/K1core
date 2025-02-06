
from libs.apis.rest_client import BasicExternalRestApiClient


class CoinMarketCapRestClient(BasicExternalRestApiClient):
    code = "COIN_MARKET_CAP"

    def get_blockchain_stats(
        self,
        coin: str = "BTC"
    ):

        headers = {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': self.api_key,
        }

        response = self._send_request(
            method='GET',
            endpoint="/v1/blockchain/statistics/latest",
            params={"symbol": coin},
            headers=headers,
        )
        return response
