"""
Author: Sebastian Quiles
Based on:
https://stackoverflow.com/questions/33767627/python-write-unittest-for-console-print/46307456#46307456
"""
import io
import sys
from enum import Enum
from typing import Any


class AssertTypeEnum(Enum):
    """internal enum Types of assertions"""
    EQ = "Equals"
    IN = "In"
    REGEX = "Regex"


class AssertStdoutContext:
    """"internal Context Class to use it in a with context block"""

    def __init__(self, test_case: 'TestCaseStdoutMixin', assert_type: AssertTypeEnum, output_expected: Any):
        """constructor, testcase is the TestCase original instance, output_expected is the expected
        output on quiting the context"""
        self.test_case: TestCaseStdoutMixin = test_case
        self.expected: Any = output_expected
        self.captured: io.StringIO = io.StringIO()
        self.assert_type: AssertTypeEnum = assert_type

    def __enter__(self) -> 'AssertStdoutContext':
        """"when the context begin, this method will hook stdout"""
        sys.stdout = self.captured
        return self

    def __exit__(self, exception_type, exception_value, exception_traceback) -> Any:
        # assert methods duck typing (as they are present in the TestCase class) cannot be resolved by
        # mypy, because the way to do it is with Protocol, but Protocol has an __init__ method and
        # Pytest will collect only TestClasses that doesn't implement __init__
        """"where the context finishes, stdout will be unhooked, and final assert is performed"""
        sys.stdout = sys.__stdout__
        captured = self.captured.getvalue()
        if self.assert_type == AssertTypeEnum.EQ:
            self.test_case.assertEqual(captured, self.expected)  # type: ignore
        elif self.assert_type == AssertTypeEnum.IN:
            # pylint: disable=expression-not-assigned
            [self.test_case.assertIn(expected_text, captured) for expected_text in self.expected]  # type: ignore
            # pylint: enable=expression-not-assigned
        elif self.assert_type == AssertTypeEnum.REGEX:
            self.test_case.assertRegex(captured, self.expected)  # type: ignore


class TestCaseStdoutMixin:
    """Class to use as a Mixin Class along django.test.Testcase or unitest.Testcase"""

    # pylint: disable=invalid-name
    def assertStdout(self, expected_output: str) -> AssertStdoutContext:  # noqa: N802
        """"method to test if the expected_output is exactly what was streamed in stdout"""
        return AssertStdoutContext(self, AssertTypeEnum.EQ, expected_output)

    def assertStdoutPrints(self, *expected_output: Any) -> AssertStdoutContext:  # noqa: N802
        """"method to test if a list of strings, (*expected_output) is exactly what was
        streamed in stdout separated with /n"""
        _expected_output: str = "\n".join(expected_output) + "\n"
        return AssertStdoutContext(self, AssertTypeEnum.EQ, _expected_output)

    def assertStdoutContains(self, *expected_output: Any) -> AssertStdoutContext:  # noqa: N802
        """"method to test if a list of expected_output was printed in stdout"""
        return AssertStdoutContext(self, AssertTypeEnum.IN, expected_output)

    def assertStdoutRegex(self, expected_regex_output: str) -> AssertStdoutContext:  # noqa: N802
        """"method to test if expected_regex_output match with stdout"""
        return AssertStdoutContext(self, AssertTypeEnum.REGEX, expected_regex_output)
    # pylint: enable=invalid-name
