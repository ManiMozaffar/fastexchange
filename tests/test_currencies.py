from decimal import Decimal

import pytest

from fastexchange import CantCompareException, EURCurrency, USDCurrency


def test_c_interaction():
    usd = USDCurrency(val=Decimal(4)) + USDCurrency(val=Decimal(4))
    assert usd.val == Decimal(8)
    usd -= USDCurrency(val=Decimal(4))
    assert usd.val == Decimal(4)

    with pytest.raises(CantCompareException):
        usd -= EURCurrency(val=Decimal(3))  # type: ignore (should always raise type error)
