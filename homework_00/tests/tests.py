import os
import os.path
import stat
import unittest

from gradescope_utils.autograder_utils.decorators import weight, number

SEMESTER_FILENAME = "semester"
LAST_MODIFIED_FILENAME = "last-modified.txt"

EXPECTED_CONTENTS = [
    "#!/bin/sh",
    "curl --head --silent https://cs198.org/"
]


def strip_spaces_and_newlines(s):
    return s.strip().replace("\n", "").replace("\r", "")


class HW00(unittest.TestCase):
    @weight(1)
    @number("1")
    def test_1_free(self):
        return

    @weight(1)
    @number("2")
    def test_2_touch(self):
        assert os.path.isfile(SEMESTER_FILENAME), f"File '{SEMESTER_FILENAME}' does not exist"

    @weight(1)
    @number("3")
    def test_3_semester_contents(self):
        with open(SEMESTER_FILENAME) as f:
            lines = f.readlines()
            assert len(lines) >= 2, f"File '{SEMESTER_FILENAME}' contains too few lines"
            assert strip_spaces_and_newlines(lines[0]) == EXPECTED_CONTENTS[0], f"File '{SEMESTER_FILENAME}' contains an incorrect first line"
            assert strip_spaces_and_newlines(lines[1]) == EXPECTED_CONTENTS[1], f"File '{SEMESTER_FILENAME}' contains an incorrect second line"

    @weight(1)
    @number("4")
    def test_4_execution(self):
        st = os.stat(SEMESTER_FILENAME)
        assert bool(st.st_mode & stat.S_IXUSR), f"File '{SEMESTER_FILENAME}' is not executable"  # Check user-executable

    @weight(1)
    @number("5")
    def test_5_last_modified(self):
        assert os.path.isfile(LAST_MODIFIED_FILENAME), f"File '{LAST_MODIFIED_FILENAME}' does not exist."
        with open(LAST_MODIFIED_FILENAME) as f:
            contents = f.read().strip()
            assert contents.startswith("last-modified:"), f"File '{LAST_MODIFIED_FILENAME}' does not start with 'last-modified:'"
            assert contents.endswith("GMT"), f"File '{LAST_MODIFIED_FILENAME}' does not end with 'GMT'"
