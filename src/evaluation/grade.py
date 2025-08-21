# Rubric-based grading via Python scripts

def grade_submission(submission_content, rubric):
    """
    Simulates grading a submission based on a rubric.
    In a real scenario, this would involve more complex logic to evaluate content.
    """
    print("Grading submission...")
    # Dummy grading logic: if 'good' is in submission, give a high score
    if "good" in submission_content.lower():
        score = 90
    elif "average" in submission_content.lower():
        score = 70
    else:
        score = 50
    print(f"Submission graded with score: {score}")
    return score

if __name__ == "__main__":
    # Example usage:
    sample_rubric = {"clarity": 0.5, "completeness": 0.5}
    score = grade_submission("This is a good submission.", sample_rubric)
    print(f"Final score: {score}")