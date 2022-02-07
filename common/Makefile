autograder.zip: run_autograder
	zip -j autograder.zip ../common/requirements.txt ../common/run_tests.py ../common/setup.sh
	zip -u -r autograder.zip tests run_autograder -x "**/*__pycache__*" 
	test -f extra_autograder_files && { cat extra_autograder_files | xargs zip -u autograder.zip; } || echo 'No extra autograder files found.'

run_autograder: expected_files.txt
	python ../common/generate_expected_files.py $< $@

all: autograder.zip

.PHONY: clean
clean:
	rm run_autograder autograder.zip
