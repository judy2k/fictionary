all: build

build:
	python setup.py sdist bdist

clean:
	rm -rf fictionary.egg-info build .eggs .coverage.* htmlcov

distclean: clean
	rm -rf dist data

coverage:
	coverage run setup.py test \
	&& coverage html \
	&& coverage report

.PHONY: all build clean distclean
