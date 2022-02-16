install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt

lint:
	pylint app.py

test:
	python -m pytest -vv --cov=app --cov-report=term-missing test_app.py

all: install lint test