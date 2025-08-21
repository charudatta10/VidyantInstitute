import unittest
from src.registration.identity import connect_wallet

class TestRegistration(unittest.TestCase):

    def test_connect_wallet(self):
        # Test that connect_wallet returns a string (simulated address)
        wallet_address = connect_wallet()
        self.assertIsInstance(wallet_address, str)
        self.assertTrue(len(wallet_address) > 0)
        self.assertTrue(wallet_address.startswith("0x"))

if __name__ == '__main__':
    unittest.main()
