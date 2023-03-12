# Karpyncho Stdout-Context

## Goal

This package main goal is to extend unittest to be able to make assertions on what was printed in the console (StdOut) 

## Install

```sh
pip install karpyncho_stdout_context
```

https://pypi.org/project/stdout-stderr-capturing/

## TestCaseStdoutMixin

Once the package is installed TestCaseStdoutMixin can be used along unittest.TestCase or django.test.TestCase as multiple inheritance mixin.

```python
from unittest import TestCase

from karpyncho.stdout_context import TestCaseStdoutMixin


class TestMyClass(TestCase, TestCaseStdoutMixin):

    def test_assert_stdout_contains(self):
        with self.assertStdoutContains("xxxx"):
            print("test1")
            print("xxxx")
            print("test3")
```

When the context ends, the assertion will be checked

## Available assertions

### assertStdout(expected_output)

will assert that the context will finish writing exactly expected_output in console 

### assertStdoutPrints(line1, line2, ...)

is the same as assertStdout but passing each line 

### assertStdoutContains(*expected_output)

will assert that each string in the expected_output tuple is a substring of the console output

### assertStdoutRegex(regex)

will assert that the console output matches with the provided regex

## Future improvements

 * Stderr Management
 * context capturing of stdout/stderr returning the text, not forcing an assertion creating the context
 * capturing decorators