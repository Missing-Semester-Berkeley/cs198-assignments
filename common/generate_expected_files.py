import sys

assert len(sys.argv) == 3, "Expected input/output file parameter"

CP_FILE = """cp /autograder/submission/{file} /autograder/source/{file}"""
CHMOD_FILE = """chmod +x /autograder/source/{file}"""
SETUP_UTILITY = """which {binary} && ln -s $(which {binary}) /usr/bin/g{binary}"""

FORMAT = """\
#!/usr/bin/env bash

# Set up autograder files

{CP_FILES}

{CHMOD_FILES}

{SETUP_UTILITIES}

cd /autograder/source

python3.8 run_tests.py generate_gradescope
"""

GNU_BINARIES = [
    "[", "b2sum", "base32", "base64", "basename", "basenc", "cat", "chcon", "chgrp", "chmod", "chown", "chroot", "cksum", "comm", "cp", "csplit", "cut", "date", "dd", "df", "dir", "dircolors", "dirname", "du", "echo", "env", "expand", "expr", "factor", "false", "fmt", "fold", "groups", "head", "hostid", "id", "install", "join", "kill", "link", "ln", "logname", "ls", "md5sum", "mkdir", "mkfifo", "mknod", "mktemp", "mv", "nice", "nl", "nohup", "nproc", "numfmt", "od", "paste", "pathchk", "pinky", "pr", "printenv", "printf", "ptx", "pwd", "readlink", "realpath", "rm", "rmdir", "runcon", "seq", "sha1sum", "sha224sum", "sha256sum", "sha384sum", "sha512sum", "shred", "shuf", "sleep", "sort", "split", "stat", "stdbuf", "stty", "sum", "sync", "tac", "tail", "tee", "test", "timeout", "touch", "tr", "true", "truncate", "tsort", "tty", "uname", "unexpand", "uniq", "unlink", "uptime", "users", "vdir", "wc", "who", "whoami", "yes", "ed", "red", "awk", "egrep", "fgrep", "grep", "sed", "tar", "make", "find", "xargs"
]

cp_files = []
chmod_files = []
setup_utilities = [SETUP_UTILITY.format(binary=binary) for binary in GNU_BINARIES]

with open(sys.argv[1], "r") as f:
    for file_line in f.readlines():
        file_parts = file_line.split()
        print(file_parts)
        if len(file_parts) == 2:  # Set executable bit
            assert file_parts[1] == "x"  # Executable bit
            chmod_files.append(CHMOD_FILE.format(file=file_parts[0]))
        cp_files.append(CP_FILE.format(file=file_parts[0]))

with open(sys.argv[2], "w") as f:
    f.write(FORMAT.format(
        CP_FILES="\n".join(cp_files),
        CHMOD_FILES="\n".join(chmod_files),
        SETUP_UTILITIES="\n".join(setup_utilities)
    ))
