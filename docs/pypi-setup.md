# PyPI Publishing Setup Guide

This guide explains how to set up automatic publishing to PyPI using GitHub Actions.

## Prerequisites

1. **PyPI Account**: You need a PyPI account at https://pypi.org
2. **GitHub Repository**: Your code should be hosted on GitHub
3. **Trusted Publishing**: Configure trusted publishing on PyPI (recommended)

## Setup Steps

### 1. Configure Trusted Publishing on PyPI

Trusted publishing is the modern, secure way to publish to PyPI without API tokens.

1. Go to https://pypi.org/manage/account/publishing/
2. Click "Add a new pending publisher"
3. Fill in the details:
   - **PyPI project name**: `all-in-mcp`
   - **Owner**: `jiahaoxiang2000` (your GitHub username)
   - **Repository name**: `all-in-mcp`
   - **Workflow name**: `release.yml`
   - **Environment name**: `release` (optional but recommended)

### 2. Create GitHub Environment (Optional but Recommended)

1. Go to your GitHub repository
2. Click Settings → Environments
3. Click "New environment"
4. Name it `release`
5. Add protection rules:
   - Required reviewers (optional)
   - Deployment branches: Only protected branches

### 3. Version Management

The workflow triggers on version tags. Update your version in `pyproject.toml`:

```toml
[project]
version = "0.1.1"  # Update this for each release
```

### 4. Creating a Release

To publish a new version:

1. **Update the version** in `pyproject.toml`
2. **Commit and push** your changes
3. **Create and push a tag**:
   ```bash
   git tag v0.1.1
   git push origin v0.1.1
   ```

The GitHub Action will automatically:

- Run tests on multiple Python versions
- Build the package
- Publish to PyPI
- Create a GitHub Release

## Alternative: Manual Token Setup (Not Recommended)

If you prefer using API tokens instead of trusted publishing:

1. Generate an API token on PyPI
2. Add it as a secret named `PYPI_API_TOKEN` in your GitHub repository
3. Modify the publish step in `.github/workflows/release.yml`:
   ```yaml
   - name: Publish to PyPI
     uses: pypa/gh-action-pypi-publish@release/v1
     with:
       password: ${{ secrets.PYPI_API_TOKEN }}
   ```

## Workflow Features

The release workflow includes:

- **Multi-version testing**: Tests on Python 3.9-3.12
- **Linting**: Runs ruff if available
- **Package validation**: Checks package integrity
- **Automatic releases**: Creates GitHub releases with artifacts
- **Security**: Uses trusted publishing (no secrets needed)

## Testing the Workflow

To test without publishing:

1. Create a test tag: `git tag test-v0.1.0`
2. Push it: `git push origin test-v0.1.0`
3. The workflow will run but won't publish (since PyPI project doesn't exist yet)

## Troubleshooting

### Common Issues

1. **"Project does not exist"**: Make sure you've registered the project name on PyPI
2. **"Trusted publishing not configured"**: Complete step 1 above
3. **"Tests failing"**: Check the CI logs for specific test failures
4. **"Build failing"**: Verify your `pyproject.toml` configuration

### Checking Workflow Status

1. Go to your GitHub repository
2. Click "Actions" tab
3. Look for your workflow run
4. Click on it to see detailed logs

## Manual Publishing (For Testing)

If you want to publish manually first:

```bash
# Install build tools
uv add --dev build twine

# Build the package
uv run python -m build

# Upload to PyPI (you'll need an API token)
uv run python -m twine upload dist/*
```

## Next Steps

After successful setup:

1. Consider adding badges to your README
2. Set up automated dependency updates with Dependabot
3. Add more comprehensive tests
4. Consider setting up documentation hosting
