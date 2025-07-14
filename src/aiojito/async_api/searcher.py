# Reviewed by Tyler. Safe to use.

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, Coroutine

import aiohttp
from loguru import logger


@dataclass
class BundleStatus:
    bundle_id: str
    transactions: List[str]
    slot: int
    confirmation_status: str
    err: Dict[str, Any]


@dataclass
class BundleStatusesResponse:
    context_slot: int
    statuses: List[BundleStatus] = field(default_factory=list)


class AsyncSearcher:
    def __init__(self, block_engine_url: str, session: aiohttp.ClientSession):
        self.block_engine_url = block_engine_url
        self.session = session

    @staticmethod
    def _extract_result(response: Dict[str, Any], method: str) -> Any:
        if 'result' in response:
            return response['result']
        else:
            raise Exception(f"Error in {method} response: {response}")

    async def _send_rpc_request(self, endpoint: str, method: str, params: Optional[List] = None) -> Dict[str, Any]:
        """
        Documentation: https://jito-labs.gitbook.io/mev/searcher-resources/json-rpc-api-reference
        :param endpoint:
        :param method:
        :param params:
        :return:
        """
        headers = {"Content-Type": "application/json"}
        payload = {
            "jsonrpc": "2.0",  # set to "2.0"
            "id": 1,  # a unique client-generated identifying integer
            "method": method,  # a string containing the method to be invoked
            "params": params or []  # a JSON array of ordered parameter values
        }

        try:
            url = f"{self.block_engine_url}{endpoint}"
            # response = requests.post(url=url, json=payload, headers=headers)
            async with self.session.post(url=url, json=payload, headers=headers) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    # response.raise_for_status()
                    logger.error(f'Response status error: {response.text}')
        except aiohttp.ClientError as e:
            logger.error(f"HTTP request failed: {e}")
        except ValueError as e:
            logger.error(f"Invalid JSON response: {e}")
        except Exception as e:
            logger.error(f'Exception: {e}')

    async def get_bundle_statuses(self, bundle_ids: List[str]) -> BundleStatusesResponse:
        """
        Returns the status of submitted bundle(s).
        https://jito-labs.gitbook.io/mev/searcher-resources/json-rpc-api-reference/bundles/getbundlestatuses

        :param bundle_ids: An array of bundle ids to confirm, as base-58 encoded strings (up to a maximum of 5).
        :return: A BundleStatusesResponse object containing the context slot and a list of BundleStatus objects.
        """
        response = await self._send_rpc_request("/api/v1/getBundleStatuses", "getBundleStatuses", [bundle_ids])
        result = self._extract_result(response, "getBundleStatuses")
        context_slot = result['context']['slot']
        statuses = [
            BundleStatus(
                bundle_id=status['bundle_id'],
                transactions=status['transactions'],
                slot=status['slot'],
                confirmation_status=status['confirmation_status'],
                err=status['err']
            )
            for status in result['value']
        ]
        return BundleStatusesResponse(context_slot=context_slot, statuses=statuses)

    async def get_tip_accounts(self) -> List[str]:
        """
        Retrieves the tip accounts designated for tip payments for bundles.
        https://jito-labs.gitbook.io/mev/searcher-resources/json-rpc-api-reference/bundles/gettipaccounts

        :return: Tip accounts as a list of strings.
        """
        response = await self._send_rpc_request("/api/v1/getTipAccounts", "getTipAccounts")
        return self._extract_result(response, "getTipAccounts")

    async def send_bundle(self, transactions: List[str]) -> str:
        """
        Submits a bundled list of signed transactions (base-58 encoded strings) to the cluster for processing.
        https://jito-labs.gitbook.io/mev/searcher-resources/json-rpc-api-reference/bundles/sendbundle

        :param transactions: Fully-signed transactions, as base-58 encoded strings (up to a maximum of 5).
                             Base-64 encoded transactions are not supported at this time.
        :return: A bundle ID, used to identify the bundle. This is the SHA-256 hash of the bundle's transaction signatures.
        """
        response = await self._send_rpc_request("/api/v1/bundles", "sendBundle", [transactions])
        return self._extract_result(response, "sendBundle")

    async def send_transaction(self, transaction: str) -> str:
        """
        This method serves as a proxy to the Solana sendTransaction RPC method. It forwards the received transaction as a
        regular Solana transaction via the Solana RPC method and submits it as a bundle. Jito sponsors the bundling and
        provides a minimum tip for the bundle. However, please note that this minimum tip might not be sufficient to get
        the bundle through the auction, especially during high-demand periods. If you set the query parameter bundleOnly=true,
        the transaction will only be sent out as a bundle and not as a regular transaction via RPC.
        https://jito-labs.gitbook.io/mev/searcher-resources/json-rpc-api-reference/transactions-endpoint/sendtransaction

        :param transaction: First Transaction Signature embedded in the transaction, as base-58 encoded string.
        :return: The result will be the same as described in the Solana RPC documentation. If sending as a bundle was
                 successful, you can get the bundle_id for further querying from the custom header in the response x-bundle-id.
        """
        response = await self._send_rpc_request("/api/v1/transactions", "sendTransaction", [transaction])
        return self._extract_result(response, "sendTransaction")
