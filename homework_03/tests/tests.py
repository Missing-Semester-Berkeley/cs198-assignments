import os
import os.path
import stat
import subprocess
import unittest

Q2 = "q2.txt"
WORDS = "words.txt"
SED = "sed.txt"


def strip_spaces_and_newlines(s):
    return s.strip().replace("\n", "").replace("\r", "")


def execute_file(filename, timeout=None):
    st = os.stat(filename)
    assert os.path.isfile(filename), f"File '{filename}' does not exist"
    assert bool(st.st_mode & stat.S_IXUSR), f"File '{filename}' is not executable"
    return subprocess.run(filename, capture_output=True, shell=True, timeout=timeout)


def execute_command(command, timeout=None):
    return subprocess.run(command, capture_output=True, shell=True, timeout=timeout)


class HW03(unittest.TestCase):
    def test_1_(self):
        return

    def test_2_part1(self):
        assert os.path.isfile(Q2), f"File '{Q2} does not exist'"
        assert os.path.isfile(WORDS), f"File '{WORDS} does not exist'"

        with open(Q2) as q2:
            lines = list(q2.readlines())
            assert len(lines) >= 2, f"There are only {len(lines)} in {Q2}, but expected 2."

            line_one = int(lines[0])

        with open(WORDS) as words:
            num_words = 0

            for word in words.readlines():
                word = strip_spaces_and_newlines(word).lower()
                if word.count("a") >= 3 and word[-2:] != "'s":
                    num_words += 1

            assert num_words == line_one, "The number of words was incorrect. (line 1 of q2.txt)"

    def test_2_part2(self):
        assert os.path.isfile(Q2), f"File '{Q2} does not exist'"
        assert os.path.isfile(WORDS), f"File '{WORDS} does not exist'"

        with open(Q2) as q2:
            lines = list(q2.readlines())
            assert len(lines) >= 2, f"There are only {len(lines)} in {Q2}, but expected 2."

            word_one = strip_spaces_and_newlines(lines[1])
            word_two = strip_spaces_and_newlines(lines[2])
            word_three = strip_spaces_and_newlines(lines[3])

        with open(WORDS) as words:
            last_counts = {}

            for word in words.readlines():
                word = strip_spaces_and_newlines(word).lower()
                if word.count("a") >= 3 and word[-2:] != "'s":
                    last_two = word[-2:]
                    if last_two in last_counts:
                        last_counts[last_two] += 1
                    else:
                        last_counts[last_two] = 1

            sorted_counts = sorted(last_counts, key=lambda k: last_counts[k], reverse=True)
            assert sorted_counts[0] == word_one, "The first word is incorrect. (line 2 of q2.txt)"
            assert sorted_counts[1] == word_two, "The second word is incorrect. (line 3 of q2.txt)"
            assert sorted_counts[2] == word_three, "The third word is incorrect. (line 4 of q2.txt)"

    def test_3_sed(self):
        with open(SED) as f:
            assert len(f.read().split()) > 10, "Please write more than a sentence."
