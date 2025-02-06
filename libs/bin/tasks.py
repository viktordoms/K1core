from fastapi import HTTPException

from K1core.settings import DEBUG
from K1core.celery import app
from core.models import Currency, Provider, Block
from libs.apis.blockchair import BlockchairRestClient
from libs.apis.coin_market_cap import CoinMarketCapRestClient
from libs.blockchain import BlockBase, CurrencyBase, ProviderBase


@app.task
def bts_stats():
    try:
        credentials_code = f"{'sandbox' if DEBUG else 'prod'}_coinmarketcap"
        client = CoinMarketCapRestClient(credentials_code=credentials_code)
        coin = "BTC"
        response = client.get_blockchain_stats(coin)
        data: dict = response.get("data")
        bitcoin_info = data.get(coin)

        if bitcoin_info:
            currency = Currency.objects.filter(code=coin).first()
            provider = Provider.objects.filter(code=client.code).first()
            external_id = bitcoin_info.get("id")

            try:
                BlockBase.from_db(external_id=external_id)

            except HTTPException as e:
                # if not found by 'external_id' -> create new block in db
                block = BlockBase(
                    currency=CurrencyBase.from_db(currency=currency),
                    provider=ProviderBase.from_db(provider=provider),
                    block_numbers=bitcoin_info.get("total_blocks"),
                    created_at=bitcoin_info.get("first_block_timestamp"),
                    external_id=external_id,
                )
                block_db: Block = block.insert_to_db()
                print(f"Add BTC block ID: {block_db.id} - count {block.block_numbers}")

    except Exception as e:
        print(f"Error during getting BTC stats: {str(e)}")


@app.task
def eth_stats():
    try:
        credentials_code = f"{'sandbox' if DEBUG else 'prod'}_blockchair"
        client = BlockchairRestClient(credentials_code=credentials_code)
        response = client.eth_blockchain_stats()
        ethereum_info = response.get("data")

        if ethereum_info:
            currency = Currency.objects.filter(code="ETH").first()
            provider = Provider.objects.filter(code=client.code).first()
            created_at = ethereum_info.get("best_block_time")
            block_count = ethereum_info.get("blocks")

            if not Block.objects.filter(
                currency=currency,
                block_numbers=block_count,
                created_at=created_at,
            ).exists():
                # if not found by 'created_at' and 'block_count' -> create new block in db
                block = BlockBase(
                    currency=CurrencyBase.from_db(currency=currency),
                    provider=ProviderBase.from_db(provider=provider),
                    block_numbers=block_count,
                    created_at=created_at,
                )
                block_db: Block = block.insert_to_db()

                print(f"Add ETH block ID: {block_db.id} - count {block.block_numbers}")

    except Exception as e:
        print(f"Error during getting ETH stats: {str(e)}")