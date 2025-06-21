# Git Hooks for Automatic Tagging

This repository includes git hooks that automatically create git tags when the version in `pyproject.toml` is changed.

## How It Works

The git hooks consist of two scripts:

### 1. Pre-commit Hook (`.git/hooks/pre-commit`)

- **Triggers**: Before each commit
- **Function**: Detects if `pyproject.toml` is being modified
- **Validation**:
  - Checks if the version follows semantic versioning format (X.Y.Z)
  - Ensures the tag doesn't already exist
  - Stores the new version for the post-commit hook

### 2. Post-commit Hook (`.git/hooks/post-commit`)

- **Triggers**: After a successful commit
- **Function**: Creates a git tag if a version change was detected
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
pyproject.toml is being modified, checking for version changes...
Version change detected: 0.1.2 -> 0.1.3
Will create tag v0.1.3 after successful commit
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

```text
Warning: Tag v0.1.3 already exists!
Please use a different version number or delete the existing tag.
```

**Solution**: Either increment the version number or delete the existing tag:

```bash
git tag -d v0.1.3  # Delete local tag
git push origin --delete v0.1.3  # Delete remote tag (if pushed)
```

### Invalid Version Format Error

```text
Error: Version format should be X.Y.Z (e.g., 0.1.1)
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
