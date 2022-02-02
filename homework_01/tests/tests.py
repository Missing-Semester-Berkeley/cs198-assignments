import os
import os.path
import unittest

MYLS_FILENAME = "myls"
MARCO_FILENAME = "marco.sh"
DEBUG_FAILING_COMMAND = "debug_failing_command.sh"
DEBUG_FAILING_COMMAND_OUTPUT = "out.txt"
TAR_HTML = "tar_html.sh"
TAR_HTML_TARBALL = "archive.tar.gz"


def strip_spaces_and_newlines(s):
    return s.strip().replace("\n", "").replace("\r", "")


class HW01(unittest.TestCase):
    def test_1_myls(self):
        assert os.path.isfile(MYLS_FILENAME), f"File '{MYLS_FILENAME}' does not exist"
        with open(MYLS_FILENAME) as f:
            lines = [line for line in f.readlines() if len(line) > 1]  # Filter out 'intentional' line (non-whitespace)
            assert len(lines) >= 1, f"File '{SEMESTER_FILENAME}' contains too few lines"
            assert strip_spaces_and_newlines(lines[-1])[:len("ls")] == "ls", f"File '{MYLS_FILENAME}' does not contain an ls command"

    def test_2_marco(self):
        import subprocess
        assert os.path.isfile(MARCO_FILENAME), f"File '{MARCO_FILENAME}' does not exist"
        res = subprocess.run("./test_marco", capture_output=True, shell=True).stdout.decode().split()

        assert len(res) == 2, "There were more than 2 lines of output in test_marco. This is a bug!"
        assert res[0] == res[1], f"""Marco and polo do not result in the same directories. Compare:
    Before Marco: {res[0]}
    After  Polo : {res[1]}
"""

    def test_3_debug_failing_command(self):
        import subprocess
        assert os.path.isfile(DEBUG_FAILING_COMMAND), f"File '{DEBUG_FAILING_COMMAND}' does not exist"
        res = subprocess.run(f"./{DEBUG_FAILING_COMMAND}", capture_output=True, shell=True, timeout=3).stdout.decode().split("\n")

        assert "Something went wrong" in res, "Stdout was not captured"
        assert "The error was using magic numbers" in res, "Stderr was not captured"
        assert "Everything went according to plan" not in res, "Do not capture successful run outputs"

    def test_4_tar_html(self):
        import subprocess
        assert os.path.isfile(TAR_HTML), f"File '{TAR_HTML}' does not exist"
        res = subprocess.run(f"./{TAR_HTML}", capture_output=True, shell=True, timeout=3).stdout.decode().split("\n")
        assert os.path.isfile(TAR_HTML_TARBALL), f"Tarball '{TAR_HTML_TARBALL}' does not exist"
        res = subprocess.run(f"tar --list -f {TAR_HTML_TARBALL}", capture_output=True, shell=True, timeout=3).stdout.decode().split("\n")
        assert len(res) == 3, f"Expected 2 files but found {len(res)-1} in tarball."
