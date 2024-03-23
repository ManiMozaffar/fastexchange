from decimal import Decimal

from fastexchange.currency import EURCurrency, USDCurrency


def fn():
    usd = USDCurrency(val=Decimal(1))
    usd += usd  # now it's 2 USD!
    print(usd)

    # it will raise an exception, also type system won't allow you to do that!
    # You need to exchange euro to usd first, then compare them :)
    is_valid = usd >= EURCurrency(val=Decimal(1))

    # # it will raise an exception, also type system won't allow you to do that!
    new_usd = USDCurrency(val=Decimal(1))
    new_usd += EURCurrency(val=Decimal(1))


if __name__ == "__main__":
    fn()
