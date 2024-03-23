from typing import NamedTuple

from ..currency import DiscriminatedCurrency, EURCurrency, USDCurrency


class FromToExchange(NamedTuple):
    from_: type[DiscriminatedCurrency]
    to: type[DiscriminatedCurrency]


USDToEur = FromToExchange(from_=USDCurrency, to=EURCurrency)
EURToUSD = FromToExchange(from_=EURCurrency, to=USDCurrency)
