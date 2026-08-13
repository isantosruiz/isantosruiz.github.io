# DR Automática en Astro

Migración del portal de divulgación de `divulgacion.html` a Astro sin reemplazar el sitio académico raíz.

## Desarrollo local

Desde la raíz del repositorio:

```bash
cd astro-drautomatica
npm ci
npm run dev
```

El proyecto lee durante `dev` y `build` los archivos legacy que siguen en la raíz del repositorio (`inicio.html`, `control.html`, `MATLAB.html`, etc.). Los HTML propios de `html/*.html` se publican como rutas limpias bajo `/articulos/<slug>/`; los assets de `html/`, `pdf/`, `images/` y logos necesarios se copian al build de DR Automática.

## Publicación

`npm run build` genera la salida estática en `../drautomatica/`. El workflow de GitHub Actions incluido recompila esa carpeta cuando cambia `astro-drautomatica/**` o cualquiera de los contenidos legacy vinculados.

URL objetivo: `https://isantosruiz.github.io/drautomatica/`.

La configuración actual usa `site: 'https://isantosruiz.github.io'` y `base: '/drautomatica'`. Para mover el portal a `https://drautomatica.com/`, la intención es cambiar esos valores de Astro sin rediseñar páginas ni reescribir el contenido.
