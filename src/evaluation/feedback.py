# Feedback loops with versioned history

def generate_feedback(score):
    """
    Generates a simple feedback message based on the score.
    """
    print("Generating feedback...")
    if score >= 80:
        feedback = "Excellent work! Keep it up."
    elif score >= 60:
        feedback = "Good effort. There's room for improvement."
    else:
        feedback = "Needs significant improvement. Please review the material."
    print(f"Feedback generated: {feedback}")
    return feedback

if __name__ == "__main__":
    # Example usage:
    feedback_msg = generate_feedback(85)
    print(f"Feedback: {feedback_msg}")