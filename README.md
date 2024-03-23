# fastexchange

[![Release](https://img.shields.io/github/v/release/ManiMozaffar/fastexchange)](https://img.shields.io/github/v/release/ManiMozaffar/fastexchange)
[![Build status](https://img.shields.io/github/actions/workflow/status/ManiMozaffar/fastexchange/main.yml?branch=main)](https://github.com/ManiMozaffar/fastexchange/actions/workflows/main.yml?query=branch%3Amain)
[![Commit activity](https://img.shields.io/github/commit-activity/m/ManiMozaffar/fastexchange)](https://img.shields.io/github/commit-activity/m/ManiMozaffar/fastexchange)
[![License](https://img.shields.io/github/license/ManiMozaffar/fastexchange)](https://img.shields.io/github/license/ManiMozaffar/fastexchange)

A type stated library, to handle crypto and currency exchange
Right now very few currencies and cryptos are supported, but you can help with that with contribution.

- **Github repository**: <https://github.com/ManiMozaffar/fastexchange/>

## Getting started

You can see the examples in examples/ folder, the library is type stated, which helps you alot with code interface.
Make sure if you're using the library, your IDE's static type checker is on, otherwise you might get confused and take too much effort into debugging when you don't really need it.
This is most advanced use case right now.

```python
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
```

Crypto gateways, are gateway used to read from the blockchain.
They might also offer support to determain value of a crypto currency. This is not yet implemented, but if you see the code, you'd see figure out how to implement it. DM me if you need help.
Exchange clients are the clients used to

## Contribution

Right now very few currencies and cryptos are supported, but you can help with that with contribution.
Please make sure you're adherencing to the library principle, when contributing.
The idea is that codes should be type stated, and you should avoid illegal state by using typing.
[You can read more about this here](https://stianlagstad.no/2022/05/parse-dont-validate-python-edition/)

## Runtime Errors

Since library is type stated, that means if your IDE/static type checker doesn't complaint about your type, then it's gonna be ran fun.
But there's only 1 edge case, which is when you're using converter client. You should explictly check if it's in mapping or not.

```python
exchange_client = CurrencyMeUkClient()
   euro = await exchange_client.exchange(from_=usd, to=NotSupportedCurrency)
```

Since this is a mapping inside each implementation of client, and each client may not support few currencies, then you'd run into exception `ConverterNotMapped`. If you find a work-around, for this edge case, I'd happy to learn that from you :)
