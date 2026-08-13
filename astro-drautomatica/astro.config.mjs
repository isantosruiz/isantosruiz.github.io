import { defineConfig } from 'astro/config';

export default defineConfig({
  site: 'https://isantosruiz.github.io',
  base: '/drautomatica',
  output: 'static',
  outDir: '../drautomatica',
  build: {
    assets: '_astro',
    format: 'directory'
  },
  trailingSlash: 'always'
});
