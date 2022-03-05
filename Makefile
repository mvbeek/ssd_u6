install:
	python3 -m pip install --upgrade pip &&\
		python3 -m pip install -r requirements.txt
		
sudo_install_redoc-cli:
	sudo apt-get update &&\
		sudo apt install npm &&\
		sudo npm install -g redoc-cli

lint:
	pylint *.py &&\
		pylint ./api

flake8:
	flake8 --format=html --htmldir='static/reports/' --statistics &&\
		mv static/reports/index.html static/reports/flake8_report.html

bandit:
	bandit -r . --configfile bandit.yaml

test:
	python3 -m pytest -vv --disable-pytest-warnings --html='./static/reports/pytest_report.html' --self-contained-html

document:
	redoc-cli bundle openapi.yaml &&\
		mv redoc-static.html static/documents/api-document.html

check:
	flake8 --format=html --htmldir='static/reports/' --statistics
	mv static/reports/index.html static/reports/flake8_report.html
	pylint *.py
	pylint ./api
	bandit -r . --configfile bandit.yaml
	python3 -m pytest -vv --disable-pytest-warnings --html='./static/reports/pytest_report.html' --self-contained-html
	redoc-cli bundle openapi.yaml
	mv redoc-static.html static/documents/api-document.html

# all: lint flake8 bandit