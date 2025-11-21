.PHONY: install install-dev test test-cov lint format clean build docs

install:
	pip install -r requirements.txt
	pip install -e .

install-dev:
	pip install -r requirements.txt
	pip install -e ".[dev]"

test:
	pytest tests/ -v

test-cov:
	pytest tests/ --cov=memorable_ai --cov-report=html --cov-report=term-missing

lint:
	flake8 memorable_ai tests examples
	mypy memorable_ai

format:
	black memorable_ai tests examples benchmarks
	isort memorable_ai tests examples benchmarks

clean:
	find . -type d -name __pycache__ -exec rm -r {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.db" -delete
	find . -type d -name "*.egg-info" -exec rm -r {} +
	find . -type d -name ".pytest_cache" -exec rm -r {} +
	find . -type d -name ".coverage" -exec rm -r {} +
	find . -type d -name "htmlcov" -exec rm -r {} +

build:
	python setup.py sdist bdist_wheel

docs:
	@echo "Documentation is in docs/ directory"
	@echo "See README.md for main documentation"

benchmark:
	python -m pytest benchmarks/ -v

benchmark-locomo:
	python -m pytest benchmarks/locomo/ -v

benchmark-multihop:
	python -m pytest benchmarks/multihop/ -v

benchmark-temporal:
	python -m pytest benchmarks/temporal/ -v

benchmark-comparison:
	python -m pytest benchmarks/comparison/ -v

