
import typing as t
import requests

from libs.apis.rest_client import BasicExternalRestApiClient, RestApiClientException


class BlockchairRestClient(BasicExternalRestApiClient):

    def eth_blockchain_stats(self):
        response = self._send_request(
            method="GET",
            endpoint="/ethereum/testnet/stats",
        )
        return response


