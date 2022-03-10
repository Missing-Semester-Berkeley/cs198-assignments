import os
import os.path
import stat
import subprocess
import unittest
import hashlib

FIZZBUZZ = "fizzbuzz.py"
COMMITS = "commits"
EXPECTED_HASH = [["5f84b17d9720fc1a6d28423a253e11e5"], ["20f057650ac381de1ae0c52d8b4de84a", "38e14ce3568e2c52db7d196be85d4d55"]]
ANSWER = "answer"
EXPECTED_ANSWER_HASH = ["4a255aebaf9a19799a8bae9e697ceec8", "9937bb9efc9b34c7d0bf06ca26e10442"]


def strip_spaces_and_newlines(s):
    return s.strip().replace("\n", "").replace("\r", "")


def execute_file(filename, timeout=None):
    st = os.stat(filename)
    assert os.path.isfile(filename), f"File '{filename}' does not exist"
    assert bool(st.st_mode & stat.S_IXUSR), f"File '{filename}' is not executable"
    return subprocess.run(filename, capture_output=True, shell=True, timeout=timeout)


def execute_command(command, timeout=None):
    return subprocess.run(command, capture_output=True, shell=True, timeout=timeout)


class HW05(unittest.TestCase):
    def test_1_fizzbuzz(self):
        res = execute_command(f"python {FIZZBUZZ}").stdout.decode().split()
        assert len(res) == 15, f"Expected 15 lines but found {len(res)} lines in output."
        assert res == ['1', '2', 'fizz', '4', 'buzz', 'fizz', '7', '8', 'fizz', 'buzz', '11', 'fizz', '13', '14', 'fizzbuzz']

    def test_2_commits(self):
        assert os.path.isfile(COMMITS), f"File '{COMMITS}' does not exist"
        with open(COMMITS) as f:
            content = f.readlines()
            for i, line in enumerate(content):
                hashed = hashlib.md5(line.encode()).hexdigest()
                assert hashed in EXPECTED_HASH[i], f"Incorrect git hash on line {i+1}."

    def test_3_answer(self):
        assert os.path.isfile(ANSWER), f"File '{ANSWER}' does not exist"
        with open(ANSWER) as f:
            content = strip_spaces_and_newlines(f.read())
            hashed = hashlib.md5(content.encode()).hexdigest()
            assert hashed in EXPECTED_ANSWER_HASH, "Incorrect password."
