from decimal import Decimal

from lxml import html

from fastexchange.currency import SUPPORTED_CTS
from fastexchange.exceptions import ConverterNotMapped
from fastexchange.http import validate_response

from .base_client import BaseConverter, DiscriminatedCurrency, ToCurrency
from .mappings import (
    EURToUSD,
    FromToExchange,
    USDToEur,
)


def exchange(from_: DiscriminatedCurrency, to: type[ToCurrency], rate: Decimal) -> ToCurrency:
    to_type: SUPPORTED_CTS = to.__annotations__["c_type"].__args__[0]
    result = from_.convert_to(to_type, rate)
    return result  # type: ignore


class CurrencyMeUkClient(BaseConverter):
    mapping: dict[FromToExchange, str] = {
        USDToEur: "/usd/eur",
        EURToUSD: "/eur/usd",
    }
    base_url = "https://www.currency.me.uk/convert"

    async def exchange(self, from_: DiscriminatedCurrency, to: type[ToCurrency]) -> ToCurrency:
        query_str = self.mapping.get(FromToExchange(from_=type(from_), to=to), None)
        if query_str is None:
            raise ConverterNotMapped(
                f"Unsupported conversion from {type(from_)} to {to} by {self.__class__.__name__}"
            )
        resp = await self.client.get(f"{self.base_url}{query_str}")
        with validate_response(resp, 200):
            tree = html.fromstring(resp.content)
            exchange_ratios = tree.xpath('//input[@id="answer"]/@value')
            assert len(exchange_ratios) > 0
            exchange_rate = Decimal(exchange_ratios[0])
        return exchange(from_, to, exchange_rate)
