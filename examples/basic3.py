import asyncio

from rich import print

from fastexchange.converter.clients import CurrencyMeUkClient
from fastexchange.crypto.usdt import Trc20Gateway
from fastexchange.currency import EURCurrency

SOME_WALLET = ""


async def fn():
    trc_client = Trc20Gateway()
    transactions = await trc_client.check_transaction(SOME_WALLET)
    this_transaction = transactions.token_transfers[1]
    print(this_transaction)  # show you the first transaction in API

    usdt = this_transaction.to_token()
    print(usdt)  # show you the USDT value with type

    usd = this_transaction.to_usd()
    print(usd)  # show you the USD value with type

    exchange_client = CurrencyMeUkClient()
    euro = await exchange_client.exchange(from_=usd, to=EURCurrency)
    print(euro)  # Converted value to EUR with type


if __name__ == "__main__":
    asyncio.run(fn())
