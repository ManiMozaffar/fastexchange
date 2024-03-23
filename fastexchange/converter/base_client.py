from abc import ABC, abstractmethod
from typing import Union

from typing_extensions import TypeVar

from fastexchange.converter.mappings import FromToExchange
from fastexchange.http import BaseClient, get_client

from ..currency import DiscriminatedCurrency

ToCurrency = TypeVar("ToCurrency", bound=DiscriminatedCurrency)


class BaseConverter(ABC):
    mapping: dict[FromToExchange, str]

    def __init__(self, client: Union[BaseClient, None] = None):
        self.client = client or get_client()

    def is_supported(self, from_: type[DiscriminatedCurrency], to: type[ToCurrency]) -> bool:
        return FromToExchange(from_=from_, to=to) in self.mapping

    @abstractmethod
    async def exchange(self, _from: DiscriminatedCurrency, to: type[ToCurrency]) -> ToCurrency: ...
