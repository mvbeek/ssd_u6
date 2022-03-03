install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt &&\
		npm install -g redoc-cli

lint:
	pylint *.py &&\
		pylint ./api

flake8:
	flake8 *.py

bandit:
	bandit -r . --configfile bandit.yaml

test:
	python -m pytest -vv --disable-pytest-warnings --html=pytest_report.html #--cov=app --cov-report=term-missing 

document:
	redoc-cli bundle openapi.yaml

check:
	flake8
	pylint *.py
	pylint ./api
	bandit -r . --configfile bandit.yaml
	python -m pytest -vv --disable-pytest-warnings --pytest_html=report.html #--cov=app --cov-report=term-missing 
	redoc-cli bundle openapi.yaml

# all: lint flake8 bandit