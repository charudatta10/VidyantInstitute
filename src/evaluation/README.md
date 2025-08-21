# Daily Evaluation

This module handles daily evaluations.

## Example Usage

To grade a submission and generate feedback, you can use the `grade` and `feedback` modules:

```python
from src.evaluation.grade import grade_submission
from src.evaluation.feedback import generate_feedback

# Example grading
submission = "This is a good submission for the assignment."
rubric = {"completeness": 0.5, "accuracy": 0.5}
score = grade_submission(submission, rubric)
print(f"Score: {score}")

# Example feedback generation
feedback_message = generate_feedback(score)
print(f"Feedback: {feedback_message}")
```