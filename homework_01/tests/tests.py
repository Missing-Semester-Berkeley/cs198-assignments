import os
import os.path
import stat
import subprocess
import unittest

MYLS_FILENAME = "myls"
MARCO_FILENAME = "marco.sh"
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


class HW01(unittest.TestCase):
    def test_1_myls(self):
        assert os.path.isfile(MYLS_FILENAME), f"File '{MYLS_FILENAME}' does not exist"
        with open(MYLS_FILENAME) as f:
            lines = [line for line in f.readlines() if len(line) > 1]  # Filter out 'intentional' line (non-whitespace)
            assert len(lines) >= 1, f"File '{MYLS_FILENAME}' contains too few lines"
            first_word = strip_spaces_and_newlines(lines[-1]).split(" ")[0]
            assert first_word == "ls" or first_word == "gls", \
                f"File '{MYLS_FILENAME}' does not contain an (g)ls command"

    def test_2_marco(self):
        assert os.path.isfile(MARCO_FILENAME), f"File '{MARCO_FILENAME}' does not exist"
        res = execute_file("./test_marco").stdout.decode().split()

        assert len(res) == 2, "There were more than 2 lines of output in test_marco. This is a bug!"
        assert res[0] == res[1], f"""Marco and polo do not result in the same directories. Compare:
    Before Marco: {res[0]}
    After  Polo : {res[1]}
"""

    def test_3_debug_failing_command(self):
        res = execute_file(f"./{DEBUG_FAILING_COMMAND}", timeout=3).stdout.decode().split("\n")

        assert "Something went wrong" in res, "Stdout was not captured"
        assert "The error was using magic numbers" in res, "Stderr was not captured"
        assert "Everything went according to plan" not in res, "Do not capture successful run outputs"

    def test_4_tar_html(self):
        assert os.path.isfile(TAR_HTML), f"File '{TAR_HTML}' does not exist"
        res = execute_file(f"./{TAR_HTML}").stdout.decode().split("\n")
        assert os.path.isfile(TAR_HTML_TARBALL), f"Tarball '{TAR_HTML_TARBALL}' does not exist"
        res = execute_command(f"tar --list -f {TAR_HTML_TARBALL}").stdout.decode().split("\n")
        assert len(res) == 3, f"Expected 2 files but found {len(res)-1} in tarball."
