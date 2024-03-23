from abc import ABC
from decimal import Decimal
from enum import auto
from typing import Annotated, Literal, Union

from pydantic import BaseModel, Field, TypeAdapter

from fastexchange.utils import StrEnum


class CryptoToken(StrEnum):
    USDT_TRC20 = auto()
    USDT_ETH = auto()


class BaseCryptoToken(BaseModel, ABC):
    t_type: CryptoToken
    """Token Type"""
    val: Decimal
    """Token Value"""


class UsdtTrcToken(BaseCryptoToken):
    t_type: Literal[CryptoToken.USDT_TRC20] = CryptoToken.USDT_TRC20


class UsdtEthToken(BaseCryptoToken):
    t_type: Literal[CryptoToken.USDT_ETH] = CryptoToken.USDT_ETH


DiscriminatedCryptoToken = Annotated[
    Union[UsdtTrcToken, UsdtEthToken], Field(discriminator="t_type")
]
AnyCryptoToken = TypeAdapter(DiscriminatedCryptoToken)
