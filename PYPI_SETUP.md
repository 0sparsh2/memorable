# PyPI Publishing - Quick Setup Guide

This guide will help you publish Memorable to PyPI so users can `pip install memorable`.

## Step 1: Create PyPI Accounts (Manual - 5 minutes)

1. **Production PyPI**:
   - Go to: https://pypi.org/account/register/
   - Register with your email
   - Verify your email
   - Log in

2. **Test PyPI** (for testing before production):
   - Go to: https://test.pypi.org/account/register/
   - Register with your email (can use same as production)
   - Verify your email
   - Log in

## Step 2: Create API Tokens (Manual - 2 minutes)

### Production PyPI Token:
1. Log in to https://pypi.org
2. Go to: Account Settings → API tokens
3. Click "Add API token"
4. Name it: "memorable-publishing"
5. Scope: "Entire account"
6. Click "Add token"
7. **Copy the token immediately** (starts with `pypi-`)
8. Save it securely - you won't see it again!

### Test PyPI Token:
1. Log in to https://test.pypi.org
2. Go to: Account Settings → API tokens
3. Click "Add API token"
4. Name it: "memorable-test-publishing"
5. Scope: "Entire account"
6. Click "Add token"
7. **Copy the token immediately** (starts with `pypi-`)
8. Save it securely

## Step 3: Add Tokens to GitHub Secrets (Manual - 3 minutes)

1. Go to: https://github.com/0sparsh2/memorable/settings/secrets/actions
2. Click "New repository secret"
3. Name: `PYPI_API_TOKEN`
4. Value: Paste your production PyPI token
5. Click "Add secret"
6. Repeat for Test PyPI:
   - Name: `TEST_PYPI_API_TOKEN`
   - Value: Paste your test PyPI token

## Step 4: Test on Test PyPI (Run this command)

```bash
# Option A: Use the helper script
./scripts/publish_to_pypi.sh test

# Option B: Manual
python3 -m build
twine upload --repository testpypi dist/*
# Enter your test token when prompted
```

## Step 5: Verify Test Installation

```bash
pip install --index-url https://test.pypi.org/simple/ memorable
python3 -c "import memorable; print('✅ Memorable installed!')"
```

## Step 6: Publish to Production PyPI

### Option A: Automated (Recommended)
Once you've tested on Test PyPI:

```bash
# Update version if needed (in setup.py and pyproject.toml)
# Create a git tag
git tag v0.1.0
git push origin v0.1.0

# GitHub Actions will automatically publish!
```

### Option B: Manual
```bash
# Use the helper script
./scripts/publish_to_pypi.sh production

# Or manual
python3 -m build
twine upload dist/*
# Enter your production token when prompted
```

## Step 7: Verify Production Installation

```bash
pip install memorable
python3 -c "import memorable; print('✅ Memorable installed from PyPI!')"
```

## Checklist Before Publishing

- [ ] Version updated in `setup.py` and `pyproject.toml`
- [ ] All tests pass: `make test`
- [ ] Package builds successfully: `python3 -m build`
- [ ] Package checks pass: `twine check dist/*`
- [ ] Tested on Test PyPI first
- [ ] GitHub Secrets configured (for automated publishing)

## Troubleshooting

### Package name already exists
If "memorable" is taken, you'll need a different name:
- Update `name` in `setup.py` and `pyproject.toml`
- Choose a new name like `memorable-ai` or `memorable-engine`

### Authentication errors
- Make sure token starts with `pypi-`
- Check token hasn't expired
- Verify you copied the full token

### Build errors
- Run `pip install build twine` first
- Make sure all dependencies are in `requirements.txt`
- Check `setup.py` and `pyproject.toml` are valid

## After Publishing

1. Verify on PyPI: https://pypi.org/project/memorable/
2. Update README.md if needed
3. Announce the release!

---

**Need help?** See `docs/PUBLISHING.md` for detailed instructions.

