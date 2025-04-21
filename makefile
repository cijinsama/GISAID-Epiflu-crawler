install: clean
	pip install .
test-install:
	pip install -e .
clean:
	rm -rf build src/*.egg-info tmp download
	find . -name "__pycache__" -type d | xargs rm -rf
.PHONY: clean install
