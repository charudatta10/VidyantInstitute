# Licensing Stack

This module handles the licensing framework for SageEduMint.

## Example Usage

### Apply PUCL-1.0 License

```python
from src.licensing.pucl import apply_pucl_license

confirmation = apply_pucl_license("my_new_course_content")
print(f"PUCL-1.0 Application Confirmation: {confirmation}")
```

### Apply Creative Commons License

```python
from src.licensing.cc import apply_creative_commons_license

confirmation = apply_creative_commons_license("my_module_design", "CC BY-NC-SA")
print(f"Creative Commons Application Confirmation: {confirmation}")
```

### Load License Tiers

```python
from src.licensing.cc import load_license_tiers

tiers = load_license_tiers()
print("Available License Tiers:")
for tier in tiers["tiers"]:
    print(f"- {tier["name"]}: {tier["license"]} ({tier["use_case"]})")
```