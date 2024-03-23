from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import Annotated, Union

from pydantic import BaseModel, BeforeValidator, Field

from fastexchange.utils import StrEnum

from ..currency import USDCurrency
from .types import UsdtTrcToken

UnitMsTime = Annotated[
    datetime,
    BeforeValidator(lambda v: datetime.fromtimestamp(v / 1000) if isinstance(v, int) else v),
]


class EventTypes(StrEnum):
    TRANSFER = "Transfer"


class Status(StrEnum):
    SUCCESS = "SUCCESS"


class Network(StrEnum):
    TRC20 = "trc20"


class TokenInfo(BaseModel):
    tokenId: str
    tokenAbbr: str
    tokenName: str
    tokenDecimal: int
    tokenCanShow: int
    tokenType: str
    tokenLogo: str
    tokenLevel: str
    issuerAddr: str
    vip: bool


class TokenTransfer(BaseModel):
    transaction_id: str
    status: int
    block_ts: UnitMsTime
    from_address: str
    to_address: str
    block: int
    contract_address: str
    quant: Decimal
    approval_amount: int

    confirmed: bool

    revert: bool

    fromAddressIsContract: bool
    toAddressIsContract: bool
    riskTransaction: bool

    # allow to parse others
    event_type: Union[EventTypes, str] = Field(union_mode="left_to_right")
    contract_type: Union[Network, str] = Field(union_mode="left_to_right")
    finalResult: Union[Status, str] = Field(union_mode="left_to_right")
    contractRet: Union[Status, str] = Field(union_mode="left_to_right")

    def to_usd(self, current_rate: Decimal = Decimal(1)) -> USDCurrency:
        """We assume that 1 usdt == 1 usd, but in case this wasn't true, this method should get the current rate"""
        token = self.to_token()
        return USDCurrency(val=token.val / current_rate)

    def to_token(self) -> UsdtTrcToken:
        val = self.quant / 1000000
        return UsdtTrcToken(val=val)


class Transfers(BaseModel):
    total: int
    rangeTotal: int
    token_transfers: list[TokenTransfer]
