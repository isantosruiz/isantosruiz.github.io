import fs from 'node:fs';
import path from 'node:path';

const project = process.cwd();
const repo = path.resolve(project, '..');
const publicDir = path.join(project, 'public');

fs.rmSync(publicDir, { recursive: true, force: true });
fs.mkdirSync(publicDir, { recursive: true });

const rootAssets = [
  'arm.png',
  'banner.png',
  'banner_1200x630.png',
  'drAutomatica.png',
  'favicon.png',
  'favicon_.png',
  'ilatex-icon.png',
  'LaTeX_logo.png',
  'matlab-online.svg',
  'monline.png',
  'MonaspaceNeon-Regular.woff2',
  'python_logo.png'
];

function copyFileIfExists(relativePath) {
  const source = path.join(repo, relativePath);
  const target = path.join(publicDir, relativePath);
  if (!fs.existsSync(source)) return;
  fs.mkdirSync(path.dirname(target), { recursive: true });
  fs.copyFileSync(source, target);
}

function copyDirIfExists(relativePath) {
  const source = path.join(repo, relativePath);
  const target = path.join(publicDir, relativePath);
  if (!fs.existsSync(source)) return;
  fs.cpSync(source, target, { recursive: true });
}

function copyHtmlAssets() {
  const sourceDir = path.join(repo, 'html');
  const targetDir = path.join(publicDir, 'html');
  if (!fs.existsSync(sourceDir)) return;
  fs.mkdirSync(targetDir, { recursive: true });
  for (const filename of fs.readdirSync(sourceDir)) {
    if (filename.endsWith('.html')) continue;
    fs.copyFileSync(path.join(sourceDir, filename), path.join(targetDir, filename));
  }
}

function rewriteStandaloneCompiler(html) {
  return html
    .replace(/href=["']\.\/index\.html["']/gi, 'href="./"')
    .replace(/(src|href)=["']\.\/([^"']+)["']/gi, '$1="./$2"');
}

for (const asset of rootAssets) copyFileIfExists(asset);
copyDirIfExists('pdf');
copyDirIfExists('images');
copyHtmlAssets();

const latexCompiler = path.join(repo, 'LaTeX.html');
if (fs.existsSync(latexCompiler)) {
  const html = rewriteStandaloneCompiler(fs.readFileSync(latexCompiler, 'utf8'));
  fs.writeFileSync(path.join(publicDir, 'LaTeX.html'), html);
}

fs.writeFileSync(path.join(publicDir, '.nojekyll'), '');
