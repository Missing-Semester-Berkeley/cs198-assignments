import os
import os.path
import stat
import subprocess
import unittest

EXPECTED_FIZZBUZZ = """\
def fizz_buzz(limit):
    for i in range(1, limit):
        if i % 3 == 0:
            print('fizz', end='')
        if i % 5 == 0:
            print('buzz', end='')
        if i % 3 and i % 5:
            print(i)
        else:
            print()

def main():
    fizz_buzz(10)

main()
"""

DEMO_FILENAME = "demo.py"
ITEMS_FILENAME = "items"
DEBUG_FAILING_COMMAND = "debug_failing_command.sh"
DEBUG_FAILING_COMMAND_OUTPUT = "out.txt"
TAR_HTML = "tar_html.sh"
TAR_HTML_TARBALL = "archive.tar.gz"


def strip_spaces_and_newlines(s):
    return s.strip().replace("\n", "").replace("\r", "")


def execute_file(filename, timeout=None):
    st = os.stat(filename)
    assert os.path.isfile(filename), f"File '{filename}' does not exist"
    assert bool(st.st_mode & stat.S_IXUSR), f"File '{filename}' is not executable"
    return subprocess.run(filename, capture_output=True, shell=True, timeout=timeout)


def execute_command(command, timeout=None):
    return subprocess.run(command, capture_output=True, shell=True, timeout=timeout)


class HW02(unittest.TestCase):
    def test_1_fizzbuzz(self):
        assert os.path.isfile(DEMO_FILENAME), f"File '{DEMO_FILENAME}' does not exist"
        with open(DEMO_FILENAME) as f:
            text = f.read()
            assert text == EXPECTED_FIZZBUZZ, "Fizzbuzz text does not match expected."
