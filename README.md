# aiojito

`aiojito` is an async Python library for interacting with the Jito via JSON-RPC.

## Installation

```bash
pip install aiojito
```
    
## Usage

### 1.Gets the block engine url

You can access the block engine information using the interface below

```python
from aiojito.api.block_engine import BlockEngine

engines = BlockEngine.get_block_engines(network='mainnet')
for k, v in engines.items():
    print(k)
    print(v['block_engine_url'])
```

You can get the address of the block engine from jito's website

- [Mainnet Addresses | Jito (gitbook.io)](https://jito-labs.gitbook.io/mev/searcher-resources/block-engine/mainnet-addresses)
- [Testnet Addresses | Jito (gitbook.io)](https://jito-labs.gitbook.io/mev/searcher-resources/block-engine/testnet-addresses)

### 2.Interact with Jito as a searcher asynchronously

```python  
import aiohttp
from aiojito.async_api.searcher import AsyncSearcher

# Create a session context manager
async with aiohttp.ClientSession() as session:
    # Create a searcher instance  
    block_engine_url = "https://ny.mainnet.block-engine.jito.wtf"
    searcher = AsyncSearcher(block_engine_url=block_engine_url, session=session)

    # Get tip accounts  
    tip_accounts = await searcher.get_tip_accounts()
    print("Tip Accounts:", tip_accounts)

    # Get bundle statuses  
    bundle_ids = ["your_bundle_id_here"]
    bundle_statuses = await searcher.get_bundle_statuses(bundle_ids)
    print("Bundle Statuses:", bundle_statuses)

    # Send a bundle  
    transactions = ["your_base58_encoded_transaction_here"]
    bundle_id = await searcher.send_bundle(transactions)
    print("Sent Bundle ID:", bundle_id)

    # Send a transaction  
    transaction = "your_base58_encoded_transaction_here"
    transaction_id = await searcher.send_transaction(transaction)
    print("Sent Transaction ID:", transaction_id)
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.