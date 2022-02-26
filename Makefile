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
	python -m pytest -vv --disable-pytest-warnings #--cov=app --cov-report=term-missing 

check:
	flake8
	pylint *.py
	pylint ./api
	bandit -r .
	python -m pytest -vv --disable-pytest-warnings #--cov=app --cov-report=term-missing 

# all: lint flake8 bandit