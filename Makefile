install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt

lint:
	pylint *.py &&\
		pylint ./api

flake8:
	flake8 *.py

bandit:
	bandit -r .

test:
	python -m pytest -vv --cov=app --cov-report=term-missing test_app.py

check:
	flake8
	pylint *.py
	pylint ./api
	bandit -r .

# all: lint flake8 bandit