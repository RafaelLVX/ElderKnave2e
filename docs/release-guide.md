# Release Creation Guide

This guide explains how to create a new release of Elder Knave 2e.

## Prerequisites

1. **GitHub CLI**: Install from https://cli.github.com/
2. **Authentication**: Run `gh auth login` and follow prompts
3. **Git Repository**: Ensure you're in a clean git state with all changes committed

## Release Workflow

### 1. Update Version

Edit `system.json` and bump the `version` field:
```json
"version": "0.8.0"
```

### 2. Update CHANGELOG.md

Add a new section for the version with all changes:
```markdown
## 0.8.0
- Added new feature X
- Fixed bug Y
- Improved Z
```

### 3. Commit Changes

```bash
git add system.json CHANGELOG.md
git commit -m "Bump version to 0.8.0"
git push origin main
```

### 4. Create Release

Run the release script:
```bash
npm run release
```

Or for a draft release (to preview before publishing):
```bash
npm run release:draft
```

## What the Script Does

1. ✓ Checks GitHub CLI is installed and authenticated
2. ✓ Verifies git status and warns about uncommitted changes
3. ✓ Reads version from system.json
4. ✓ Checks that tag doesn't already exist
5. ✓ Runs `node scripts/system-package.mjs --zip` to build the package
6. ✓ Generates release notes from CHANGELOG.md or RELEASE_NOTES.md
7. ✓ Creates comparison link to previous version
8. ✓ Creates GitHub release with tag `vX.X.X`
9. ✓ Uploads `dist/system.zip` as release asset
10. ✓ Publishes release (or saves as draft)

## Customizing Release Notes

### Option 1: Use CHANGELOG.md (Default)

The script automatically extracts the section for your version from CHANGELOG.md.

### Option 2: Use RELEASE_NOTES.md Template

1. Edit `RELEASE_NOTES.md` with your custom description
2. Run the release script
3. The script will use your custom notes instead of CHANGELOG.md
4. Delete or rename `RELEASE_NOTES.md` after release to use auto-extraction again

## Release Options

### Draft Release
Create but don't publish (for review):
```bash
npm run release:draft
# or
node scripts/create-release.mjs --draft
```

### Pre-release
Mark as pre-release (beta, alpha, etc.):
```bash
node scripts/create-release.mjs --prerelease
```

### Combined Options
```bash
node scripts/create-release.mjs --draft --prerelease
```

## Troubleshooting

### "Tag already exists"
You're trying to create a release for a version that already exists. Update the version number in system.json.

### "GitHub CLI not installed"
Install from https://cli.github.com/ and ensure it's in your PATH.

### "Not authenticated"
Run `gh auth login` and follow the prompts to authenticate with GitHub.

### "Working directory has uncommitted changes"
Commit or stash your changes before creating a release. The script will warn but continue.

## Post-Release Steps

1. ✓ Visit the release page: https://github.com/RafaelLVX/ElderKnave2e/releases
2. ✓ Verify the release notes look correct
3. ✓ Check that system.zip is attached
4. ✓ If it was a draft, click "Publish release"
5. ✓ Announce the release on Discord, forums, etc.

## Release Checklist

- [ ] Version bumped in system.json
- [ ] CHANGELOG.md updated with version section
- [ ] Changes committed and pushed to main
- [ ] Release script executed successfully
- [ ] Release page reviewed
- [ ] Release published (if created as draft)
- [ ] Community notified

## Manual Release (If Script Fails)

If the automated script fails, you can create a release manually:

1. Build the package: `npm run release:zip`
2. Create a tag: `git tag v0.8.0 && git push origin v0.8.0`
3. Go to https://github.com/RafaelLVX/ElderKnave2e/releases/new
4. Select the tag, write notes, upload dist/system.zip
5. Click "Publish release"
