all: build

build:
	python setup.py sdist bdist

clean:
	rm -rf fictionary.egg-info build

distclean: clean
	rm -rf dist data

.PHONY: all build clean distclean
