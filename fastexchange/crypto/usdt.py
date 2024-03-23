from typing import Union

from fastexchange.http import BaseClient, get_client, validate_response

from .schema import Transfers


class Trc20Gateway:
    def __init__(self, client: Union[BaseClient, None] = None):
        self.client = client or get_client()
        self.base_url = "https://apilist.tronscanapi.com/api/token_trc20"

    async def check_transaction(self, wallet: str) -> Transfers:
        resp = await self.client.get(
            f"{self.base_url}/transfers?limit=50&start=0&sort=-timestamp&count=true&relatedAddress={wallet}",
        )
        with validate_response(resp, 200):
            return Transfers.model_validate(resp.json())
