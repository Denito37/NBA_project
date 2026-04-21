---
name: test-review
description: create new test cases or review current test cases and suggest new test to improve code coverage
---

When creating good unit test in Pytest for a Python function make sure to:


### Test Standards

1. test the behavior of functions under many possible inputs/edge cases
2. set up mock data to simulate the function in action
3. Mock extrernal dependencies such as api calls
4. verify that the actual outcome matches the expected result
5. follow the arrange-act-assert structural pattern
