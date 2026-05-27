/**
 * build_admin_spa.js
 * JSX → JS: Admin SPA fayllarini esbuild bilan compile qilish
 * Docker build time da ishlaydi — Babel runtime browser da kerak emas
 *
 * Ishlatish: node scripts/build_admin_spa.js
 */

const fs   = require('fs');
const path = require('path');

// esbuild — Vite dependency sifatida o'rnatilgan
let esbuild;
try {
  esbuild = require(path.join(__dirname, '..', 'frontend', 'node_modules', 'esbuild'));
} catch(e) {
  try {
    esbuild = require('esbuild');
  } catch(e2) {
    console.error('esbuild topilmadi: ' + e.message);
    process.exit(1);
  }
}

const SPA_DIR = path.join(__dirname, '..', 'core', 'static', 'admin_ui', 'spa');

const FILES = [
  'tweaks-panel',
  'ui',
  'shell',
  'pages-core',
  'pages-qr',
  'pages-comm',
  'pages-meta',
  'app',
];

let success = 0;
let errors  = 0;

for (const name of FILES) {
  const inFile  = path.join(SPA_DIR, name + '.jsx');
  const outFile = path.join(SPA_DIR, name + '.js');

  try {
    const source = fs.readFileSync(inFile, 'utf8');
    const result = esbuild.transformSync(source, {
      loader:      'jsx',
      jsxFactory:  'React.createElement',
      jsxFragment: 'React.Fragment',
      target:      'es2017',
    });
    fs.writeFileSync(outFile, result.code);
    console.log(`  ✓  ${name}.jsx  →  ${name}.js`);
    success++;
  } catch (err) {
    console.error(`  ✗  ${name}.jsx  XATO: ${err.message}`);
    errors++;
  }
}

console.log(`\nNatija: ${success} muvaffaqiyatli, ${errors} xato`);
if (errors > 0) process.exit(1);
