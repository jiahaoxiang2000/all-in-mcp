# Copilot Instructions

<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

This is an MCP (Model Context Protocol) server project that provides daily-use utility functions as MCP services.

## Project Guidelines

- This project uses UV for modern Python dependency management
- Follow MCP server patterns and conventions
- Use async/await for all server handlers
- Implement proper error handling and validation
- Use type hints throughout the codebase
- Follow the MCP specification for tools, resources, and prompts

## MCP Server Information

You can find more info and examples at:

- https://modelcontextprotocol.io/llms-full.txt
- https://github.com/modelcontextprotocol/create-python-server

## Daily Utilities Focus

This server provides practical daily-use functions including:

- Text processing utilities
- File operations
- Date/time utilities
- System information
- Network utilities
- String manipulation
- Data conversion utilities

When adding new tools, ensure they are:

- Safe to execute
- Well-documented
- Properly validated
- Useful for daily tasks
