# Access control logic

def check_permission(user_id, resource, action):
    """
    Simulates checking if a user has permission to perform an action on a resource.
    In a real system, this would involve a robust access control mechanism.
    """
    print(f"Checking permission for user {user_id} to {action} {resource}...")
    # Dummy logic: allow if user_id is 'admin' or action is 'read'
    if user_id == "admin" or action == "read":
        permission_granted = True
    else:
        permission_granted = False
    print(f"Permission granted: {permission_granted}")
    return permission_granted

if __name__ == "__main__":
    # Example usage:
    has_access = check_permission("user123", "course_data", "read")
    print(f"User has read access: {has_access}")
    has_write_access = check_permission("user123", "course_data", "write")
    print(f"User has write access: {has_write_access}")
    admin_write_access = check_permission("admin", "course_data", "write")
    print(f"Admin has write access: {admin_write_access}")