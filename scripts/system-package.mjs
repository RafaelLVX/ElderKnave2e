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

async function buildPacks() {
  console.log('[stage] Building compendium packs...');
  const srcDir = path.join(root, 'packs');
  const buildRoot = path.join(root, 'build');
  const packsDir = path.join(buildRoot, systemId, 'packs');
  
  if (!fs.existsSync(srcDir)) {
    console.log('[info] No packs directory found, skipping pack build');
    return;
  }
  
  try {
    // Find all pack groups
    const packGroups = fs.readdirSync(srcDir);
    let totalEntries = 0;
    
    for (const group of packGroups) {
      const groupPath = path.join(srcDir, group);
      const stat = fs.statSync(groupPath);
      
      if (stat.isDirectory()) {
        console.log(`[packs] Processing group: ${group}`);
        
        // Find all pack files (JSON files in the group directory)
        const files = fs.readdirSync(groupPath);
        const jsonFiles = files.filter(f => f.endsWith('.json'));
        
        for (const file of jsonFiles) {
          const filePath = path.join(groupPath, file);
          const packName = path.basename(file, '.json');
          
          const outputDir = path.join(packsDir, group);
          const outputFile = path.join(outputDir, `${packName}.db`);
          
          // Ensure output directory exists
          fse.ensureDirSync(outputDir);
          
          // Read the JSON file
          const content = fs.readFileSync(filePath, 'utf8');
          
          try {
            const data = JSON.parse(content);
            
            // Handle both single object and array of objects
            const entries = Array.isArray(data) ? data : [data];
            
            if (entries.length === 0) {
              console.warn(`[packs] No entries in ${group}/${file}`);
              continue;
            }
            
            // Process each entry
            const processedEntries = [];
            for (const entry of entries) {
              // Ensure proper _stats metadata for Foundry v12
              if (!entry._stats) {
                entry._stats = {
                  compendiumSource: null,
                  duplicateSource: null,
                  coreVersion: "12.343",
                  systemId: systemId,
                  systemVersion: version,
                  createdTime: null,
                  modifiedTime: null,
                  lastModifiedBy: null
                };
              }
              
              // Ensure embedded items also have proper _stats
              if (entry.items && Array.isArray(entry.items)) {
                entry.items.forEach(item => {
                  if (!item._stats) {
                    item._stats = {
                      compendiumSource: null,
                      duplicateSource: null,
                      coreVersion: "12.343",
                      systemId: systemId,
                      systemVersion: version,
                      createdTime: null,
                      modifiedTime: null,
                      lastModifiedBy: null
                    };
                  }
                });
              }
              
              processedEntries.push(JSON.stringify(entry));
              console.log(`[packs]   Added: ${entry.name || entry._id || 'unknown'}`);
            }
            
            if (processedEntries.length > 0) {
              // Write entries to .db file (one JSON object per line)
              fs.writeFileSync(outputFile, processedEntries.join('\n') + '\n');
              console.log(`[packs] Built ${group}/${packName}.db with ${processedEntries.length} entries`);
              totalEntries += processedEntries.length;
            }
          } catch (error) {
            console.error(`[packs] Error parsing ${file}:`, error.message);
          }
        }
      }
    }
    
    console.log(`[packs] Complete: ${totalEntries} total entries built`);
  } catch (error) {
    console.error('[packs] Error building packs:', error.message);
    process.exit(1);
  }
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
  await buildPacks();
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
