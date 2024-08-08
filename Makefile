all: run

run:
	python main.py
test:
	unittest discover -v
coverage:
	coverage -m run unittest discover -v
	coverage -m report --skip-empty
mypy:
	mypy src main.py
pylint:
	pylint src main.py
format:
	black src/**/*.py main.py
populate:
	python scripts/populate_database.py
generate_imports:
	python scripts/generate_imports.py
create_venv:
	python3.11 -m venv .venv
	@(echo "source .venv/bin/activate to activate venv")
install_deps:
	pip install --upgrade pip
	pip install -r requirements.txt
	mypy --install-types --non-interactive > /dev/null
