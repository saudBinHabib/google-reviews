clean:
	find src -type d -name "__pycache__" -exec rm -rf {} + > /dev/null 2>&1
	find src -type f -name "*.pyc" -exec rm -rf {} + > /dev/null 2>&1

	find tests -type d -name "__pycache__" -exec rm -rf {} + > /dev/null 2>&1
	find tests -type f -name "*.pyc" -exec rm -rf {} + > /dev/null 2>&1

lint:
	flake8 --show-source src
	isort --check-only -rc src --diff

	flake8 --show-source setup.py
	isort --check-only setup.py --diff

all: clean lint