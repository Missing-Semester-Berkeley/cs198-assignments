import os
import os.path
import stat
import subprocess
import unittest
import hashlib
import urllib.request as request

ENTROPY = "entropy"
SYM = "sym"
ASYM = "asym"

ENTROPY_1_HASHES = ["3295c76acbf4caaed33c36b1b5fc2cb1", "73b4c20e598d6b495de7515ad4ea2fdc"]
ENTROPY_2_HASHES = ["08c61f3fd48f12fa7c88a7f5fd01df3d", "642e92efb79421734881b53e1e1b18b6"]
ENTROPY_3_HASHES = ["c4ca4238a0b923820dcc509a6f75849b", "b026324c6904b2a9cb4b88d6d61c81d1"]
SYM_HASHES = ["4469e3363b1eff424f3030a804c8ca97", "18692e2c6e26165c09ccc3461f49c7eb"]
ASYM_HASHES = ["5a4a69c14595264736c65d2338993ea5", "c98514c98db99241bf2db7e37c077940"]


def strip_spaces_and_newlines(s):
    return s.strip().replace("\n", "").replace("\r", "")


def execute_file(filename, timeout=None):
    st = os.stat(filename)
    assert os.path.isfile(filename), f"File '{filename}' does not exist"
    assert bool(st.st_mode & stat.S_IXUSR), f"File '{filename}' is not executable"
    return subprocess.run(filename, capture_output=True, shell=True, timeout=timeout)


def execute_command(command, timeout=None):
    return subprocess.run(command, capture_output=True, shell=True, timeout=timeout)


class HW08(unittest.TestCase):
    def test_1_entropy_1(self):
        with open(ENTROPY) as f:
            line_1 = strip_spaces_and_newlines(f.readlines()[0])
            hashed = hashlib.md5(line_1.encode()).hexdigest()
            assert hashed in ENTROPY_1_HASHES, "Incorrect entropy line 1."

    def test_1_entropy_2(self):
        with open(ENTROPY) as f:
            line_2 = strip_spaces_and_newlines(f.readlines()[1])
            hashed = hashlib.md5(line_2.encode()).hexdigest()
            assert hashed in ENTROPY_2_HASHES, "Incorrect entropy line 2."

    def test_1_entropy_3(self):
        with open(ENTROPY) as f:
            line_3 = strip_spaces_and_newlines(f.readlines()[2])
            hashed = hashlib.md5(line_3.encode()).hexdigest()
            assert hashed in ENTROPY_3_HASHES, "Incorrect entropy line 3."

    def test_2_sym(self):
        with open(SYM) as f:
            content = strip_spaces_and_newlines(f.readlines()[0])
            hashed = hashlib.md5(content.encode()).hexdigest()
            assert hashed in SYM_HASHES, "Incorrect sym."

    def test_3_sym(self):
        with open(ASYM) as f:
            content = strip_spaces_and_newlines(f.readlines()[0])
            hashed = hashlib.md5(content.encode()).hexdigest()
            assert hashed in ASYM_HASHES, "Incorrect asym."
