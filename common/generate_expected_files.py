import sys

assert len(sys.argv) == 3, "Expected input/output file parameter"

CP_FILE = """cp /autograder/submission/{file} /autograder/source/{file}"""

CHMOD_FILE = """chmod +x /autograder/source/{file}"""

FORMAT = """\
#!/usr/bin/env bash

# Set up autograder files

{CP_FILES}

{CHMOD_FILES}

cd /autograder/source

python3 run_tests.py generate_gradescope
"""

cp_files = []
chmod_files = []

with open(sys.argv[1], "r") as f:
    for file_line in f.readlines():
        file_parts = file_line.split()
        print(file_parts)
        if len(file_parts) == 2:  # Set executable bit
            assert file_parts[1] == "x"  # Executable bit
            chmod_files.append(CHMOD_FILE.format(file=file_parts[0]))
        cp_files.append(CP_FILE.format(file=file_parts[0]))

with open(sys.argv[2], "w") as f:
    f.write(FORMAT.format(CP_FILES="\n".join(cp_files), CHMOD_FILES="\n".join(chmod_files)))
