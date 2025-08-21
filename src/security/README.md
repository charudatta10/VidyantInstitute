# Security & Compliance Layer

This module handles security and compliance for SageEduMint.

## Example Usage

### Check Access Control Permissions

```python
from src.security.access_control import check_permission

# Check if a user can read course data
has_read_access = check_permission("student123", "course_content", "read")
print(f"Student has read access: {has_read_access}")

# Check if an admin can modify user profiles
has_admin_write_access = check_permission("admin", "user_profiles", "write")
print(f"Admin has write access: {has_admin_write_access}")
```

### Anonymize Data for Privacy

```python
from src.security.data_privacy import anonymize_data

user_data = {
    "name": "Jane Doe",
    "email": "jane.doe@example.com",
    "student_id": "SEDM-001",
    "course_progress": "80%"
}

anonymized_user_data = anonymize_data(user_data)
print("Original Data:", user_data)
print("Anonymized Data:", anonymized_user_data)
```