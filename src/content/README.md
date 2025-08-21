# Content & Curriculum Layer

This module handles the flat, remixable content.

## Example Usage

To generate static HTML from Markdown content, you can use the `static_site_generator` module:

```python
from src.content.static_site_generator import generate_static_html

markdown_content = """
# My Course Title

This is the **introduction** to my course.

## Section 1

- Item 1
- Item 2
"""

html_output = generate_static_html(markdown_content)
print(html_output)
```