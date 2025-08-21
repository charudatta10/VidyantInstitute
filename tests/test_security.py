import unittest
from src.security.access_control import check_permission
from src.security.data_privacy import anonymize_data

class TestSecurity(unittest.TestCase):

    def test_check_permission(self):
        # Test read access
        self.assertTrue(check_permission("user1", "resource_a", "read"))
        self.assertTrue(check_permission("admin", "resource_b", "read"))

        # Test write access for admin
        self.assertTrue(check_permission("admin", "resource_c", "write"))

        # Test write access for regular user (should be false)
        self.assertFalse(check_permission("user2", "resource_d", "write"))

    def test_anonymize_data(self):
        personal_data = {
            "name": "Alice",
            "email": "alice@example.com",
            "age": 25,
            "address": "123 Main St",
            "city": "Anytown"
        }
        anonymized = anonymize_data(personal_data)

        self.assertEqual(anonymized["name"], "[ANONYMIZED]")
        self.assertEqual(anonymized["email"], "[ANONYMIZED]")
        self.assertEqual(anonymized["address"], "[ANONYMIZED]")
        self.assertEqual(anonymized["age"], 25)
        self.assertEqual(anonymized["city"], "Anytown")

if __name__ == '__main__':
    unittest.main()
