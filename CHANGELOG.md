## CHANGELOG: karpyncho-stdout-context

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

### [Unreleased]

#### Fixed - Documentation

 * fix in README.md changed title of the project
 * fix in README.md explaining changes of assertStdoutContains
 * fix CHANGELOG.md related to assertStdoutContains
 * fix CHANGELOG.md a few typos

#### Added - Test cases

 * added all test cases for failing assertions 
 
### [0.1.1] - 2023-03-12

#### Changed

 * assertStdoutContains(text1, text2, text3...) now supports several texts and all of them must be present in the console output to pass the assertion

### [0.1.0] - 2023-03-11

#### Features

 * `TestCaseStdoutMixin` mixin to be used as multiple inheritance| along a TestCase class
 * this mixin will provide the following assert methods to be used as a context
    + assertStdout(expected_output) will assert that the context will finish writing exactly expected_output in console
    + assertStdoutPrints(line1, line2, ...) is the same than assertStdout but passing each line
    + assertStdoutContains(expected_output) will assert that expected_output is a substring of the console output
    + assertStdoutRegex(regex) will assert that the console output matches with the provided regex