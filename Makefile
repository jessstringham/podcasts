PREFIX=venv/bin

clean:
	rm -r venv
	find . -name \*.pyc  | xargs rm -v

test:
	$(MAKE) pytest
	$(MAKE) check_types
	$(PREFIX)/pre-commit run --all-files

pytest:
	$(PREFIX)/python -m pytest tests -s --cov=podcast --cov-report term-missing

check_types:
	MYPYPATH=stubs $(PREFIX)/mypy podcast --disallow-untyped-defs
	MYPYPATH=stubs $(PREFIX)/mypy tests --check-untyped-defs

venv:
	virtualenv venv -p python3

requirements: requirements.txt
	$(PREFIX)/pip install -r requirements.txt

dev: venv
	$(PREFIX)/pre-commit install
