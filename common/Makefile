autograder.zip: run_autograder
	zip -j autograder.zip ../common/requirements.txt ../common/run_autograder ../common/run_tests.py ../common/setup.sh tests/__init__.py tests/tests.py

run_autograder: expected_files.txt
	python ../common/generate_expected_files.py $< $@

all: autograder.zip

.PHONY: clean
clean:
	rm run_autograder autograder.zip
