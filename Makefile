.PHONY: setup test run run-dev run-prod run-atlas clean

setup:
	bash setup.sh

test:
	pytest

run-dev:
	ENV=dev python -m counter.entrypoints.webapp

run-prod:
	ENV=prod python -m counter.entrypoints.webapp

run-atlas:
	ENV=atlas python -m counter.entrypoints.webapp

clean:
	rm -rf .venv
	rm -rf __pycache__
	rm -rf counter/__pycache__
	rm -rf counter/*/__pycache__
	rm -rf tests/__pycache__
	rm -rf tests/*/__pycache__
