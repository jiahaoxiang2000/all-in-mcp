# Changelog

All notable changes to this project will be documented in this file.

---

## [Unreleased]

---

## [0.3.1] - 2025-08-26

### 📚 Documentation

- 📝 docs: update README.md with environment variable configuration examples
- 📝 docs: add comprehensive server options and MCP client integration examples

---

## [0.3.0] - 2025-08-26

### 🚀 Features

- 🚀 feat: migrate to FastMCP architecture with modular APaper design
- ✨ feat: update README with APaper research direction image and bump version to 0.2.8

### 🔧 Fixes & Improvements

- 🔧 refactor: migrate to ProxyClient architecture and fix imports

### 📚 Documentation

- 📚 docs: update README for FastMCP architecture and MCP Inspector
- 📝 docs: reorganize CHANGELOG.md for better readability

### 🏗️ Maintenance

- bump version to 0.2.8

---

## [0.2.7] - 2025-06-27

- 🔧 chore: update version to 0.2.7 in pyproject.toml
- ✨ feat: add year filtering options to IACR search functionality (Add the years rang function for IACR paper search #3)
- 📚 docs: add Copilot instructions for project guidelines and utilities
- 📚 docs: update Python version requirement to 3.10 in README

## [0.2.6] - 2025-06-27

- 🔧 chore: update version to 0.2.6 in pyproject.toml
- 📚 docs: update README for clarity and formatting improvements
- 📚 docs: update README to clarify available tools and installation instructions
- ♻️ refactor: remove PDF download and reading methods from CrossrefSearcher and update related tests
- 🔧 chore: update version to 0.2.5 in uv.lock (to test the `crossref.py` read & download function #4)
- ♻️ refactor: clean up Makefile by removing unused commands and comments

## [0.2.5] - 2025-06-22

- 🔧 chore: update version to 0.2.5 in pyproject.toml
- ✨ feat: implement Crossref searcher functionality and add tests

## [0.2.4] - 2025-06-22

- 🔧 chore: update version to 0.2.4 in pyproject.toml
- ✨ feat: implement Google Scholar search functionality and update documentation
- ✨ feat: add PDF reading functionality and update README

## [0.2.2] - 2025-06-21

- 🔧 chore: update version to 0.2.2 in pyproject.toml
- 🔧 chore: update version to 0.2.1 in pyproject.toml
- 🔧 chore: update version to 0.2.0 in pyproject.toml
- ✨ feat: add year range filtering to CryptoBib search functionality
- 📚 docs: enhance README with CryptoBib search capabilities and integration details
- ✨ feat: add CryptoBib search functionality and documentation

## [0.1.4] - 2025-06-21

- 🔧 chore: update version to 0.1.4 and change twine installation method
- 📚 docs: update release process in README and remove git hooks documentation
- Simplify git hooks and bump version to 0.1.3
- Add helper script for creating releases
- Add git hooks for automatic tagging on version changes
- Bump version to 0.1.2 for testing git hooks
- ✨ feat: implement GitHub Actions for automated release and publishing to PyPI
- Merge remote changes and resolve conflicts
- ♻️ refactor: remove base64 encoding tool and related tests from MCP server
- ✨ feat: add Makefile for All-in-MCP server with setup, testing, and cleaning commands

## [0.1.0] - 2025-06-18/19

- Refactor code structure for improved readability and maintainability
- ♻️ refactor: remove Base64 encoding tool and update IACR search demo in MCP server
- 📚 docs: remove outdated documentation files and add PyPI publishing setup guide
- ♻️ refactor: remove outdated IACR search test script and improve abstract extraction logic (the abstract is still truncated #1)
- ✨ feat: enhance abstract extraction with multiple strategies and add detailed search result tests
- ✨ feat: add demo and test scripts for IACR paper search functionality
- feat: Add Paper data model and IACR search tools
- 📚 docs: remove outdated integration and test documentation
- 📚 docs: add comprehensive documentation for installation, configuration, integration, and testing
- 📚 docs: update README to streamline utility tools section and correct project structure
- 📚 docs: update test coverage section in README.md
- ✨ feat: enhance project with Base64 encoding tools and testing framework
- Refactor code structure for improved readability and maintainability

---
