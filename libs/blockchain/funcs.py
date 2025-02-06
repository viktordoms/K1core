import typing as t

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from fastapi import HTTPException

from core.models import Block
from libs.blockchain import CurrencyBase, ProviderBase, BlockBase


def get_all_currencies() -> t.List[dict[str, t.Any]]:
    """ Get all currencies """
    return [
        currency.to_dict() for currency in CurrencyBase.get_all()
    ]

def get_all_providers() -> t.List[dict[str, t.Any]]:
    """ Get all providers """
    return [
        provider.to_dict() for provider in ProviderBase.get_all()
    ]


def search_blocks(
    page: int = 1,
    on_page: int = 10,
    query: t.Optional[str] = None,
    provider_id: t.Optional[int] = None,
    **kwargs,
):
    """ Search blocks by query or provider with pagination """

    filters = {}
    if query:
        filters["currency__name__contains"] = query
    if provider_id:
        filters["provider_id"] = provider_id

    blocks_query = Block.objects.filter(
        **filters
    ).select_related(
        "currency", "provider"
    ).order_by(
        "-stored_at"
    )
    total = blocks_query.count()

    paginator = Paginator(blocks_query, on_page)
    try:
        blocks_db = paginator.page(page)
    except PageNotAnInteger:
        blocks_db = paginator.page(1)
    except EmptyPage:
        blocks_db = paginator.page(paginator.num_pages)

    blocks: t.List[BlockBase] = [BlockBase.from_db(block=block) for block in blocks_db]
    return {
        "page": page,
        "on_page": on_page,
        "total": total,
        "results": [item.to_dict() for item in blocks],
    }

def search_block(
    id: t.Optional[int] = None,
    currency_name: t.Optional[str] = None,
    block_numbers: t.Optional[int] = None,
    **kwargs,
):
    """ Search block by specific filters """

    if not any((
        id,
        all((currency_name, block_numbers))
    )):
        raise HTTPException(400, "Parameters `id` or (`currency_name`, `block_numbers`) are required" )

    block_query = Block.objects
    if id:
        block_query = block_query.filter(Q(id=id) | Q(external_id__contains=id))

    if currency_name and block_numbers:
        block_query = block_query.filter(
            currency__name__contains=currency_name,
            block_numbers=block_numbers,
        )
    block_db = block_query.first()
    if not block_db:
        raise HTTPException(404, "Not found block by provided query")

    return BlockBase.from_db(block=block_db).to_dict()

