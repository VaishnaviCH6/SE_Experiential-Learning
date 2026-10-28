
# Lab 5: Static Code Analysis

## Issues Identified and Fixed

| Issue | Type | Original Line(s) | Description | Fix Approach |
|---|---|---:|---|---|
| Mutable default argument | Bug | 12 | The default list could be shared across calls. | Used an explicitly managed history list. |
| Unsafe eval() | Security | 63 | User input could execute arbitrary Python code. | Replaced eval() with numeric input parsing. |
| Bare exception | Code quality | 44 | The handler caught unspecified exceptions. | Added specific exception handling. |
| Unspecified file encoding | Code quality | 42, 48 | File operations did not explicitly specify encoding. | Used UTF-8 encoding. |
| Unmanaged file resources | Code quality | 42, 48 | Files were opened without context managers. | Used with statements. |
| Unused import | Style | 2 | The sys import was not used. | Removed the import. |
| Missing docstrings | Style | Multiple | Module and functions lacked documentation. | Added docstrings. |
| Excessive line length | Style | 24, 62 | Lines exceeded the 79-character limit. | Reformatted the affected lines. |
| Negative meter readings | Validation | 36 | Negative readings could result in negative bills. | Added validation for negative readings. |

## Verification Results

- Pylint: 10.00/10
- Bandit: No issues identified.
- Flake8: No violations reported.
