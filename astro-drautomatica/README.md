# drAutomática en Astro

Migración del portal de divulgación de `divulgacion.html` a Astro sin reemplazar el sitio académico raíz.

El nombre visual del sitio debe escribirse como **drAutomática**: `dr` en minúsculas, `A` mayúscula y acento en `á`.

## Desarrollo local

Desde la raíz del repositorio:

```bash
cd astro-drautomatica
npm ci
npm run dev
```

El proyecto lee durante `dev` y `build` los archivos legacy que siguen en la raíz del repositorio (`inicio.html`, `control.html`, `MATLAB.html`, etc.). Los HTML propios de `html/*.html` se publican como rutas limpias bajo `/articulos/<slug>/`; los assets de `html/`, `pdf/`, `images/` y logos necesarios se copian al build de drAutomática.

## Publicar contenidos

Astro es ahora el gestor central de las entradas visibles en las secciones. La lista de publicaciones se edita en:

```text
astro-drautomatica/src/data/catalog.ts
```

Cada entrada indica si es contenido local, enlace externo o recurso interno:

```ts
{
  id: 'mi-articulo-modelado',
  kind: 'local',
  title: 'Mi artículo de modelado',
  href: '/drautomatica/articulos/mi-articulo-modelado/',
  icon: 'fa-li fa fa-file-alt',
  articleSlug: 'mi-articulo-modelado',
  sections: ['modelado', 'inicio']
}
```

- `kind: 'local'`: artículo propio guardado como fragmento HTML en `html/mi-articulo-modelado.html` y publicado por Astro en `/drautomatica/articulos/mi-articulo-modelado/`.
- `kind: 'external'`: enlace a Medium, MathWorks, GitHub, Vercel u otro sitio externo. No necesita archivo en `html/`.
- `kind: 'asset'`: recurso interno como PDF, imagen o archivo publicado bajo `/drautomatica/pdf/...` u otra carpeta copiada.

La propiedad `sections` define dónde aparece la entrada. Por ejemplo, `sections: ['modelado', 'inicio']` la muestra en Modelado y en la portada. Para entradas simples no hace falta escribir `html`: Astro genera el enlace con `title` y `href`.

La propiedad `order` es opcional y define el orden dentro de cada sección solo cuando necesitas una posición específica. Si no se especifica `order` para una sección, la entrada se coloca al inicio de esa lista. Si varias entradas no tienen `order`, conservan entre ellas el orden en que aparecen en `catalog.ts`.

El distintivo `✨🆕` no debe escribirse en `html`. Astro lo agrega automáticamente a los primeros 8 elementos de `inicio` y a los primeros 5 elementos de las demás secciones.

Para un artículo local con ecuaciones, el archivo de `html/` debe contener solo el contenido del artículo, no una página HTML completa con `<html>`, `<head>` ni `<body>`. KaTeX se carga desde el layout de Astro.

Para un artículo externo en Medium, agrega solamente una entrada `external` al catálogo:

```ts
{
  id: 'mi-post-medium',
  kind: 'external',
  title: 'Mi post en Medium',
  href: 'https://medium.com/p/...',
  icon: 'fa-li fa-brands fa-medium',
  sections: ['modelado', 'inicio']
}
```

Usa `html` solo si la entrada necesita marcado adicional, por ejemplo una descripción, un enlace secundario a PDF, una imagen de MathWorks File Exchange o texto en negritas dentro del enlace.

Los archivos legacy como `modelado.html` o `Python.html` se conservan como fuente histórica y para partes introductorias durante esta migración, pero las listas nuevas de publicaciones se gestionan desde el catálogo de Astro.

## Publicación

`npm run build` genera la salida estática en `../drautomatica/`. El workflow de GitHub Actions incluido recompila esa carpeta cuando cambia `astro-drautomatica/**` o cualquiera de los contenidos legacy vinculados.

URL objetivo: `https://isantosruiz.github.io/drautomatica/`.

La configuración actual usa `site: 'https://isantosruiz.github.io'` y `base: '/drautomatica'`. Para mover el portal a `https://drautomatica.com/`, la intención es cambiar esos valores de Astro sin rediseñar páginas ni reescribir el contenido.
