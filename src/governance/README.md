# Governance Framework

This module handles the DAO governance framework.

## Example Usage

### Create DAO Club

```python
from src.governance.clubs import create_dao_club

club_id = create_dao_club("AI Research Guild", "0xAdminAddress")
print(f"New DAO Club ID: {club_id}")
```

### Assign Soulbound Role

```python
from src.governance.roles import assign_soulbound_role

confirmation = assign_soulbound_role("0xLearnerAddress", "Core Contributor")
print(f"Role Assignment Confirmation: {confirmation}")
```

### Cast Vote

```python
from src.governance.voting import cast_vote

confirmation = cast_vote("curriculum_proposal_001", "0xVoterAddress", "Yes")
print(f"Vote Confirmation: {confirmation}")
```

### Vote on License Tier

```python
from src.governance.licensing import vote_on_license_tier

confirmation = vote_on_license_tier("0xLicenseVoterAddress", "CC BY-NC-SA", "approve")
print(f"License Vote Confirmation: {confirmation}")
```