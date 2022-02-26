import os
import os.path
import stat
import subprocess
import unittest
import signal
import time
import hashlib

HANDLERS = "./handlers.py"
ALIASES = "aliases"
BANDIT = "bandit0_password"
EXPECTED_HASH = ["4b2cd20485a2d813d47ef5dd5e40018c", "db850479aee144057b8fc49ec97aee99"]
DOTFILE = "chosen_dotfile"


def strip_spaces_and_newlines(s):
    return s.strip().replace("\n", "").replace("\r", "")


def execute_file(filename, timeout=None):
    st = os.stat(filename)
    assert os.path.isfile(filename), f"File '{filename}' does not exist"
    assert bool(st.st_mode & stat.S_IXUSR), f"File '{filename}' is not executable"
    return subprocess.run(filename, capture_output=True, shell=True, timeout=timeout)


def execute_command(command, timeout=None):
    return subprocess.run(command, capture_output=True, shell=True, timeout=timeout)


class HW04(unittest.TestCase):
    def test_1_handlers(self):
        assert os.path.isfile(HANDLERS), f"File '{HANDLERS} does not exist'"
        p = subprocess.Popen([HANDLERS], stdout=subprocess.PIPE)
        try:
            time.sleep(1)  # Race condition: setup signal handlers.
            p.send_signal(signal.SIGINT)
            time.sleep(1)  # Race condition: signal.pause()
            p.send_signal(signal.SIGTERM)

            outs, errs = p.communicate(timeout=2)
            outs = outs.decode().split("\n")

            assert errs is None, f"There were errors in {HANDLERS}"
            assert outs[0] == "Caught interruption", "Did not get 'Caught interruption' after SIGINT was sent."
            assert outs[1] == "Terminating", "Did not get 'Terminating' after SIGTERM was sent."
        except subprocess.TimeoutExpired:
            p.kill()
            assert False, "The program did not terminate after SIGTERM. Are you handling signals correctly?"

    def test_2_aliases(self):
        assert os.path.isfile(ALIASES), f"File '{ALIASES}' does not exist"
        res = execute_file("./test_dc").stdout.decode().split()

        assert res[0] == "/", "dc failed to work."

    def test_3_bandit(self):
        assert os.path.isfile(BANDIT), f"File '{BANDIT}' does not exist"
        with open(BANDIT) as f:
            content = f.read()
            hashed = hashlib.md5(content.encode()).hexdigest()
            assert hashed in EXPECTED_HASH, "Incorrect password."

    def test_4_dotfile(self):
        assert os.path.isfile(DOTFILE), f"File '{DOTFILE}' does not exist"
        with open(DOTFILE) as f:
            dotfile = f.read().strip()
            assert os.path.isfile(dotfile), f"File '{dotfile}' does not exist"
            with open(dotfile) as g:
                assert len(g.read()) > 0, f"'{dotfile}' is empty"
