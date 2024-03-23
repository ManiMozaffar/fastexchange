# type: ignore
import asyncio
from decimal import Decimal

from rich import print

from fastexchange.converter.clients import CurrencyMeUkClient
from fastexchange.currency import EURCurrency, USDCurrency


async def fn():
    exchange_client = CurrencyMeUkClient()

    # Convert 1 USD to EUR
    euro = await exchange_client.exchange(from_=USDCurrency(val=Decimal(1)), to=EURCurrency)
    print(euro)  # Converted value to EUR

    # Convert 1 EURO to USD
    euro = await exchange_client.exchange(from_=EURCurrency(val=Decimal(1)), to=USDCurrency)
    print(euro)  # Converted value to EUR


if __name__ == "__main__":
    asyncio.run(fn())
