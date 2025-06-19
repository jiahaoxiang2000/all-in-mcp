#!/usr/bin/env python3
"""
Release helper script for all-in-mcp

This script helps automate the release process by:
1. Updating the version in pyproject.toml
2. Creating a git tag
3. Pushing the tag to trigger CI/CD
"""

import re
import sys
import subprocess
from pathlib import Path


def get_current_version():
    """Get the current version from pyproject.toml"""
    pyproject_path = Path("pyproject.toml")
    if not pyproject_path.exists():
        print("Error: pyproject.toml not found")
        sys.exit(1)
    
    content = pyproject_path.read_text()
    match = re.search(r'version\s*=\s*"([^"]+)"', content)
    if not match:
        print("Error: Could not find version in pyproject.toml")
        sys.exit(1)
    
    return match.group(1)


def update_version(new_version):
    """Update the version in pyproject.toml"""
    pyproject_path = Path("pyproject.toml")
    content = pyproject_path.read_text()
    
    # Replace the version
    new_content = re.sub(
        r'version\s*=\s*"[^"]+"',
        f'version = "{new_version}"',
        content
    )
    
    pyproject_path.write_text(new_content)
    print(f"Updated version to {new_version} in pyproject.toml")


def run_command(cmd, check=True):
    """Run a shell command"""
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, check=False)
    if check and result.returncode != 0:
        print(f"Command failed with return code {result.returncode}")
        sys.exit(1)
    return result


def main():
    if len(sys.argv) != 2:
        print("Usage: python scripts/release.py <new_version>")
        print("Example: python scripts/release.py 0.1.1")
        sys.exit(1)
    
    new_version = sys.argv[1]
    
    # Validate version format (basic check)
    if not re.match(r'^\d+\.\d+\.\d+$', new_version):
        print("Error: Version should be in format X.Y.Z (e.g., 0.1.1)")
        sys.exit(1)
    
    current_version = get_current_version()
    print(f"Current version: {current_version}")
    print(f"New version: {new_version}")
    
    # Confirm with user
    response = input("Continue? (y/N): ")
    if response.lower() != 'y':
        print("Aborted")
        sys.exit(0)
    
    # Update version
    update_version(new_version)
    
    # Check if we have uncommitted changes
    result = run_command(["git", "status", "--porcelain"], check=False)
    if result.returncode == 0:
        # Add and commit the version change
        run_command(["git", "add", "pyproject.toml"])
        run_command(["git", "commit", "-m", f"Bump version to {new_version}"])
        print("Committed version update")
    
    # Create and push tag
    tag_name = f"v{new_version}"
    run_command(["git", "tag", tag_name])
    print(f"Created tag {tag_name}")
    
    # Push changes and tag
    run_command(["git", "push"])
    run_command(["git", "push", "origin", tag_name])
    print(f"Pushed tag {tag_name}")
    
    print(f"\nRelease {new_version} initiated!")
    print("Check GitHub Actions for build and publish status:")
    print("https://github.com/jiahaoxiang2000/all-in-mcp/actions")


if __name__ == "__main__":
    main()
