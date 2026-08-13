import fs from 'node:fs';
import path from 'node:path';

const repoRoot = path.resolve(process.cwd(), '..');
const BASE = import.meta.env.BASE_URL.replace(/\/$/, '');
const DESCRIPTION =
  'Divulgación científica y recursos didácticos sobre modelado, simulación, control y optimización de sistemas mecatrónicos.';

const sectionRoutes: Record<string, string> = {
  'inicio.html': '/',
  'modelado.html': '/modelado/',
  'simulacion.html': '/simulacion/',
  'control.html': '/control/',
  'optimizacion.html': '/optimizacion/',
  'miscelanea.html': '/miscelanea/',
  'Python.html': '/software/python/',
  'MATLAB.html': '/software/matlab/',
  'iLaTeX.html': '/software/latex/',
  'LaTeX.html': '/LaTeX.html'
};

export const sections = {
  inicio: {
    source: 'inicio.html',
    title: 'DR Automática',
    description: DESCRIPTION
  },
  modelado: {
    source: 'modelado.html',
    title: 'Modelado | DR Automática',
    description: 'Artículos y recursos didácticos sobre modelado de sistemas dinámicos y mecatrónicos.'
  },
  simulacion: {
    source: 'simulacion.html',
    title: 'Simulación | DR Automática',
    description: 'Recursos sobre simulación de sistemas dinámicos, robótica, control y análisis numérico.'
  },
  control: {
    source: 'control.html',
    title: 'Control | DR Automática',
    description: 'Divulgación y materiales sobre control automático, estabilidad y sistemas dinámicos.'
  },
  optimizacion: {
    source: 'optimizacion.html',
    title: 'Optimización | DR Automática',
    description: 'Entradas y recursos sobre optimización aplicada a ingeniería, simulación y MATLAB.'
  },
  python: {
    source: 'Python.html',
    title: 'Python | DR Automática',
    description: 'Herramientas, artículos y contribuciones sobre Python para ciencia, ingeniería y automatización.'
  },
  matlab: {
    source: 'MATLAB.html',
    title: 'MATLAB | DR Automática',
    description: 'Contribuciones, recursos y publicaciones sobre MATLAB en ingeniería y análisis científico.'
  },
  latex: {
    source: 'iLaTeX.html',
    title: 'LaTeX | DR Automática',
    description: 'Recursos y publicaciones sobre LaTeX para escritura científica y documentos técnicos.'
  },
  miscelanea: {
    source: 'miscelanea.html',
    title: 'Miscelánea | DR Automática',
    description: 'Ideas, reflexiones y contenidos diversos de divulgación científica y pensamiento crítico.'
  }
} as const;

function withBase(url: string) {
  if (url === '/') return `${BASE}/`;
  if (url.startsWith('/')) return `${BASE}${url}`;
  return `${BASE}/${url}`;
}

function isExternal(url: string) {
  return /^(?:[a-z][a-z0-9+.-]*:|\/\/|#|mailto:|tel:)/i.test(url);
}

function extractBody(html: string) {
  const match = html.match(/<body[^>]*>([\s\S]*?)<\/body>/i);
  if (match) return match[1];
  return html;
}

function extractHead(html: string) {
  const match = html.match(/<head[^>]*>([\s\S]*?)<\/head>/i);
  if (match) return match[1];
  return '';
}

function stripOuterDocument(html: string) {
  return extractBody(html).trim();
}

function textFromHtml(html: string) {
  return html
    .replace(/<script[\s\S]*?<\/script>/gi, ' ')
    .replace(/<style[\s\S]*?<\/style>/gi, ' ')
    .replace(/<[^>]+>/g, ' ')
    .replace(/\s+/g, ' ')
    .trim();
}

function titleFromHtml(html: string, fallback: string) {
  const title = html.match(/<title>\s*([^<]+?)\s*<\/title>/i)?.[1];
  const heading = html.match(/<h1[^>]*>\s*([^<]+?)\s*<\/h1>/i)?.[1];
  return (title || heading || fallback).trim();
}

function descriptionFromHtml(html: string) {
  const meta = html.match(/<meta\s+name=["']description["']\s+content=["']([^"']+)["']/i)?.[1];
  if (meta) return meta.trim();
  const text = textFromHtml(stripOuterDocument(html));
  return text.length > 155 ? `${text.slice(0, 152).trim()}...` : text || DESCRIPTION;
}

function rewriteUrl(url: string, sourceDir = '') {
  if (isExternal(url)) return url;
  if (url.startsWith('/')) return url;

  const clean = url.replace(/^\.\//, '');
  const [pathname, suffix = ''] = clean.split(/(?=[?#])/);
  if (!pathname) return clean;

  if (sectionRoutes[pathname]) return withBase(sectionRoutes[pathname]) + suffix;

  const article = pathname.match(/^html\/([a-zA-Z0-9_-]+)\.html$/);
  if (article) return withBase(`/articulos/${article[1]}/`) + suffix;

  const sameDirArticle = pathname.match(/^([a-zA-Z0-9_-]+)\.html$/);
  if (sameDirArticle && sourceDir === 'html') return withBase(`/articulos/${sameDirArticle[1]}/`) + suffix;

  if (pathname.startsWith('pdf/')) return withBase(`/${pathname}`) + suffix;
  if (pathname.startsWith('images/')) return withBase(`/${pathname}`) + suffix;
  if (pathname.startsWith('html/')) return withBase(`/${pathname}`) + suffix;
  if (sourceDir === 'html') return withBase(`/html/${pathname}`) + suffix;

  return withBase(`/${pathname}`) + suffix;
}

function rewriteHtml(html: string, sourceDir = '') {
  html = html.replace(
    /<a([^>]*?)href=["']javascript:void\(0\)["']([^>]*?)onclick=["']loadContent\(['"]([^'"]+)['"]\)["']([^>]*)>/gi,
    (_match, a, b, target, c) => `<a${a}href="${rewriteUrl(target, sourceDir)}"${b}${c}>`
  );
  html = html.replace(
    /<a([^>]*?)onclick=["']loadContent\(['"]([^'"]+)['"]\)["']([^>]*?)href=["']javascript:void\(0\)["']([^>]*)>/gi,
    (_match, a, target, b, c) => `<a${a}href="${rewriteUrl(target, sourceDir)}"${b}${c}>`
  );
  html = html.replace(/\s+onclick=["']loadContent\([^)]*\)["']/gi, '');
  html = html.replace(/\s+onclick=["'](?:w3_open|w3_close|myAccordion)\([^)]*\)["']/gi, '');
  html = html.replace(/\b(href|src)=["']([^"']+)["']/gi, (match, attr, url) => {
    const rewritten = rewriteUrl(url, sourceDir);
    return rewritten === url ? match : `${attr}="${rewritten}"`;
  });
  html = html.replace(/<b>optimización<b>/gi, '<b>optimización</b>');
  return html;
}

export function loadLegacyFragment(filename: string) {
  const html = extractBody(fs.readFileSync(path.join(repoRoot, filename), 'utf8'));
  return rewriteHtml(html);
}

export function loadSectionIntro(filename: string) {
  const html = extractBody(fs.readFileSync(path.join(repoRoot, filename), 'utf8'));
  const withoutListings = html.replace(
    /<section\s+id=["']articulos-recientes["'][^>]*>[\s\S]*?<\/section>/i,
    ''
  );
  return rewriteHtml(withoutListings);
}

export function loadSectionIntroParts(filename: string, splitAfterSectionId: string) {
  const intro = loadSectionIntro(filename);
  const sectionPattern = new RegExp(
    `(<section\\s+id=["']${splitAfterSectionId}["'][^>]*>[\\s\\S]*?<\\/section>)`,
    'i'
  );
  const match = intro.match(sectionPattern);

  if (!match || typeof match.index !== 'number') {
    return { before: intro, after: '' };
  }

  const splitIndex = match.index + match[0].length;
  return {
    before: intro.slice(0, splitIndex),
    after: intro.slice(splitIndex)
  };
}

export function makeSectionsCollapsible(html: string, sectionIds: string[]) {
  return sectionIds.reduce((currentHtml, sectionId) => {
    const sectionPattern = new RegExp(
      `<section\\s+id=["']${sectionId}["']([^>]*)>([\\s\\S]*?)<\\/section>`,
      'i'
    );

    return currentHtml.replace(sectionPattern, (_match, _attributes, content) => {
      const headingMatch = content.match(/<h[1-6][^>]*>([\s\S]*?)<\/h[1-6]>/i);
      const heading = headingMatch ? headingMatch[1].replace(/<[^>]*>/g, '').trim() : 'Mostrar contenido';
      const body = headingMatch ? content.replace(headingMatch[0], '').trim() : content.trim();

      return `<details id="${sectionId}" class="collapsible-section">
  <summary>${heading}</summary>
  <div class="collapsible-section-body">
    ${body}
  </div>
</details>`;
    });
  }, html);
}

export function removeSectionHeadings(html: string, sectionIds: string[]) {
  return sectionIds.reduce((currentHtml, sectionId) => {
    const sectionPattern = new RegExp(
      `(<section\\s+id=["']${sectionId}["'][^>]*>)([\\s\\S]*?)(<\\/section>)`,
      'i'
    );

    return currentHtml.replace(sectionPattern, (_match, opening, content, closing) => {
      const withoutHeading = content.replace(/^\s*<h[1-6][^>]*>[\s\S]*?<\/h[1-6]>/i, '');
      return `${opening}${withoutHeading}${closing}`;
    });
  }, html);
}

export function getArticleSlugs() {
  const htmlDir = path.join(repoRoot, 'html');
  return fs
    .readdirSync(htmlDir)
    .filter((filename) => filename.endsWith('.html'))
    .map((filename) => path.basename(filename, '.html'))
    .sort();
}

export function loadArticle(slug: string) {
  const source = path.join(repoRoot, 'html', `${slug}.html`);
  const raw = fs.readFileSync(source, 'utf8');
  const head = rewriteHtml(extractHead(raw), 'html')
    .replace(/<title>[\s\S]*?<\/title>/gi, '')
    .replace(/<meta\s+name=["']description["'][^>]*>/gi, '')
    .replace(/<meta\s+charset=["'][^"']+["'][^>]*>/gi, '')
    .replace(/<meta\s+name=["']viewport["'][^>]*>/gi, '')
    .trim();

  return {
    slug,
    title: `${titleFromHtml(raw, slug)} | DR Automática`,
    description: descriptionFromHtml(raw),
    head,
    html: rewriteHtml(stripOuterDocument(raw), 'html')
  };
}
