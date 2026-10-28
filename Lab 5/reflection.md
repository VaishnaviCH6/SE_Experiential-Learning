
# Lab 5: Static Code Analysis — Reflection

## 1. What is static code analysis?

Static code analysis examines source code without executing it. It helps identify potential bugs, security vulnerabilities, and coding-style violations.

## 2. What did Pylint, Bandit, and Flake8 identify?

Pylint identified code-quality issues, including a mutable default argument, missing docstrings, an unused import, and unsafe use of eval(). Bandit flagged eval() as a potential security risk. Flake8 identified formatting issues such as excessive line length and missing blank lines.

## 3. How were the issues resolved?

The code was updated to use safer numeric input parsing, explicit exception handling, UTF-8 file encoding, context managers, documented functions, and consistent formatting. Negative meter readings and adjustments were also rejected.

## 4. How does static analysis improve software quality?

Static analysis helps detect problems early, improve readability, reduce security risks, and make code easier to maintain. Using multiple tools provides complementary checks for quality, security, and style.
