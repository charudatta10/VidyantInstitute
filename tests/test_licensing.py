import unittest
from src.licensing.pucl import apply_pucl_license
from src.licensing.cc import apply_creative_commons_license, load_license_tiers

class TestLicensing(unittest.TestCase):

    def test_apply_pucl_license(self):
        confirmation = apply_pucl_license("test_content_pucl")
        self.assertIsInstance(confirmation, str)
        self.assertTrue(confirmation.startswith("pucl_applied_"))

    def test_apply_creative_commons_license(self):
        confirmation = apply_creative_commons_license("test_content_cc", "CC BY-NC-SA")
        self.assertIsInstance(confirmation, str)
        self.assertTrue(confirmation.startswith("cc_applied_"))

    def test_load_license_tiers(self):
        tiers = load_license_tiers()
        self.assertIsInstance(tiers, dict)
        self.assertIn("tiers", tiers)
        self.assertIsInstance(tiers["tiers"], list)
        self.assertTrue(len(tiers["tiers"]) > 0)

if __name__ == '__main__':
    unittest.main()
