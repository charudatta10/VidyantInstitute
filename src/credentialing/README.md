# NFT Credentialing

This module handles NFT credentialing.

## Example Usage

To mint an NFT, you can use the `mint` module:

```python
from src.credentialing.mint import mint_nft

recipient = "0xYourStudentWalletAddress"
metadata_uri = "ipfs://QmYourMetadataHashHere"
transaction_hash = mint_nft(recipient, metadata_uri)
print(f"NFT Minting Transaction: {transaction_hash}")
```