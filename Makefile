cli:
	python main.py test
tui:
	python main.py
watch_cli:
	find src/**/*.py | entr -ac python main.py test
watch_tui:
	find src/**/*.py | entr -ac python main.py
test:
	python -m unittest discover -v
watch_test:
	find tests/**/*.py | entr -ac python -m unittest discover -v
populate:
	python populate.py
