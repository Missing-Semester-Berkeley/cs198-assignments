import os
import os.path
import stat
import subprocess
import unittest
import socket
import time
import signal

SERVER = "server.py"
port = 20000


def strip_spaces_and_newlines(s):
    return s.strip().replace("\n", "").replace("\r", "")


def execute_file(filename, timeout=None):
    st = os.stat(filename)
    assert os.path.isfile(filename), f"File '{filename}' does not exist"
    assert bool(st.st_mode & stat.S_IXUSR), f"File '{filename}' is not executable"
    return subprocess.run(filename, capture_output=True, shell=True, timeout=timeout)


def execute_command(command, timeout=None):
    return subprocess.run(command, capture_output=True, shell=True, timeout=timeout)


def with_timeout(timeout=5):
    def inner(f):
        def handle_timeout(signum, frame):
            raise TimeoutError("***Test timed out.***")

        def f_with_alarm(*args, **kwargs):
            signal.signal(signal.SIGALRM, handle_timeout)
            signal.alarm(timeout)

            f(*args, **kwargs)
            signal.alarm(0)
        return f_with_alarm
    return inner


class HW10(unittest.TestCase):
    def setUp(self):
        global port
        self.server = subprocess.Popen(["python3", SERVER], env=dict(os.environ, **{"PORT": f"{port}"}))
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        time.sleep(1)  # Wait for server to start
        self.sock.connect(("localhost", port))
        self.buffer = ""
        port += 1

    def tearDown(self):
        print()
        print("DEBUG[client][CLEANUP]")
        self.sock.send("EXT".encode())
        self.sock.close()

    def recv(self, expected_message, error_message):
        print("DEBUG[client][TRYING TO RECEIVE]:", expected_message)

        try:
            while len(self.buffer) < len(expected_message):
                self.buffer += self.sock.recv(2048).decode()
        except TimeoutError as e:
            print(e)
            print("DEBUG[client][RECEIVED]", self.buffer)
            print("DEBUG[client][BUT WANTED]", expected_message)

        received, self.buffer = self.buffer[:len(expected_message)], self.buffer[len(expected_message):]
        assert received == expected_message, error_message

    def send(self, message):
        print()
        print("DEBUG[client][SENDING]:", message)
        self.sock.send(message.encode())

    @with_timeout(5)
    def test_1_gli(self):
        self.send("GLI")
        self.recv("LEVI", "Default queue should be ['LEVI']")

    @with_timeout(5)
    def test_2_add(self):
        self.send("ADD EZRA")
        self.recv("OK", "Adding new user should not result in error")

        self.send("ADD OWEN")
        self.recv("OK", "Adding new user should not result in error")

        self.send("ADD OWEN")
        self.recv("ERROR", "Double-adding user should result in error")

        self.send("GLI")
        self.recv("LEVI EZRA OWEN", "Name list mismatch after adding EZRA and OWEN")

    @with_timeout(5)
    def test_3_aap(self):
        self.send("ADD EZRA")
        self.recv("OK", "Adding new user should not result in error")

        self.send("AAP OWEN 1")
        self.recv("OK", "Adding new user should not result in error")

        self.send("AAP OWEN 1")
        self.recv("ERROR", "Double-adding user should result in error")

        self.send("GLI")
        self.recv("LEVI OWEN EZRA", "Name list mismatch after adding EZRA and OWEN")

    @with_timeout(5)
    def test_4_rmv(self):
        self.send("ADD EZRA")
        self.recv("OK", "Adding new user should not result in error")

        self.send("AAP OWEN 1")
        self.recv("OK", "Adding new user should not result in error")

        self.send("GLI")
        self.recv("LEVI OWEN EZRA", "Name list mismatch after adding EZRA and OWEN")

        self.send("RMV EZRA")
        self.recv("OK", "Removing existing user should not result in error")

        self.send("RMV EZRA")
        self.recv("ERROR", "Removing nonexisting user should result in error")

        self.send("GLI")
        self.recv("LEVI OWEN", "Name list mismatch after removing EZRA ")

    @with_timeout(5)
    def test_5_upd(self):
        self.send("ADD EZRA")
        self.recv("OK", "Adding new user should not result in error")

        self.send("AAP OWEN 1")
        self.recv("OK", "Adding new user should not result in error")

        self.send("GLI")
        self.recv("LEVI OWEN EZRA", "Name list mismatch after adding EZRA and OWEN")

        self.send("UPD OWEN 2")
        self.recv("OK", "Updating existing user should not result in error")

        self.send("UPD EVAN 3")
        self.recv("ERROR", "Updating nonexisting user should result in error")

        self.send("GLI")
        self.recv("LEVI EZRA OWEN", "Name list mismatch after removing EZRA ")

    @with_timeout(10)
    def test_6_get(self):
        self.send("ADD EZRA")
        self.recv("OK", "Adding new user should not result in error")

        self.send("AAP OWEN 1")
        self.recv("OK", "Adding new user should not result in error")

        self.send("GLI")
        self.recv("LEVI OWEN EZRA", "Name list mismatch after adding EZRA and OWEN")

        self.send("GET EZRA")
        self.recv("2", "Getting existing user should give back their position")

        self.send("GET EZRA")
        self.recv("2", "Getting existing user should give back their position")

        self.send("GLI")
        self.recv("LEVI OWEN EZRA", "Name list mismatch after getting position of EZRA")

        self.send("GET EVAN")
        self.recv("ERROR", "Getting nonexisting user should error")
