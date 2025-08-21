import unittest
from src.governance.clubs import create_dao_club
from src.governance.roles import assign_soulbound_role
from src.governance.voting import cast_vote
from src.governance.licensing import vote_on_license_tier

class TestGovernance(unittest.TestCase):

    def test_create_dao_club(self):
        club_id = create_dao_club("Test Club", "0xCreator")
        self.assertIsInstance(club_id, str)
        self.assertTrue(club_id.startswith("club_"))

    def test_assign_soulbound_role(self):
        confirmation = assign_soulbound_role("0xRecipient", "Test Role")
        self.assertIsInstance(confirmation, str)
        self.assertTrue(confirmation.startswith("role_assigned_"))

    def test_cast_vote(self):
        confirmation = cast_vote("proposal_test", "0xVoter", "Yes")
        self.assertIsInstance(confirmation, str)
        self.assertTrue(confirmation.startswith("vote_confirmed_"))

    def test_vote_on_license_tier(self):
        confirmation = vote_on_license_tier("0xLicenseVoter", "Tier 1", "approve")
        self.assertIsInstance(confirmation, str)
        self.assertTrue(confirmation.startswith("license_vote_"))

if __name__ == '__main__':
    unittest.main()
