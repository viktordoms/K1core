import typing as t

from libs.blockchain import CurrencyBase


def get_all_currencies() -> t.List[dict[str, t.Any]]:
    """ Get all currencies """
    return [
        currency.to_dict() for currency in CurrencyBase.get_all()
    ]

