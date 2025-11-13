# Release Process

This document describes how to create a new release of pySMOKEPostProcessor.

---

## Overview

Releases are automated via GitHub Actions. When you create a new release/tag, GitHub Actions will:

1. ✅ Build wheels for Linux, macOS (Intel + ARM), and Windows
2. ✅ Build source distribution (sdist)
3. ✅ Test all wheels
4. ✅ Upload to GitHub Releases


---

## Release Workflow

### 1. Prepare the Release

Before creating a release, ensure:

```bash
# Pull latest changes
git checkout main
git pull origin main

# Run tests locally
conda activate pySMOKEPostProcessor
pip install -e .
python -c "import pySMOKEPostProcessor; print('OK')"
```

### 2. Update Version Number

Update the version in these files:
- `pyproject.toml` (line 3)
- `CMakeLists.txt` (line 7, VERSION field)
- `conda.recipe/meta.yaml` (line 2)

```bash
# Example for version 0.3.0
VERSION="0.3.0"

# Update pyproject.toml
sed -i '' "s/version = .*/version = \"$VERSION\"/" pyproject.toml

# Commit changes
git add pyproject.toml CMakeLists.txt conda.recipe/meta.yaml
git commit -m "Bump version to $VERSION"
git push origin main
```

### 3. Create a Git Tag

```bash
VERSION="0.3.0"
git tag -a v$VERSION -m "Release version $VERSION"
git push origin v$VERSION
```

### 4. Create GitHub Release

Go to: https://github.com/tdinelli/pySMOKEPostProcessor/releases/new

Or use GitHub CLI:

```bash
gh release create v$VERSION \
  --title "v$VERSION" \
  --notes "Release notes here..." \
  --draft  # Remove --draft when ready
```

**Release Notes Template:**

```markdown
## What's New in v0.3.0

### Features
- Feature 1
- Feature 2

### Bug Fixes
- Fix 1
- Fix 2

### Breaking Changes
- None

### Installation

**From GitHub Release:**
```bash
pip install https://github.com/tdinelli/pySMOKEPostProcessor/releases/download/v0.3.0/pySMOKEPostProcessor-0.3.0-cp311-cp311-macosx_14_0_arm64.whl
```

**From PyPI (if published):**
```bash
pip install pySMOKEPostProcessor==0.3.0
```

**Full Changelog**: https://github.com/tdinelli/pySMOKEPostProcessor/compare/v0.2.0...v0.3.0
```

### 5. Monitor GitHub Actions

After creating the release:

1. Go to: https://github.com/tdinelli/pySMOKEPostProcessor/actions
2. Watch the "Build Wheels (cibuildwheel)" workflow
3. Ensure all jobs complete successfully

Build time: ~30-45 minutes for all platforms

### 6. Verify Release Artifacts

Once the workflow completes, check:

1. Go to: https://github.com/tdinelli/pySMOKEPostProcessor/releases
2. Verify wheels are uploaded:
   - `pySMOKEPostProcessor-*-linux_x86_64.whl`
   - `pySMOKEPostProcessor-*-macosx_*_x86_64.whl`
   - `pySMOKEPostProcessor-*-macosx_*_arm64.whl`
   - `pySMOKEPostProcessor-*-win_amd64.whl`
   - `pySMOKEPostProcessor-*.tar.gz` (source distribution)

### 7. Test Installation from Release

Test on a clean environment:

```bash
# Create fresh environment
conda create -n test-release python=3.11
conda activate test-release

# Install from GitHub release (replace with actual URL)
pip install https://github.com/tdinelli/pySMOKEPostProcessor/releases/download/v0.3.0/pySMOKEPostProcessor-0.3.0-cp311-cp311-macosx_14_0_arm64.whl

# Test import
python -c "import pySMOKEPostProcessor; print('Success!')"
```

---

## Workflows Explanation

### `wheels_cibuildwheel.yml` (Recommended)

Uses `cibuildwheel` for robust cross-platform builds:

- **Triggers**: On tags (`v*`), releases, or manual dispatch
- **Platforms**: Linux, macOS (Intel + ARM), Windows
- **Python versions**: 3.8, 3.9, 3.10, 3.11, 3.12
- **Artifacts**: Wheels uploaded to GitHub Release

**Advantages:**
- ✅ Handles manylinux builds
- ✅ Cross-compilation for macOS ARM
- ✅ Automatic testing of wheels

### `build_wheels.yml` (Alternative)

Manual build for each platform/Python combination:

- More control but slower
- Good for debugging build issues

### `test.yml`

Runs on every push/PR to test the build:

- **Platforms**: Ubuntu, macOS
- **Python**: 3.9, 3.11
- **Purpose**: Catch build issues early

---


## Troubleshooting

### Build fails on specific platform

1. Check the Actions log
2. Try building locally with cibuildwheel:

```bash
pip install cibuildwheel
cibuildwheel --platform linux  # or macos, windows
```

### Boost/Eigen not found

Verify system dependencies are installed in workflow:
- Linux: `libboost-all-dev`, `libeigen3-dev`
- macOS: `boost`, `eigen`
- Windows: Installed via conda/vcpkg

### Wheel is too large

Boost is statically linked. To reduce size:
- Use shared Boost libraries
- Strip debug symbols

### OpenSMOKEpp fetch fails

GitHub Actions needs internet access. Check:
- Git is installed in workflow
- GitHub API rate limits

---

## Release Checklist

- [ ] Update version in `pyproject.toml`, `CMakeLists.txt`, `conda.recipe/meta.yaml`
- [ ] Commit version bump
- [ ] Create and push git tag (`v*.*.*`)
- [ ] Create GitHub Release
- [ ] Monitor GitHub Actions workflow
- [ ] Verify wheels are uploaded
- [ ] Test installation from release
- [ ] Announce release (README, documentation, etc.)

---

## Version Naming Convention

- **Major** (X.0.0): Breaking changes
- **Minor** (0.X.0): New features, backward compatible
- **Patch** (0.0.X): Bug fixes

Examples:
- `v0.2.0` → `v0.2.1` (bug fix)
- `v0.2.1` → `v0.3.0` (new feature)
- `v0.3.0` → `v1.0.0` (breaking change)

---

## Additional Resources

- cibuildwheel docs: https://cibuildwheel.readthedocs.io/
- GitHub Actions: https://docs.github.com/en/actions
- GitHub Releases: https://docs.github.com/en/repositories/releasing-projects-on-github
