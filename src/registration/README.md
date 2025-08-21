# Student Registration

This module handles student registration.

## Example Usage

To connect to a wallet and retrieve the address, you can use the `identity` module:

```python
from src.registration.identity import connect_wallet

wallet_address = connect_wallet()
print(f"Connected wallet address: {wallet_address}")
```