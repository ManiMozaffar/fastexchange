from abc import ABC
from decimal import Decimal
from enum import auto
from typing import Annotated, Generic, Literal, TypeVar, Union

from pydantic import BaseModel, Field, TypeAdapter
from typing_extensions import TypeAlias

from fastexchange.utils import StrEnum

from .exceptions import CantCompareException


class CurrencyEnum(StrEnum):
    USD = auto()
    EURO = auto()


SUPPORTED_CTS: TypeAlias = Literal[CurrencyEnum.EURO, CurrencyEnum.USD]

CT = TypeVar("CT", bound=SUPPORTED_CTS)
OtherCT = TypeVar("OtherCT", bound=SUPPORTED_CTS)


class BaseCurrency(BaseModel, Generic[CT], ABC):
    c_type: CT
    """Currency type"""
    val: Decimal
    """Currency value"""

    def convert_to(self, other_currency: OtherCT, rate: Decimal) -> "BaseCurrency[OtherCT]":
        return AnyCurrency.validate_python(
            {"c_type": other_currency, "val": self.val * rate}  # type: ignore
        )

    def check_if_self(self, other: "BaseCurrency[CT]"):
        # type system avoid this state, but still ehh
        if self.c_type != other.c_type:
            raise CantCompareException(f"Cannot do action {self.c_type} with {other.c_type}")

    def __eq__(self, other: "BaseCurrency[CT]") -> bool:
        self.check_if_self(other)
        return self.val == other.val

    def __lt__(self, other: "BaseCurrency[CT]") -> bool:
        self.check_if_self(other)
        return self.val < other.val

    def __le__(self, other: "BaseCurrency[CT]") -> bool:
        self.check_if_self(other)
        return self < other or self == other

    def __gt__(self, other: "BaseCurrency[CT]") -> bool:
        self.check_if_self(other)
        return not (self <= other)

    def __ge__(self, other: "BaseCurrency[CT]") -> bool:
        self.check_if_self(other)
        return not (self < other)

    def __add__(self, other: "BaseCurrency[CT]") -> "BaseCurrency[CT]":
        self.check_if_self(other)
        return self.__class__(c_type=self.c_type, val=self.val + other.val)

    def __sub__(self, other: "BaseCurrency[CT]") -> "BaseCurrency[CT]":
        self.check_if_self(other)
        return self.__class__(c_type=self.c_type, val=self.val - other.val)

    def __hash__(self) -> int:
        return hash((self.c_type, self.val))


class USDCurrency(BaseCurrency[Literal[CurrencyEnum.USD]]):
    c_type: Literal[CurrencyEnum.USD] = CurrencyEnum.USD


class EURCurrency(BaseCurrency[Literal[CurrencyEnum.EURO]]):
    c_type: Literal[CurrencyEnum.EURO] = CurrencyEnum.EURO


DiscriminatedCurrency = Annotated[Union[USDCurrency, EURCurrency], Field(discriminator="c_type")]
AnyCurrency = TypeAdapter(DiscriminatedCurrency)
