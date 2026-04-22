install:
	pip install -r requirements.txt

run:
	python main.py

test:
	pytest tests/ -v

lint:
	flake8 . --max-line-length=100 --exclude=.venv
