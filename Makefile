.PHONY: help install dev test lint format clean build docker release

help:
	@echo "🎮 FreeLauncher - Development Commands"
	@echo "========================================"
	@echo ""
	@echo "Installation:"
	@echo "  make install     - Install dependencies"
	@echo "  make dev         - Install dev dependencies"
	@echo ""
	@echo "Development:"
	@echo "  make run         - Run the application"
	@echo "  make test        - Run tests"
	@echo "  make lint        - Run linting checks"
	@echo "  make format      - Format code with black"
	@echo ""
	@echo "Build & Release:"
	@echo "  make build       - Build distributions (wheel, source)"
	@echo "  make docker      - Build Docker image"
	@echo "  make release     - Full release build"
	@echo ""
	@echo "Cleanup:"
	@echo "  make clean       - Remove build artifacts"
	@echo "  make clean-all   - Remove all generated files"

install:
	python -m pip install -r requirements.txt

dev:
	python -m pip install -r requirements.txt
	python -m pip install pytest pytest-cov black flake8 mypy wheel build

run:
	python main.py

test:
	pytest tests/ -v --tb=short

coverage:
	pytest tests/ --cov=src --cov-report=html --cov-report=term

lint:
	flake8 src/ main.py --count --select=E9,F63,F7,F82 --show-source --statistics
	mypy src/ --ignore-missing-imports || true

format:
	black src/ main.py tests/

build: clean
	python scripts/build.py --dist

docker:
	python scripts/build.py --skip-tests --skip-lint

release: clean
	python scripts/build.py --all

clean:
	rm -rf build/ dist/ *.egg-info/ .pytest_cache/ .coverage htmlcov/ .mypy_cache/

clean-all: clean
	rm -rf venv/ .venv/ __pycache__/ .DS_Store
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete

docker-build:
	docker build -t freelauncher:latest .

docker-run:
	docker-compose up -d

docker-stop:
	docker-compose down

docker-logs:
	docker-compose logs -f

docker-clean:
	docker-compose down -v
	docker image rm freelauncher:latest || true

docker-push:
	@echo "Pushing Docker image (requires Docker credentials)"
	docker push freelauncher:latest

init:
	git config core.hooksPath .git/hooks 2>/dev/null || true

version:
	python setup.py --version 2>/dev/null || echo "Version not found in setup.py"

.DEFAULT_GOAL := help
