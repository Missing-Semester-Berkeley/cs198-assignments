import io
import sys
import unittest
import json

from gradescope_utils.autograder_utils.json_test_runner import JSONTestRunner

TESTCASE_FORMAT = "{number}. {name}: {score} / {max_score}"
TESTCASE_FORMAT_OUTPUT = "{number}. {name}: {score} / {max_score}\n{output}"


def print_formatted_test_results(contents):
    for testcase in contents['tests']:
        if "output" in testcase:
            print(TESTCASE_FORMAT_OUTPUT.format(number=testcase["number"], name=testcase["name"], score=testcase["score"], max_score=testcase["max_score"], output=testcase["output"]))
        else:
            print(TESTCASE_FORMAT.format(number=testcase["number"], name=testcase["name"], score=testcase["score"], max_score=testcase["max_score"]))


if __name__ == '__main__':
    suite = unittest.defaultTestLoader.discover('tests')
    if len(sys.argv) > 1 and sys.argv[1] == "generate_gradescope":
        with open('/autograder/results/results.json', 'w') as f:
            JSONTestRunner(visibility='visible', stream=f).run(suite)
    else:
        output = io.StringIO()
        JSONTestRunner(visibility='visible', stdout_visibility='visible', failfast=True, stream=output).run(suite)

        contents = json.loads(output.getvalue())
        output.close()

        print_formatted_test_results(contents)
