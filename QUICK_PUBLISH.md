# Quick Publishing Guide

You've already set up your tokens in GitHub Secrets. Here's how to publish:

## Step 1: Publish to Test PyPI (Test First!)

Run this command and enter your Test PyPI token when prompted:

```bash
./scripts/publish_to_pypi.sh test
```

Or manually:
```bash
export TWINE_USERNAME=__token__
export TWINE_PASSWORD=your-test-token-here
twine upload --repository testpypi dist/*
```

## Step 2: Verify Test Installation

```bash
pip install --index-url https://test.pypi.org/simple/ memorable
python3 -c "import memorable; print('✅ Success!')"
```

## Step 3: Publish to Production PyPI

Once Test PyPI works, publish to production:

```bash
./scripts/publish_to_pypi.sh production
```

Or manually:
```bash
export TWINE_USERNAME=__token__
export TWINE_PASSWORD=your-production-token-here
twine upload dist/*
```

## Step 4: Verify Production Installation

```bash
pip install memorable
python3 -c "import memorable; print('✅ Success!')"
```

---

**Or use automated publishing (after tokens are in GitHub Secrets):**

```bash
git tag v0.1.0
git push origin v0.1.0
# GitHub Actions will automatically publish!
```

