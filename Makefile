.PHONY: help install dev test lint format build clean release

help: ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install the package
	uv pip install -e .

dev: ## Install development dependencies
	uv pip install -e ".[dev]"

test: ## Run tests
	pytest

lint: ## Run linting
	flake8 budgt
	mypy budgt

format: ## Format code
	black budgt

build: ## Build the package
	python -m build

clean: ## Clean build artifacts
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

release: clean build ## Build and check package for release
	python -m twine check dist/*
	@echo "Ready for release! Run 'twine upload dist/*' to publish to PyPI"

run: ## Run the application
	budgt

# Homebrew formula update (manual process)
update-homebrew: ## Instructions for updating Homebrew formula
	@echo "To update Homebrew formula:"
	@echo "1. Update the URL and SHA256 in HomebrewFormula/budgt-sh.rb"
	@echo "2. Test with: brew install --build-from-source ./HomebrewFormula/budgt-sh.rb"
	@echo "3. Submit PR to homebrew-core or create your own tap"
	@echo ""
	@echo "Current version: 0.1.0"
