"""
Author: Sebastian Quiles
Based on:
https://stackoverflow.com/questions/33767627/python-write-unittest-for-console-print/46307456#46307456
"""
import io
import sys
from enum import Enum
from typing import Tuple


class _AssertType(Enum):
    """internal enum Types of assertions"""
    EQ = "Equals"
    IN = "In"
    REGEX = "Regex"


class _AssertStdoutContext:
    """"internal Context Class to use it in a with context block"""

    def __init__(self, test_case, assert_type: _AssertType, output_expected: Tuple[str] | str):
        """constructor, testcase is the TestCase original instance, output_expected is the expected
        output on quiting the context"""
        self.test_case = test_case
        self.expected = output_expected
        self.captured = io.StringIO()
        self.assert_type = assert_type

    def __enter__(self):
        """"when the context begin, this method will hook stdout"""
        sys.stdout = self.captured
        return self

    def __exit__(self, exception_type, exception_value, exception_traceback):
        """"where the context finishes, stdout will be unhooked, and final assert is performed"""
        sys.stdout = sys.__stdout__
        captured = self.captured.getvalue()
        if self.assert_type == _AssertType.EQ:
            self.test_case.assertEqual(captured, self.expected)
        elif self.assert_type == _AssertType.IN:
            # pylint: disable=expression-not-assigned
            [self.test_case.assertIn(expected_text, captured) for expected_text in self.expected]
            # pylint: enable=expression-not-assigned
        elif self.assert_type == _AssertType.REGEX:
            self.test_case.assertRegex(captured, self.expected)


class TestCaseStdoutMixin:
    """Class to use as a Mixin Class along django.test.Testcase or unitest.Testcase"""

    def assertStdout(self, expected_output: str):  # noqa: N802 # pylint: disable=invalid-name
        """"method to test if the expected_output is exactly what was streamed in stdout"""
        return _AssertStdoutContext(self, _AssertType.EQ, expected_output)

    def assertStdoutPrints(self, *expected_output: Tuple[str] | str):  # noqa: N802 # pylint: disable=invalid-name
        """"method to test if a list of strings, (*expected_output) is exactly what was
        streamed in stdout separated with /n"""
        expected_output = "\n".join(expected_output) + "\n"
        return _AssertStdoutContext(self, _AssertType.EQ, expected_output)

    def assertStdoutContains(self, *expected_output: Tuple[str] | str):  # noqa: N802 # pylint: disable=invalid-name
        """"method to test if a list of expected_output was printed in stdout"""
        return _AssertStdoutContext(self, _AssertType.IN, *expected_output)

    def assertStdoutRegex(self, expected_regex_output: str):  # noqa: N802 # pylint: disable=invalid-name
        """"method to test if expected_regex_output match with stdout"""
        return _AssertStdoutContext(self, _AssertType.REGEX, expected_regex_output)
