import os
import os.path
import unittest

SEMESTER_FILENAME = "semester"
LAST_MODIFIED_FILENAME = "last-modified.txt"

EXPECTED_CONTENTS = [
    "#!/bin/sh",
    "curl --head --silent https://cs198.org/"
]


def strip_spaces_and_newlines(s):
    return s.strip().replace("\n", "").replace("\r", "")


class HW00(unittest.TestCase):
    def test_1_free(self):
        return

    def test_2_touch(self):
        assert os.path.isfile(SEMESTER_FILENAME), f"File '{SEMESTER_FILENAME}' does not exist"

    def test_3_semester_contents(self):
        with open(SEMESTER_FILENAME) as f:
            lines = f.readlines()
            assert len(lines) >= 2, f"File '{SEMESTER_FILENAME}' contains too few lines"
            assert strip_spaces_and_newlines(lines[0]) == EXPECTED_CONTENTS[0], f"File '{SEMESTER_FILENAME}' contains an incorrect first line"
            assert strip_spaces_and_newlines(lines[1]) == EXPECTED_CONTENTS[1], f"File '{SEMESTER_FILENAME}' contains an incorrect second line"

    def test_4_execution(self):
        return
        # st = os.stat(SEMESTER_FILENAME)
        # assert bool(st.st_mode & stat.S_IXUSR), f"File '{SEMESTER_FILENAME}' is not executable"  # Check user-executable

    def test_5_last_modified(self):
        assert os.path.isfile(LAST_MODIFIED_FILENAME), f"File '{LAST_MODIFIED_FILENAME}' does not exist."
        with open(LAST_MODIFIED_FILENAME) as f:
            contents = f.read().strip().lower()
            assert contents.startswith("last-modified:"), f"File '{LAST_MODIFIED_FILENAME}' does not start with 'last-modified:'"
