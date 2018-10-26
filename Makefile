all: build

build:
	python setup.py sdist bdist_wheel

clean:
	rm -rf fictionary.egg-info build .eggs .coverage.* htmlcov
	find . -name '*.pyc' -delete

distclean: clean
	rm -rf dist data

reallyclean: distclean
	rm -f src/fictionary/models/*.txt

coverage:
	coverage run setup.py test \
	&& coverage html \
	&& coverage report

data: src/fictionary/models/all.txt \
	src/fictionary/models/british.txt \
	src/fictionary/models/american.txt \
	src/fictionary/models/words.txt

src/fictionary/models/words.txt: ispell_wordlist/*.*
	./util/make_wordlist -o $@ $^

src/fictionary/models/all.txt: ispell_wordlist/*.*
	./util/make_model -o $@ $^

src/fictionary/models/british.txt: ispell_wordlist/english.* ispell_wordlist/british.*
	./util/make_model -o $@ $^

src/fictionary/models/american.txt: ispell_wordlist/english.* ispell_wordlist/american.*
	./util/make_model -o $@ $^

.PHONY: all build clean distclean reallyclean data
