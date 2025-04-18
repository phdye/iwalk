NAME = iwalk
FILES={Makefile,setup.py,src,tests}

# ,scripts/mk-toxenv,tox.ini,.toxenv}

PYTHON = python3
TEST_DIR = tests

ERRORS=/dn/errors.txt

.PHONY: all check test clean layout tar input itest pytest

all: clear-errors check test

check:
	@echo "Checking Python scripts for syntax..."
	@for f in src/$(NAME)/*.py; do \
	  echo "  $$f"; \
	  $(PYTHON) -m py_compile $$f || exit 1; \
	done

# 3.x
pytest: clear-errors
	PYTHONPATH=.:${PYxTHONPATH} err -a pytest tests

itest: clear-errors test

test: clear-errors test-27 test-32

test-27:
	@ # err -a bash -xc "export PYTHONPATH=$$(pwd)/src:$${PYTHONPATH} ; $(PYTHON) -m unittest discover -s tests"
	@ # bash -xc "export PYTHONPATH=$$(pwd):$${PYTHONPATH} && $(PYTHON) -m unittest discover -s tests"
	@ err -a bash -xc "export PYTHONPATH=$$(pwd)/src:$${PYTHONPATH} ; pytest -s -v tests"

test-32:
	@ err -a bash -cx "PYTHONPATH=$$(pwd)/src python3.2 -m pytest -s -v tests"

test-39:
	@ err -a bash -cx "PYTHONPATH=$$(pwd)/src python3.9 -m pytest -s -v tests"

test-py3:
	@ err -a bash -cx "PYTHONPATH=$$(pwd)/src python3 -m pytest -s -v tests"

no-args noargs:
	@ bash -xc "export PYTHONPATH=$$(pwd):$${PYTHONPATH} && err use-case/stree.py"

cx clear-errors:
	rm -f $(ERRORS)

clean:
	@ echo "Cleaning up..."
	rm -f env.json vars.json $(ERRORS) .errors.*
	rm -rf build dist
	find . -name '*.pyc'               -delete
	find . -name '__pycache__'         | xargs rm -rf
	find . -name '*.egg-info'          | xargs rm -rf

dist-clean: clean
	@ echo "Cleaning up..."
	rm -rf build dist

tar: clean
	( cd .. ; tar cvfJ /dn/${NAME}.tar.xz --exclude="*/__pycache__" ${NAME}/${FILES} )

layout:
	@ stree $$(echo ${FILES} | tr , ' ') | tee doc/layout.txt
