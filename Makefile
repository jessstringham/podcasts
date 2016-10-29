PREFIX=venv/bin

clean:
	rm -r venv
	find . -name \*.pyc  | xargs rm -v

test: venv
	$(MAKE) pytest
	$(MAKE) check_types
	$(PREFIX)/pre-commit run --all-files

pytest: venv
	$(PREFIX)/python -m pytest tests -s --cov=podcast --cov-report term-missing

check_types: venv
	MYPYPATH=podcast $(PREFIX)/mypy podcast --disallow-untyped-defs
	MYPYPATH=podcast:tests $(PREFIX)/mypy tests --check-untyped-defs

venv-init:
	virtualenv venv -p python3

venv: requirements.txt
	$(PREFIX)/pip install -r requirements.txt

dev: venv
	$(PREFIX)/pre-commit install
