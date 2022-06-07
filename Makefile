-include .env
export

req-update:
	python -m piptools compile --generate-hashes requirements.in --output-file requirements.txt

req-install:
	python -m pip install --upgrade setuptools
	python -m piptools sync requirements.txt

run:
	python main.py

lint:
	pylint app
