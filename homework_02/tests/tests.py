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
ITEMS_NUMBERED_FILENAME = "items_numbered"
EXAMPLE_DATA = "example-data.json"
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

    def test_2_items(self):
        assert os.path.isfile(ITEMS_FILENAME), f"File '{ITEMS_FILENAME} does not exist'"
        assert os.path.isfile(ITEMS_NUMBERED_FILENAME), f"File '{ITEMS_NUMBERED_FILENAME} does not exist'"

        with open(ITEMS_FILENAME) as orig:
            with open(ITEMS_NUMBERED_FILENAME) as new:
                orig_lines = orig.readlines()
                new_lines = new.readlines()

                for (i, (orig_line, new_line)) in enumerate(zip(orig_lines, new_lines)):
                    orig_line = strip_spaces_and_newlines(orig_line)
                    new_line = strip_spaces_and_newlines(new_line)
                    assert f"{i+1}. {orig_line}" == new_line, f"{i+1}. {orig_line} and {new_line} differ"

    def test_3_data(self):
        from expected_data import data
        import json
        with open(EXAMPLE_DATA) as f:
            user_data = json.load(f)
            assert len(user_data) == len(data), \
                f"Expected {len(data)} lines but got {len(user_data)} lines."

            for user_item, expected_item in zip(user_data, data):
                assert user_item["name"] == expected_item["name"], \
                    f"Name does not match: Got {user_item['name']} but expected {expected_item['name']}"
                assert user_item["email"] == expected_item["email"], \
                    f"Email does not match: Got {user_item['email']} but expected {expected_item['email']}"
