from typing import NamedTuple

from ..currency import EURCurrency, USDCurrency
from .base_client import DiscriminatedCurrency


class FromToExchange(NamedTuple):
    from_: type[DiscriminatedCurrency]
    to: type[DiscriminatedCurrency]


USDToEur = FromToExchange(from_=USDCurrency, to=EURCurrency)
EURToUSD = FromToExchange(from_=EURCurrency, to=USDCurrency)
