#!/bin/bash
# Helper script to create a new release by updating the version in pyproject.toml
# This will trigger the git hooks to automatically create tags

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to display usage
usage() {
    echo -e "${BLUE}Usage: $0 <new_version>${NC}"
    echo -e "${BLUE}Example: $0 0.1.2${NC}"
    echo ""
    echo "This script will:"
    echo "1. Update the version in pyproject.toml"
    echo "2. Commit the change (triggering git hooks)"
    echo "3. Git hooks will automatically create a tag"
    echo ""
    echo "Version format should be X.Y.Z (semantic versioning)"
}

# Check if version argument is provided
if [ $# -ne 1 ]; then
    echo -e "${RED}Error: Version number is required${NC}"
    usage
    exit 1
fi

NEW_VERSION=$1

# Validate version format
if [[ ! "$NEW_VERSION" =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
    echo -e "${RED}Error: Invalid version format. Use X.Y.Z (e.g., 0.1.2)${NC}"
    exit 1
fi

# Check if pyproject.toml exists
if [ ! -f "pyproject.toml" ]; then
    echo -e "${RED}Error: pyproject.toml not found. Run this script from the project root.${NC}"
    exit 1
fi

# Get current version
CURRENT_VERSION=$(grep -E '^version = ".*"$' pyproject.toml | sed 's/version = "\(.*\)"/\1/')

if [ -z "$CURRENT_VERSION" ]; then
    echo -e "${RED}Error: Could not find current version in pyproject.toml${NC}"
    exit 1
fi

echo -e "${BLUE}Current version: ${CURRENT_VERSION}${NC}"
echo -e "${BLUE}New version: ${NEW_VERSION}${NC}"

# Check if the version is actually different
if [ "$CURRENT_VERSION" = "$NEW_VERSION" ]; then
    echo -e "${YELLOW}Warning: New version is the same as current version${NC}"
    exit 1
fi

# Check if tag already exists
TAG_NAME="v$NEW_VERSION"
if git tag -l | grep -q "^$TAG_NAME$"; then
    echo -e "${RED}Error: Tag $TAG_NAME already exists${NC}"
    echo "Available tags:"
    git tag -l
    exit 1
fi

# Check for uncommitted changes
if [ -n "$(git status --porcelain)" ]; then
    echo -e "${YELLOW}Warning: You have uncommitted changes${NC}"
    git status --short
    echo ""
    read -p "Do you want to continue? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo -e "${YELLOW}Aborted${NC}"
        exit 1
    fi
fi

# Confirm with user
echo ""
read -p "Create release $NEW_VERSION? (y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${YELLOW}Aborted${NC}"
    exit 1
fi

echo -e "${BLUE}Updating version in pyproject.toml...${NC}"

# Update version in pyproject.toml
sed -i "s/version = \"$CURRENT_VERSION\"/version = \"$NEW_VERSION\"/" pyproject.toml

# Verify the change
NEW_VERSION_CHECK=$(grep -E '^version = ".*"$' pyproject.toml | sed 's/version = "\(.*\)"/\1/')
if [ "$NEW_VERSION_CHECK" != "$NEW_VERSION" ]; then
    echo -e "${RED}Error: Failed to update version in pyproject.toml${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Version updated in pyproject.toml${NC}"

# Stage and commit the change (this will trigger the git hooks)
echo -e "${BLUE}Committing version change...${NC}"
git add pyproject.toml
git commit -m "Bump version to $NEW_VERSION"

echo ""
echo -e "${GREEN}🎉 Release $NEW_VERSION created successfully!${NC}"
echo ""
echo -e "${BLUE}Next steps:${NC}"
echo "1. Push the changes and tag to remote:"
echo -e "   ${YELLOW}git push && git push origin $TAG_NAME${NC}"
echo ""
echo "2. Or push everything including all tags:"
echo -e "   ${YELLOW}git push --follow-tags${NC}"
echo ""
echo "3. Check the tag was created:"
echo -e "   ${YELLOW}git tag -l${NC}"
