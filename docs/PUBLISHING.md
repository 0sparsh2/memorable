# Publishing to PyPI

This guide explains how to publish Memorable to PyPI so users can install it with `pip install memorable`.

## Prerequisites

1. **PyPI Accounts**:
   - Create account on [PyPI](https://pypi.org/account/register/)
   - Create account on [Test PyPI](https://test.pypi.org/account/register/) (for testing)

2. **API Tokens**:
   - Log in to PyPI → Account Settings → API tokens
   - Create a new API token (scope: entire account)
   - Save the token (starts with `pypi-`)

3. **Required Tools**:
   ```bash
   pip install build twine
   ```

## Publishing Steps

### 1. Test on Test PyPI First

Always test on Test PyPI before publishing to production PyPI:

```bash
# Build the package
python -m build

# Upload to Test PyPI
twine upload --repository testpypi dist/*

# Test installation from Test PyPI
pip install --index-url https://test.pypi.org/simple/ memorable
```

### 2. Publish to Production PyPI

Once tested, publish to production PyPI:

```bash
# Build the package (if not already built)
python -m build

# Check the package
twine check dist/*

# Upload to PyPI
twine upload dist/*
```

### 3. Verify Installation

After publishing, verify it works:

```bash
# Uninstall any existing version
pip uninstall memorable -y

# Install from PyPI
pip install memorable

# Verify it works
python -c "import memorable; print(memorable.__version__)"
```

## Automated Publishing with GitHub Actions

We have automated publishing set up via GitHub Actions (see `.github/workflows/publish.yml`).

To trigger a release:

1. Update version in `setup.py` and `pyproject.toml`
2. Create a git tag:
   ```bash
   git tag v0.1.0
   git push origin v0.1.0
   ```
3. GitHub Actions will automatically:
   - Build the package
   - Upload to PyPI
   - Create a GitHub release

## Version Management

Update version in two places before each release:

1. `setup.py`: `version="0.1.0"`
2. `pyproject.toml`: `version = "0.1.0"`

Follow [Semantic Versioning](https://semver.org/):
- `MAJOR.MINOR.PATCH` (e.g., `0.1.0`)
- Increment MAJOR for breaking changes
- Increment MINOR for new features (backward compatible)
- Increment PATCH for bug fixes

## Checklist Before Publishing

- [ ] Update version in `setup.py` and `pyproject.toml`
- [ ] Update `CHANGELOG.md` with new release notes
- [ ] Run tests: `make test`
- [ ] Run linter: `make lint`
- [ ] Build package: `python -m build`
- [ ] Check package: `twine check dist/*`
- [ ] Test on Test PyPI first
- [ ] Create git tag for version
- [ ] Push tag to GitHub (triggers automated publish)

## Post-Publication

After publishing:

1. Verify package is live: https://pypi.org/project/memorable/
2. Update README.md installation instructions
3. Announce the release (GitHub release notes, social media, etc.)

## Troubleshooting

### Package name already exists

If "memorable" is taken on PyPI, you'll need to use a different name:
- `memorable-ai`
- `memorable-memory`
- `memorable-engine`

Update `name` in `setup.py` and `pyproject.toml`.

### Authentication errors

Make sure your API token is set correctly:
```bash
# Using environment variable
export TWINE_USERNAME=__token__
export TWINE_PASSWORD=pypi-YourTokenHere

# Or use keyring
pip install keyring
keyring set https://upload.pypi.org/legacy/ __token__
# Enter your token when prompted
```

### Package validation errors

Run `twine check dist/*` to catch issues before uploading:
- Missing metadata
- Invalid file paths
- Unreadable files

