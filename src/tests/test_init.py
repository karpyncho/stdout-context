import sys

from karpyncho.stdout_context import TestCaseStdoutMixin
from unittest import TestCase


class TestPrint(TestCase, TestCaseStdoutMixin):
    def test_assert_stdout(self):
        with self.assertStdout("test\n"):
            print("test")

    def test_assert_stdout_prints(self):
        with self.assertStdoutPrints("test1", "test2", "test3"):
            print("test1")
            print("test2")
            pass
            print("test3")

    def test_assert_stdout_using_write(self):
        with self.assertStdout("test\n"):
            sys.stdout.write("test\n")

    def test_assert_stdout_not_stderr(self):
        with self.assertStdout(""):
            sys.stderr.write("test\n")

    def test_assert_stdout_contains(self):
        with self.assertStdoutContains("xxxx"):
            print("test1")
            print("xxxx")
            print("test3")

    def test_assert_stdout_contains_one_line(self):
        with self.assertStdoutContains("mytest"):
            print("test1 mytest test2")

    def test_assert_stdout_contains_one_line_fails(self):
        with self.assertRaises(AssertionError):
            with self.assertStdoutContains("blah blah"):
                print("test1 mytest test2")

    def test_assert_stdout_contains_several_lines(self):
        with self.assertStdoutContains("mytest",  "test1"):
            print("test1 mytest test2")

    def test_assert_stdout_contains_several_lines_fails(self):
        with self.assertRaises(AssertionError):
            with self.assertStdoutContains("mytest", "blah blah"):
                print("test1 mytest test2")

    def test_assert_stdout_regex(self):
        with self.assertStdoutRegex(r'^a+b+c+$'):
            print("aaaaaaaaaaaaaaaaaabbbbbbbbbbbbbbbbbbccccccccccccc")
