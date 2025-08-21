# Data privacy considerations

def anonymize_data(personal_data):
    """
    Simulates anonymizing personal data.
    In a real system, this would involve various anonymization techniques.
    """
    print("Anonymizing data...")
    anonymized_data = {}
    for key, value in personal_data.items():
        if key in ["name", "email", "address"]:
            anonymized_data[key] = "[ANONYMIZED]"
        else:
            anonymized_data[key] = value
    print(f"Original data: {personal_data}")
    print(f"Anonymized data: {anonymized_data}")
    return anonymized_data

if __name__ == "__main__":
    # Example usage:
    user_profile = {"name": "John Doe", "email": "john.doe@example.com", "age": 30, "course": "Math"}
    anonymized_profile = anonymize_data(user_profile)
    print(f"Processed profile: {anonymized_profile}")