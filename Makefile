PREFIX=venv/bin/

clean:
	rm -r venv
	find . -name \*.pyc  | xargs rm -v

test: venv
	$(MAKE) pytest
	MYPYPATH=podcast $(PREFIX)/mypy podcast --disallow-untyped-defs -s
	MYPYPATH=podcast:tests $(PREFIX)/mypy tests -s
	$(PREFIX)/pre-commit run --all-files

pytest: venv
	$(PREFIX)/python -m pytest tests -s


venv: requirements.txt
	virtualenv venv -p python3.5
	$(PREFIX)/pip install -r requirements.txt

dev: venv
	$(PREFIX)/pre-commit install
