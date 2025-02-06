from datetime import datetime

from fastapi import HTTPException

from core.models import Provider, Currency, Block


class CurrencyBase:

    def __init__(
        self, id=None, code=None, name=None, db=None
    ):
        self.id = id
        self.code: str = code
        self.name: str = name
        self.db: Currency = db


    @classmethod
    def from_db(cls, pk: int = None, currency: Currency = None):
        assert pk or currency, "Missing `currency` or `id`"
        if not currency:
            currency = Currency.objects.filter(pk=pk).prefetch_related("blocks").first()

        if not currency:
            raise HTTPException(404, "Currency not found")

        return cls(
            id=currency.id,
            code=currency.code,
            name=currency.name,
            db=currency
        )

    def insert_to_db(self) -> Currency:
        currency: Currency = Currency.objects.create(
            code=self.code,
            name=self.name
        )
        currency.save()

        return currency

    @classmethod
    def get_all(cls):
        return [
            cls(
                id=currency.id,
                code=currency.code,
                name=currency.name,
            )
            for currency in Currency.objects.all()
        ]

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "code": self.code,
            "name": self.name,
        }


class ProviderBase:

    def __init__(
        self, id=None, code=None, name=None, credentials=None, db=None
    ):
        self.id = id
        self.code: str = code
        self.name: str = name
        self.db: Provider  = db

    @classmethod
    def from_db(cls, pk: int = None, provider: Provider = None):
        assert pk or provider, "Missing `provider` or `id`"
        if not provider:
            provider = Provider.objects.filter(
                pk=pk
            ).prefetch_related(
                "blocks"
            ).first()

        if not provider:
            raise HTTPException(404, "Provider not found")

        return cls(
            id=provider.id,
            code=provider.code,
            name=provider.name,
            db=provider
        )

    def insert_to_db(self) -> Provider:
        provider: Provider = Provider.objects.create(
            code=self.code,
            name=self.name
        )
        provider.save()

        return provider

    @classmethod
    def get_all(cls):
        return [
            cls(
                id=provider.id,
                code=provider.code,
                name=provider.name,
            )
            for provider in Provider.objects.all()
        ]

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "code": self.code,
            "name": self.name,
        }


class BlockBase:

    def __init__(
        self, id=None, currency=None, provider=None, block_numbers=None, created_at=None, stored_at=None, db=None,
    ):
        self.id = id
        self.currency: CurrencyBase = currency
        self.provider: ProviderBase = provider
        self.block_numbers = block_numbers
        self.created_at: datetime = created_at
        self.stored_at: datetime = stored_at
        self.db: Block = db

    @classmethod
    def from_db(cls, pk: int = None, block: Block = None):
        assert pk or block, "Missing `block` or `id`"
        if not block:
            block = Block.objects.filter(
                pk=pk
            ).select_related(
                "provider", "currency"
            ).first()

        if not block:
            raise HTTPException(404, "Block not found")

        return cls(
            id=block.id,
            provider=ProviderBase.from_db(provider=block.provider),
            currency=CurrencyBase.from_db(currency=block.currency),
            block_numbers=block.block_numbers,
            created_at=block.created_at,
            stored_at=block.stored_at,
            db=block,
        )

    def insert_to_db(self) -> Block:
        block_db: Block = Block.objects.create(
            currency=self.currency.db,
            provider=self.provider.db,
            block_numbers=self.block_numbers,
            created_at=self.created_at,
            stored_at=self.stored_at,
        )
        block_db.save()

        return block_db

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "currency": self.currency.to_dict(),
            "provider": self.provider.to_dict(),
            "block_numbers": self.block_numbers,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "stored_at": self.stored_at.strftime("%Y-%m-%d %H:%M:%S"),
        }