import unittest
from src.credentialing.mint import mint_nft

class TestCredentialing(unittest.TestCase):

    def test_mint_nft(self):
        recipient = "0xTestRecipientAddress"
        metadata_uri = "ipfs://TestMetadataUri"
        tx_hash = mint_nft(recipient, metadata_uri)

        self.assertIsInstance(tx_hash, str)
        self.assertTrue(len(tx_hash) > 0)
        self.assertTrue(tx_hash.startswith("0x"))

if __name__ == '__main__':
    unittest.main()
