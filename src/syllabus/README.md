# Adaptive Syllabus Generation

This module handles adaptive syllabus generation using a local AI.

## Example Usage

To generate a syllabus prompt for a specific learning path, you can use the `prompts` module:

```python
from src.syllabus.prompts import generate_syllabus_prompt

prompt = generate_syllabus_prompt("web_development")
print(prompt)
```