#!/usr/bin/env node
// Cross-platform system packaging script for FoundryVTT
// Creates build/<systemId> with runtime files and optionally dist/system.zip

import fs from 'fs';
import fse from 'fs-extra';
import path from 'path';
import archiver from 'archiver';
import * as sass from 'sass';
import postcss from 'postcss';
import autoprefixer from 'autoprefixer';

const root = process.cwd();
const manifestPath = path.join(root, 'system.json');
if (!fs.existsSync(manifestPath)) {
  console.error('system.json not found; run from project root.');
  process.exit(1);
}
const manifest = JSON.parse(fs.readFileSync(manifestPath, 'utf-8'));
const systemId = manifest.id;
const version = manifest.version;
const zip = process.argv.includes('--zip');

async function runCssBuild() {
  console.log('[stage] Compiling SCSS via sass+postcss...');
  const entry = path.join(root, 'scss', 'knave2e.scss');
  if (!fs.existsSync(entry)) {
    console.error('Missing entry SCSS file: ' + entry);
    process.exit(1);
  }
  const result = sass.compile(entry, {
    style: 'expanded',
    sourceMap: true,
    loadPaths: [path.join(root, 'scss')]
  });
  const post = await postcss([autoprefixer({ 
    overrideBrowserslist: ['last 3 versions'],
    cascade: false 
  })]).process(result.css, {
    from: 'knave2e.scss',
    to: 'knave2e.css',
    map: { prev: result.sourceMap, inline: true, sourcesContent: false }
  });
  
  // Ensure no external map file is written
  if (post.map) {
    delete post.map;
  }
  
  // Match original gulp sourcemap format by adding charset=utf8
  let finalCss = post.css;
  if (finalCss.includes('/*# sourceMappingURL=data:application/json;base64,')) {
    finalCss = finalCss.replace(
      '/*# sourceMappingURL=data:application/json;base64,',
      '/*# sourceMappingURL=data:application/json;charset=utf8;base64,'
    );
  }
  const cssDir = path.join(root, 'css');
  fse.ensureDirSync(cssDir);
  const cssArtifact = path.join(cssDir, 'knave2e.css');
  // Write CSS with inline sourcemap to match gulp-sourcemaps behavior
  fs.writeFileSync(cssArtifact, finalCss);
  const stat = fs.statSync(cssArtifact);
  if (!stat.isFile() || stat.size === 0) {
    console.error('[error] CSS artifact missing or empty after build');
    process.exit(1);
  }
  console.log('[verify] CSS artifact present (' + stat.size + ' bytes)');
}

function cleanDir(dir) {
  if (fs.existsSync(dir)) {
    fse.removeSync(dir);
  }
  fse.ensureDirSync(dir);
}

function copyRuntime() {
  const buildRoot = path.join(root, 'build');
  const target = path.join(buildRoot, systemId);
  cleanDir(buildRoot);
  fse.ensureDirSync(target);
  const runtimePaths = [
    'system.json',
    'template.json',
    'module',
    'templates',
    'css',
    'assets',
    'lang',
    'LICENSE.txt'
  ];
  for (const p of runtimePaths) {
    const src = path.join(root, p);
    if (!fs.existsSync(src)) {
      console.warn(`[warn] Missing path: ${p} (skipped)`);
      continue;
    }
    const dest = path.join(target, p);
    fse.copySync(src, dest, { dereference: true });
    console.log('[copy] ' + p);
  }
  return target;
}

function createZip(sourceDir) {
  const distDir = path.join(root, 'dist');
  fse.ensureDirSync(distDir);
  const zipPath = path.join(distDir, 'system.zip');
  if (fs.existsSync(zipPath)) fs.unlinkSync(zipPath);
  const output = fs.createWriteStream(zipPath);
  const archive = archiver('zip', { zlib: { level: 9 } });

  return new Promise((resolve, reject) => {
    output.on('close', () => {
      console.log(`[zip] Created ${zipPath} (${archive.pointer()} bytes)`);
      resolve(zipPath);
    });
    archive.on('error', reject);
    archive.pipe(output);
    archive.directory(sourceDir + '/', false); // contents only
    archive.finalize();
  });
}

async function main() {
  console.log(`Packaging system '${systemId}' v${version}`);
  await runCssBuild();
  const stagedDir = copyRuntime();
  if (zip) {
    await createZip(stagedDir);
  } else {
    console.log('[info] Zip not requested; use --zip to create dist/system.zip');
  }
  console.log('Done.');
}

main().catch(err => {
  console.error(err);
  process.exit(1);
});
