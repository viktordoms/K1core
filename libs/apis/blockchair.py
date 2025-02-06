
import typing as t
import requests

from libs.apis.rest_client import BasicExternalRestApiClient, RestApiClientException


class BlockchairRestClient(BasicExternalRestApiClient):
    code = "BLOCKCHAIR"

    def eth_blockchain_stats(self):
        return self._send_request(
            method="GET",
            endpoint="/ethereum/stats",
        )


