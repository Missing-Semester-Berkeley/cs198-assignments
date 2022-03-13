import os
import os.path
import stat
import subprocess
import unittest
import hashlib
import urllib.request as request

MAKEFILE_EXPECTED_DELETED_FILES = ["paper.log", "paper.pdf", "paper.aux"]
GITHUB_PAGE = "github_page"
SURVEY = "survey"
SURVEY_HASHES = ["501d3c7ba1f345cb471551b55390d497", "d00a8c8ae014d7de47486dd2fba69fee"]
PRE_COMMIT = "pre-commit"


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
    def test_1_make_clean(self):
        execute_command("make")
        execute_command("make clean")
        out2 = execute_command("make clean")
        assert len(out2.stderr) == 0, "Makefile should not error even if run twice. If you're using `rm`, are you using the right flags?"
        for file in MAKEFILE_EXPECTED_DELETED_FILES:
            assert not os.path.isfile(file), f"File '{file}' was not deleted"

    def test_2_github_page(self):
        assert os.path.isfile(GITHUB_PAGE), f"File '{GITHUB_PAGE}' does not exist"
        with open(GITHUB_PAGE) as f:
            url = f.readlines()[0]
            try:
                r = request.urlopen(url)
            except:
                assert False, "Opening URL failed. Are you using https:// ?"
            assert 200 <= r.status < 300, "Opening URL failed."

    def test_3_makehook(self):
        assert os.path.isfile(PRE_COMMIT), f"File '{PRE_COMMIT}' does not exist"
        out = execute_file(f"./{PRE_COMMIT}")
        assert len(out.stderr) == 0, "Pre-commit hook should not error."

        execute_command("mv Makefile Makefile.old")  # Simulate deleting Makefile
        out2 = execute_file(f"./{PRE_COMMIT}")

        execute_command("mv Makefile.old Makefile")
        assert len(out2.stderr) == 0, "Pre-commit hook should have errored, but didn't."

    def test_4_survey(self):
        assert os.path.isfile(SURVEY), f"File '{SURVEY}' does not exist"
        with open(SURVEY) as f:
            content = strip_spaces_and_newlines(f.read())
            hashed = hashlib.md5(content.encode()).hexdigest()
            assert hashed in SURVEY_HASHES, "Incorrect survey code."
