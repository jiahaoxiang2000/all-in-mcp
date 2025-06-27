# Makefile for All-in-MCP Server
# MCP (Model Context Protocol) server providing daily-use utility functions

.PHONY: help install install-dev install-system install-all sync clean test lint format run build check dev-setup pre-commit

# Default target
.DEFAULT_GOAL := help

# Colors for output
BLUE := \033[34m
GREEN := \033[32m
YELLOW := \033[33m
RED := \033[31m
RESET := \033[0m

help: ## Show this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(GREEN)%-20s$(RESET) %s\n", $$1, $$2}'

# Environment Setup
install: ## Install dependencies using uv
	@echo "$(BLUE)Installing dependencies...$(RESET)"
	uv sync

install-dev: ## Install development dependencies
	@echo "$(BLUE)Installing development dependencies...$(RESET)"
	uv sync --extra dev

install-system: ## Install with system dependencies (psutil)
	@echo "$(BLUE)Installing with system dependencies...$(RESET)"
	uv sync --extra system

install-all: ## Install all dependencies (dev + system)
	@echo "$(BLUE)Installing all dependencies...$(RESET)"
	uv sync --extra dev --extra system --extra all

sync: ## Sync dependencies (equivalent to install)
	@echo "$(BLUE)Syncing dependencies...$(RESET)"
	uv sync

# Development Setup
dev-setup: install-all ## Complete development environment setup
	@echo "$(GREEN)Development environment setup complete!$(RESET)"
	@echo "$(YELLOW)You can now run:$(RESET)"
	@echo "  make run    - to start the MCP server"
	@echo "  make test   - to run tests"

# Testing
test: ## Run tests with pytest
	@echo "$(BLUE)Running tests...$(RESET)"
	uv run pytest

test-verbose: ## Run tests with verbose output
	@echo "$(BLUE)Running tests (verbose)...$(RESET)"
	uv run pytest -v

# Running the Server
run: ## Run the All-in-MCP server
	@echo "$(BLUE)Starting All-in-MCP server...$(RESET)"
	uv run all-in-mcp

run-debug: ## Run server with debug output
	@echo "$(BLUE)Starting All-in-MCP server (debug mode)...$(RESET)"
	uv run python -m all_in_mcp

# Building and Distribution
build: ## Build the package
	@echo "$(BLUE)Building package...$(RESET)"
	uv build

# Testing Server Import
test-import: ## Test that the server imports correctly
	@echo "$(BLUE)Testing server import...$(RESET)"
	uv run python -c "import all_in_mcp; print('All-in-MCP server imports successfully')"

# Cleaning
clean: ## Clean build artifacts and cache
	@echo "$(BLUE)Cleaning build artifacts...$(RESET)"
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf __pycache__/
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name ".coverage" -delete
	rm -rf htmlcov/

clean-all: clean ## Clean everything including uv cache
	@echo "$(BLUE)Cleaning all caches...$(RESET)"
	uv cache clean

# Quick development workflow
dev: dev-setup test-import run ## Complete dev setup and run server

# Show project status
status: ## Show project status
	@echo "$(BLUE)All-in-MCP Project Status:$(RESET)"
	@echo "$(YELLOW)Project structure:$(RESET)"
	@find . -name "*.py" | head -10
	@echo "$(YELLOW)Available tasks:$(RESET)"
	@echo "  - Text processing utilities"
	@echo "  - IACR ePrint Archive integration"
	@echo "  - PDF processing capabilities"
	@echo "$(YELLOW)Dependencies status:$(RESET)"
	@uv tree --quiet 2>/dev/null || echo "Dependencies not installed - run 'make install'"
