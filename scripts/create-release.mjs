#!/usr/bin/env node
// Automated GitHub Release Creation Script for Elder Knave 2e
// Usage: node scripts/create-release.mjs [--draft] [--prerelease]
// Documentation: docs/release-guide.md

import fs from 'fs';
import path from 'path';
import { execSync } from 'child_process';
import readline from 'readline';

const root = process.cwd();
const manifestPath = path.join(root, 'system.json');
const changelogPath = path.join(root, 'CHANGELOG.md');
const zipPath = path.join(root, 'dist', 'system.zip');
const releaseNotesPath = path.join(root, 'RELEASE_NOTES.md');

// Parse arguments
const isDraft = process.argv.includes('--draft');
const isPrerelease = process.argv.includes('--prerelease');

// Track warnings for confirmation prompt
let hasWarnings = false;

function checkGhCli() {
  try {
    execSync('gh --version', { stdio: 'pipe' });
    console.log('[check] GitHub CLI (gh) is installed');
  } catch (err) {
    console.error('ERROR: GitHub CLI (gh) is not installed or not in PATH');
    console.error('Install from: https://cli.github.com/');
    process.exit(1);
  }
}

function checkGitStatus() {
  try {
    const status = execSync('git status --porcelain', { encoding: 'utf-8' });
    if (status.trim()) {
      console.warn('\n⚠️  WARNING: Working directory has uncommitted changes');
      console.warn('   Uncommitted changes will not be included in the release\n');
      hasWarnings = true;
    }
  } catch (err) {
    console.error('ERROR: Not a git repository or git is not available');
    process.exit(1);
  }
}

function getManifest() {
  if (!fs.existsSync(manifestPath)) {
    console.error('ERROR: system.json not found');
    process.exit(1);
  }
  return JSON.parse(fs.readFileSync(manifestPath, 'utf-8'));
}

function getVersion() {
  return getManifest().version;
}

function getRepository() {
  const manifest = getManifest();
  const url = manifest.url;
  if (!url) {
    console.error('ERROR: No url field in system.json');
    process.exit(1);
  }
  // Extract owner/repo from GitHub URL
  const match = url.match(/github\.com\/([^\/]+\/[^\/]+?)(?:\.git)?$/);
  if (!match) {
    console.error('ERROR: Could not parse GitHub repository from url in system.json');
    process.exit(1);
  }
  return match[1];
}

function checkTagExists(version) {
  try {
    const tags = execSync('git tag', { encoding: 'utf-8' });
    const tagName = `v${version}`;
    if (tags.split('\n').includes(tagName)) {
      console.error(`ERROR: Tag ${tagName} already exists`);
      console.error('Update version in system.json before creating a new release');
      process.exit(1);
    }
  } catch (err) {
    console.error('ERROR: Failed to check existing tags');
    process.exit(1);
  }
}

function getPreviousTag() {
  try {
    const tags = execSync('git tag --sort=-version:refname', { encoding: 'utf-8' })
      .split('\n')
      .filter(t => t.trim())
      .filter(t => t.match(/^v\d+\.\d+\.\d+$/));
    return tags.length > 0 ? tags[0] : null;
  } catch (err) {
    return null;
  }
}

function buildRelease() {
  console.log('[build] Running system packager with --zip...');
  try {
    execSync('node scripts/system-package.mjs --zip', { 
      stdio: 'inherit',
      cwd: root 
    });
  } catch (err) {
    console.error('ERROR: Failed to build system package');
    process.exit(1);
  }

  if (!fs.existsSync(zipPath)) {
    console.error(`ERROR: Expected zip file not found: ${zipPath}`);
    process.exit(1);
  }

  const stats = fs.statSync(zipPath);
  console.log(`[build] Package created: ${(stats.size / 1024).toFixed(2)} KB`);
}

function extractChangelogForVersion(version) {
  if (!fs.existsSync(changelogPath)) {
    console.error('ERROR: CHANGELOG.md not found');
    console.error('Please create CHANGELOG.md with a section for this version');
    process.exit(1);
  }

  const changelog = fs.readFileSync(changelogPath, 'utf-8');
  const lines = changelog.split('\n');
  
  const versionHeader = `## ${version}`;
  const startIdx = lines.findIndex(line => line.trim() === versionHeader);
  
  if (startIdx === -1) {
    console.error(`ERROR: Version ${version} not found in CHANGELOG.md`);
    console.error('Please add a section for this version before creating a release');
    process.exit(1);
  }

  // Find the next version header (starts with ##)
  let endIdx = lines.slice(startIdx + 1).findIndex(line => line.trim().startsWith('##'));
  if (endIdx === -1) {
    endIdx = lines.length;
  } else {
    endIdx = startIdx + 1 + endIdx;
  }

  const versionChangelog = lines.slice(startIdx + 1, endIdx)
    .join('\n')
    .trim();

  return versionChangelog;
}

function generateReleaseNotes(version) {
  console.log('[notes] Generating release notes...');
  
  let notes = '';
  
  // Check for custom release notes file
  if (fs.existsSync(releaseNotesPath)) {
    console.log('[notes] Using RELEASE_NOTES.md');
    notes = fs.readFileSync(releaseNotesPath, 'utf-8');
  } else {
    // Extract from CHANGELOG.md (will exit if not found)
    const changelog = extractChangelogForVersion(version);
    notes = `## Changes\n\n${changelog}`;
  }

  // Add comparison link to previous version
  const previousTag = getPreviousTag();
  if (previousTag) {
    notes += `\n\n## Full Changelog\n\n`;
    notes += `[${previousTag}...v${version}](https://github.com/RafaelLVX/ElderKnave2e/compare/${previousTag}...v${version})`;
  }

  // Add installation instructions
  notes += `\n\n## Installation\n\n`;
  notes += `In Foundry VTT:\n`;
  notes += `- Go to Game Systems tab\n`;
  notes += `- Click Install System\n`;
  notes += `- In the Manifest URL field, paste:\n`;
  notes += `  \`https://raw.githubusercontent.com/RafaelLVX/ElderKnave2e/main/system.json\`\n`;
  notes += `- Click Install`;

  return notes;
}

function promptConfirmation() {
  return new Promise((resolve) => {
    const rl = readline.createInterface({
      input: process.stdin,
      output: process.stdout
    });
    
    rl.question('Continue with release creation? (y/N): ', (answer) => {
      rl.close();
      const normalized = answer.toLowerCase().trim();
      // Default to 'no' if empty input
      if (normalized === '') {
        resolve(false);
      } else {
        resolve(normalized === 'yes' || normalized === 'y');
      }
    });
  });
}

function createRelease(version, notes) {
  const tagName = `v${version}`;
  const title = `Elder Knave v${version}`;
  const repo = getRepository();
  
  console.log(`[release] Creating GitHub release: ${title}`);
  console.log(`[release] Tag: ${tagName}`);
  console.log(`[release] Repository: ${repo}`);
  
  // Save notes to temp file (gh release create needs a file)
  const tempNotesFile = path.join(root, '.release-notes.tmp');
  fs.writeFileSync(tempNotesFile, notes);

  try {
    let cmd = `gh release create "${tagName}" "${zipPath}" `;
    cmd += `--repo "${repo}" `;
    cmd += `--title "${title}" `;
    cmd += `--notes-file "${tempNotesFile}" `;
    
    if (isDraft) {
      cmd += '--draft ';
      console.log('[release] Creating as DRAFT');
    }
    
    if (isPrerelease) {
      cmd += '--prerelease ';
      console.log('[release] Marking as PRERELEASE');
    }

    console.log('[release] Executing gh release create...');
    execSync(cmd, { stdio: 'inherit', cwd: root });
    
    // Clean up temp file
    fs.unlinkSync(tempNotesFile);
    
    console.log(`\n✓ Release created successfully!`);
    console.log(`  View at: https://github.com/RafaelLVX/ElderKnave2e/releases/tag/${tagName}`);
    
  } catch (err) {
    if (fs.existsSync(tempNotesFile)) {
      fs.unlinkSync(tempNotesFile);
    }
    console.error('ERROR: Failed to create GitHub release');
    console.error('Check that you are authenticated with gh (run: gh auth login)');
    process.exit(1);
  }
}

async function main() {
  console.log('Elder Knave 2e - GitHub Release Creator\n');
  
  // Pre-flight checks
  checkGhCli();
  checkGitStatus();
  
  const version = getVersion();
  console.log(`[info] Version: ${version}`);
  
  checkTagExists(version);
  
  // Prompt for confirmation if there are warnings
  if (hasWarnings) {
    const confirmed = await promptConfirmation();
    if (!confirmed) {
      console.log('\nRelease creation cancelled.');
      process.exit(0);
    }
    console.log('');
  }
  
  // Build the package
  buildRelease();
  
  // Generate release notes
  const notes = generateReleaseNotes(version);
  
  // Create the release
  createRelease(version, notes);
  
  console.log('Done! 🎉');
}

main().catch(err => {
  console.error(err);
  process.exit(1);
});
