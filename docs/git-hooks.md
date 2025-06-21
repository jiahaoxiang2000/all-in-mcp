# Git Hooks for Automatic Tagging

This repository includes git hooks that automatically create git tags when the version in `pyproject.toml` is changed.

## How It Works

The git hooks consist of two simple scripts:

### 1. Pre-commit Hook (`.git/hooks/pre-commit`)

- **Triggers**: Before each commit
- **Function**: Validates version format in `pyproject.toml`
- **Validation**: Ensures version follows semantic versioning format (X.Y.Z)

### 2. Post-commit Hook (`.git/hooks/post-commit`)

- **Triggers**: After a successful commit
- **Function**: Detects version changes and creates git tags automatically
- **Tag Format**: `v{version}` (e.g., `v0.1.2`)
- **Tag Message**: `Release version {version}`

## Usage

1. **Edit Version**: Simply change the version in `pyproject.toml`:

   ```toml
   [project]
   name = "all-in-mcp"
   version = "0.1.3"  # Changed from 0.1.2
   ```

2. **Commit Changes**: Commit the changes as usual:

   ```bash
   git add pyproject.toml
   git commit -m "Bump version to 0.1.3"
   ```

3. **Automatic Tag Creation**: The hooks will:
   - Detect the version change
   - Validate the version format
   - Create a git tag automatically
   - Show instructions for pushing the tag

## Example Output

```bash
$ git commit -m "Bump version to 0.1.3"
pyproject.toml is being modified, validating version format...
Version format validated: 0.1.3
Creating git tag: v0.1.3
✅ Successfully created tag: v0.1.3
📝 Tag message: Release version 0.1.3

To push the tag to remote repository, run:
  git push origin v0.1.3

Or to push all tags:
  git push --tags
```

## Push Tags to Remote

After the tag is created locally, push it to the remote repository:

```bash
# Push specific tag
git push origin v0.1.3

# Or push all tags
git push --tags
```

## Benefits

1. **Consistency**: Ensures every version change gets a corresponding git tag
2. **Automation**: No need to manually create tags
3. **Validation**: Prevents invalid version formats and duplicate tags
4. **Traceability**: Easy to track releases and version history

## Troubleshooting

### Hook Not Executing

- Ensure hooks are executable: `chmod +x .git/hooks/pre-commit .git/hooks/post-commit`
- Check if hooks exist in `.git/hooks/` directory

### Tag Already Exists Error

This error is now handled automatically - if a tag already exists, the hook will skip creating a duplicate tag and just inform you.

```text
Tag v0.1.3 already exists, skipping tag creation
```

### Invalid Version Format Error

```text
Error: Version format should be X.Y.Z (e.g., 0.1.1)
Found version: 0.1.1-beta
```

**Solution**: Use semantic versioning format (e.g., `1.0.0`, `0.2.5`, `2.1.3`)

## Integration with Release Process

This git hook system works well with:

- **CI/CD pipelines**: Triggered by git tags
- **Release scripts**: Can detect new tags for automated releases
- **Package publishing**: Automatic PyPI uploads on new tags
- **Changelog generation**: Based on git tags and commits

## Manual Tag Creation (If Needed)

If you need to create a tag manually (bypassing the hooks):

```bash
git tag -a v0.1.4 -m "Release version 0.1.4"
git push origin v0.1.4
```
