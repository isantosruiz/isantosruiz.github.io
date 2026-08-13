export type SectionId = 'inicio' | 'modelado' | 'simulacion' | 'control' | 'optimizacion' | 'miscelanea' | 'python' | 'matlab' | 'latex';

export type CatalogEntryKind = 'local' | 'external' | 'asset';

export interface CatalogEntry {
  id: string;
  kind: CatalogEntryKind;
  title: string;
  href: string;
  html: string;
  icon: string;
  articleSlug?: string;
  sections: SectionId[];
  order: Partial<Record<SectionId, number>>;
}

export const catalogEntries = [
  {
    "id": "math-notebook-cuaderno-de-matematicas-simbolicas",
    "kind": "external",
    "title": "Math Notebook: Cuaderno de matemáticas simbólicas",
    "href": "https://mnotebook.vercel.app/",
    "html": "<a href=\"https://mnotebook.vercel.app/\">Math Notebook: Cuaderno de matemáticas simbólicas</a>✨🆕",
    "icon": "fa-li fa fa-cloud",
    "sections": [
      "inicio"
    ],
    "order": {
      "inicio": 0
    }
  },
  {
    "id": "graficas-en-tiempo-real-con-matlab",
    "kind": "external",
    "title": "Gráficas en tiempo real con MATLAB",
    "href": "https://medium.com/p/bd732f5c2c30/",
    "html": "<a href=\"https://medium.com/p/bd732f5c2c30/\">Gráficas en tiempo real con MATLAB</a>✨🆕",
    "icon": "fa-li fa-brands fa-medium",
    "sections": [
      "inicio"
    ],
    "order": {
      "inicio": 1
    }
  },
  {
    "id": "como-aprenden-las-maquinas-cinco-enfoques-del-aprendizaje-automatico",
    "kind": "external",
    "title": "Cómo aprenden las máquinas: cinco enfoques del aprendizaje automático",
    "href": "https://medium.com/p/46f0accb297f/",
    "html": "<a href=\"https://medium.com/p/46f0accb297f/\">Cómo aprenden las máquinas: cinco enfoques del aprendizaje automático</a>✨🆕",
    "icon": "fa-li fa-brands fa-medium",
    "sections": [
      "inicio"
    ],
    "order": {
      "inicio": 2
    }
  },
  {
    "id": "que-debe-contener-la-introduccion-de-un-articulo-cientifico",
    "kind": "external",
    "title": "¿Qué debe contener la introducción de un artículo científico?",
    "href": "https://medium.com/p/092974a9b4a5/",
    "html": "<a href=\"https://medium.com/p/092974a9b4a5/\">¿Qué debe contener la introducción de un artículo científico?</a>✨🆕",
    "icon": "fa-li fa-brands fa-medium",
    "sections": [
      "inicio"
    ],
    "order": {
      "inicio": 3
    }
  },
  {
    "id": "conectando-la-placa-m5stack-core2-for-aws-con-matlab",
    "kind": "external",
    "title": "Conectando la placa M5Stack Core2 for AWS con MATLAB",
    "href": "https://medium.com/p/276430eba9e8/",
    "html": "<a href=\"https://medium.com/p/276430eba9e8/\">Conectando la placa M5Stack Core2 for AWS con MATLAB</a>✨🆕",
    "icon": "fa-li fa-brands fa-medium",
    "sections": [
      "inicio"
    ],
    "order": {
      "inicio": 4
    }
  },
  {
    "id": "la-teoria-de-la-informacion-en-el-mundo-digital",
    "kind": "external",
    "title": "La teoría de la información en el mundo digital",
    "href": "https://medium.com/p/b5f52913c721/",
    "html": "<a href=\"https://medium.com/p/b5f52913c721/\">La teoría de la información en el mundo digital</a>✨🆕",
    "icon": "fa-li fa-brands fa-medium",
    "sections": [
      "inicio"
    ],
    "order": {
      "inicio": 5
    }
  },
  {
    "id": "como-sabe-un-robot-movil-donde-esta",
    "kind": "external",
    "title": "Cómo sabe un robot móvil dónde está",
    "href": "https://medium.com/p/ebab90f44cd9/",
    "html": "<a href=\"https://medium.com/p/ebab90f44cd9/\">Cómo sabe un robot móvil dónde está</a>✨🆕",
    "icon": "fa-li fa-brands fa-medium",
    "sections": [
      "inicio"
    ],
    "order": {
      "inicio": 6
    }
  },
  {
    "id": "control-adaptable-basado-en-un-modelo-de-referencia",
    "kind": "external",
    "title": "Control adaptable basado en un modelo de referencia",
    "href": "https://medium.com/p/34277da598ec",
    "html": "<a href=\"https://medium.com/p/34277da598ec\">Control adaptable basado en un modelo de referencia</a>✨🆕",
    "icon": "fa-li fa-brands fa-medium",
    "sections": [
      "inicio"
    ],
    "order": {
      "inicio": 7
    }
  },
  {
    "id": "transformadas-de-laplace-y-z-herramientas-para-resolver-la-dinamica-de-sistemas-",
    "kind": "external",
    "title": "Transformadas de Laplace y Z: herramientas para resolver la dinámica de sistemas continuos y discretos",
    "href": "https://medium.com/p/b65daadad1cb",
    "html": "<a href=\"https://medium.com/p/b65daadad1cb\">Transformadas de Laplace y Z: herramientas para resolver la dinámica de sistemas continuos y discretos</a>",
    "icon": "fa-li fa-brands fa-medium",
    "sections": [
      "inicio"
    ],
    "order": {
      "inicio": 8
    }
  },
  {
    "id": "el-lazo-de-corriente-de-4-20-ma-sin-enredos",
    "kind": "external",
    "title": "El lazo de corriente de 4-20 mA sin enredos",
    "href": "https://medium.com/p/9214755adc97",
    "html": "<a href=\"https://medium.com/p/9214755adc97\">El lazo de corriente de 4-20 mA sin enredos</a>",
    "icon": "fa-li fa-brands fa-medium",
    "sections": [
      "inicio"
    ],
    "order": {
      "inicio": 9
    }
  },
  {
    "id": "funcion-de-transferencia-una-herramienta-central-en-sistemas-dinamicos-y-control",
    "kind": "external",
    "title": "Función de transferencia: una herramienta central en sistemas dinámicos y control",
    "href": "https://medium.com/p/8cbcab825ccd",
    "html": "<a href=\"https://medium.com/p/8cbcab825ccd\">Función de transferencia: una herramienta central en sistemas dinámicos y control</a>",
    "icon": "fa-li fa-brands fa-medium",
    "sections": [
      "inicio"
    ],
    "order": {
      "inicio": 10
    }
  },
  {
    "id": "icapture-e-isolve-una-propuesta-integrada-para-la-captura-y-analisis-de-circuito",
    "kind": "external",
    "title": "iCapture e iSolve: una propuesta integrada para la captura y análisis de circuitos lineales",
    "href": "https://medium.com/p/7fe00b57ce7e",
    "html": "<a href=\"https://medium.com/p/7fe00b57ce7e\">iCapture e iSolve: una propuesta integrada para la captura y análisis de circuitos lineales</a>",
    "icon": "fa-li fa-brands fa-medium",
    "sections": [
      "inicio"
    ],
    "order": {
      "inicio": 11
    }
  },
  {
    "id": "how-to-turn-a-python-script-into-a-standalone-command-line-tool",
    "kind": "external",
    "title": "How to Turn a Python Script Into a Standalone Command-Line Tool",
    "href": "https://medium.com/p/3175bfec8a77",
    "html": "<a href=\"https://medium.com/p/3175bfec8a77\">How to Turn a Python Script Into a Standalone Command-Line Tool</a>",
    "icon": "fa-li fa-brands fa-medium",
    "sections": [
      "inicio"
    ],
    "order": {
      "inicio": 12
    }
  },
  {
    "id": "matriz-de-hurwitz-y-tabla-de-routh-dos-herramientas-algebraicas-para-analisis-y-",
    "kind": "asset",
    "title": "Matriz de Hurwitz y tabla de Routh: dos herramientas algebraicas para análisis y diseño de control (doi: 10.5281/zenodo.19042506 )",
    "href": "/drautomatica/pdf/routh_hurwitz.pdf",
    "html": "<a href=\"/drautomatica/pdf/routh_hurwitz.pdf\">Matriz de Hurwitz y tabla de Routh: dos herramientas algebraicas para análisis y diseño de control</a><br>(doi: <a href=\"https://doi.org/10.5281/zenodo.19042505\">10.5281/zenodo.19042506</a>)",
    "icon": "fa-li fa fa-file-pdf",
    "sections": [
      "inicio"
    ],
    "order": {
      "inicio": 13
    }
  },
  {
    "id": "senales-sistemas-y-modelos",
    "kind": "external",
    "title": "Señales, sistemas y modelos",
    "href": "https://medium.com/p/ed4dfa66980f",
    "html": "<a href=\"https://medium.com/p/ed4dfa66980f\">Señales, sistemas y modelos</a>",
    "icon": "fa-li fa-brands fa-medium",
    "sections": [
      "inicio"
    ],
    "order": {
      "inicio": 14
    }
  },
  {
    "id": "pushpull",
    "kind": "local",
    "title": "Circuitos 1: Seguidor de emisor push-pull",
    "href": "/drautomatica/articulos/pushpull/",
    "html": "<a href=\"/drautomatica/articulos/pushpull/\" >Circuitos 1: Seguidor de emisor push-pull</a>",
    "icon": "fa-li fa fa-file-code",
    "articleSlug": "pushpull",
    "sections": [
      "inicio"
    ],
    "order": {
      "inicio": 15
    }
  },
  {
    "id": "biestable",
    "kind": "local",
    "title": "Circuitos 2: Multivibrador biestable",
    "href": "/drautomatica/articulos/biestable/",
    "html": "<a href=\"/drautomatica/articulos/biestable/\" >Circuitos 2: Multivibrador biestable</a>",
    "icon": "fa-li fa fa-file-code",
    "articleSlug": "biestable",
    "sections": [
      "inicio"
    ],
    "order": {
      "inicio": 16
    }
  },
  {
    "id": "como-redactar-un-informe-de-practica-de-laboratorio",
    "kind": "external",
    "title": "Cómo redactar un informe de práctica de laboratorio",
    "href": "https://medium.com/p/6d4138aab174",
    "html": "<a href=\"https://medium.com/p/6d4138aab174\">Cómo redactar un informe de práctica de laboratorio</a>",
    "icon": "fa-li fa-brands fa-medium",
    "sections": [
      "inicio"
    ],
    "order": {
      "inicio": 17
    }
  },
  {
    "id": "understanding-mqtt-the-lightweight-protocol-powering-the-internet-of-things",
    "kind": "external",
    "title": "Understanding MQTT: The Lightweight Protocol Powering the Internet of Things",
    "href": "https://medium.com/p/040fa78e41e1",
    "html": "<a href=\"https://medium.com/p/040fa78e41e1\">Understanding MQTT: The Lightweight Protocol Powering the Internet of Things</a>",
    "icon": "fa-li fa-brands fa-medium",
    "sections": [
      "inicio",
      "python"
    ],
    "order": {
      "inicio": 18,
      "python": 16
    }
  },
  {
    "id": "el-nuevo-arduino-y-su-modelo-de-doble-cerebro",
    "kind": "external",
    "title": "El nuevo Arduino y su modelo de “doble cerebro”",
    "href": "https://medium.com/p/036c6065a067",
    "html": "<a href=\"https://medium.com/p/036c6065a067\">El nuevo Arduino y su modelo de “doble cerebro”</a>",
    "icon": "fa-li fa-brands fa-medium",
    "sections": [
      "inicio"
    ],
    "order": {
      "inicio": 19
    }
  },
  {
    "id": "escalones-e-impulsos-base-para-el-modelado-de-senales-y-sistemas",
    "kind": "external",
    "title": "Escalones e impulsos: Base para el modelado de señales y sistemas",
    "href": "https://medium.com/p/c513480e735a",
    "html": "<a href=\"https://medium.com/p/c513480e735a\">Escalones e impulsos: Base para el modelado de señales y sistemas</a>",
    "icon": "fa-li fa-brands fa-medium",
    "sections": [
      "inicio",
      "modelado"
    ],
    "order": {
      "inicio": 20,
      "modelado": 0
    }
  },
  {
    "id": "modelado-del-decaimiento-radiactivo-mediante-ecuaciones-diferenciales",
    "kind": "external",
    "title": "Modelado del decaimiento radiactivo mediante ecuaciones diferenciales",
    "href": "https://medium.com/p/5b744c016840",
    "html": "<a href=\"https://medium.com/p/5b744c016840\">Modelado del decaimiento radiactivo mediante ecuaciones diferenciales</a>",
    "icon": "fa-li fa-brands fa-medium",
    "sections": [
      "inicio",
      "modelado"
    ],
    "order": {
      "inicio": 21,
      "modelado": 1
    }
  },
  {
    "id": "transformaciones-lineales-tutorial-paso-a-paso",
    "kind": "external",
    "title": "Transformaciones lineales: Tutorial paso a paso",
    "href": "https://medium.com/p/de35677b1026",
    "html": "<a href=\"https://medium.com/p/de35677b1026\">Transformaciones lineales: Tutorial paso a paso</a>",
    "icon": "fa-li fa-brands fa-medium",
    "sections": [
      "inicio",
      "matlab"
    ],
    "order": {
      "inicio": 22,
      "matlab": 9
    }
  },
  {
    "id": "como-escribir-un-articulo-cientifico",
    "kind": "external",
    "title": "Cómo escribir un artículo científico",
    "href": "https://medium.com/p/f6f074551577",
    "html": "<a href=\"https://medium.com/p/f6f074551577\">Cómo escribir un artículo científico</a>",
    "icon": "fa-li fa-brands fa-medium",
    "sections": [
      "inicio",
      "miscelanea"
    ],
    "order": {
      "inicio": 23,
      "miscelanea": 0
    }
  },
  {
    "id": "a-beginner-s-guide-to-writing-latex-macros",
    "kind": "external",
    "title": "A Beginner's Guide to Writing LaTeX Macros",
    "href": "https://medium.com/p/7a285d33091a",
    "html": "<a href=\"https://medium.com/p/7a285d33091a\">A Beginner's Guide to Writing LaTeX Macros</a>",
    "icon": "fa-li fa-brands fa-medium",
    "sections": [
      "inicio",
      "latex"
    ],
    "order": {
      "inicio": 24,
      "latex": 0
    }
  },
  {
    "id": "mastering-restful-apis-in-python",
    "kind": "external",
    "title": "Mastering RESTful APIs in Python",
    "href": "https://medium.com/p/f1917df89925",
    "html": "<a href=\"https://medium.com/p/f1917df89925\">Mastering RESTful APIs in Python</a>",
    "icon": "fa-li fa-brands fa-medium",
    "sections": [
      "inicio",
      "python"
    ],
    "order": {
      "inicio": 25,
      "python": 17
    }
  },
  {
    "id": "how-to-render-latex-in-jupyter-using-ipython",
    "kind": "external",
    "title": "How to Render LaTeX in Jupyter Using IPython",
    "href": "https://medium.com/p/4e1484431e21",
    "html": "<a href=\"https://medium.com/p/4e1484431e21\">How to Render LaTeX in Jupyter Using IPython</a>",
    "icon": "fa-li fa-brands fa-medium",
    "sections": [
      "inicio",
      "python",
      "latex"
    ],
    "order": {
      "inicio": 26,
      "python": 18,
      "latex": 1
    }
  },
  {
    "id": "gemelos-digitales-en-robotica-y-automatizacion",
    "kind": "asset",
    "title": "Gemelos digitales en robótica y automatización",
    "href": "/drautomatica/pdf/dt_robot.pdf",
    "html": "<a href=\"/drautomatica/pdf/dt_robot.pdf\">Gemelos digitales en robótica y automatización</a>",
    "icon": "fa-li fa fa-file-pdf",
    "sections": [
      "inicio",
      "modelado",
      "simulacion",
      "control",
      "optimizacion"
    ],
    "order": {
      "inicio": 27,
      "modelado": 2,
      "simulacion": 1,
      "control": 1,
      "optimizacion": 2
    }
  },
  {
    "id": "representacion-y-procesamiento-digital-de-imagenes",
    "kind": "external",
    "title": "Representación y procesamiento digital de imágenes",
    "href": "https://medium.com/p/1473531e72fb",
    "html": "<a href=\"https://medium.com/p/1473531e72fb\">Representación y procesamiento digital de imágenes</a>",
    "icon": "fa-li fa-brands fa-medium",
    "sections": [
      "inicio",
      "modelado",
      "control",
      "matlab"
    ],
    "order": {
      "inicio": 28,
      "modelado": 4,
      "control": 2,
      "matlab": 11
    }
  },
  {
    "id": "ad-hominem",
    "kind": "local",
    "title": "Falacias 1: Falacia ad hominem",
    "href": "/drautomatica/articulos/ad_hominem/",
    "html": "<a href=\"/drautomatica/articulos/ad_hominem/\">Falacias 1: Falacia ad hominem</a>",
    "icon": "fa-li fa fa-file-code",
    "articleSlug": "ad_hominem",
    "sections": [
      "inicio",
      "miscelanea"
    ],
    "order": {
      "inicio": 29,
      "miscelanea": 1
    }
  },
  {
    "id": "ad-verecundiam",
    "kind": "local",
    "title": "Falacias 2: Falacia ad verecundiam",
    "href": "/drautomatica/articulos/ad_verecundiam/",
    "html": "<a href=\"/drautomatica/articulos/ad_verecundiam/\">Falacias 2: Falacia ad verecundiam</a>",
    "icon": "fa-li fa fa-file-code",
    "articleSlug": "ad_verecundiam",
    "sections": [
      "inicio",
      "miscelanea"
    ],
    "order": {
      "inicio": 30,
      "miscelanea": 2
    }
  },
  {
    "id": "ad-populum",
    "kind": "local",
    "title": "Falacias 3: Falacia ad populum",
    "href": "/drautomatica/articulos/ad_populum/",
    "html": "<a href=\"/drautomatica/articulos/ad_populum/\">Falacias 3: Falacia ad populum</a>",
    "icon": "fa-li fa fa-file-code",
    "articleSlug": "ad_populum",
    "sections": [
      "inicio",
      "miscelanea"
    ],
    "order": {
      "inicio": 31,
      "miscelanea": 3
    }
  },
  {
    "id": "ad-lazarum",
    "kind": "local",
    "title": "Falacias 4: Falacia ad lazarum",
    "href": "/drautomatica/articulos/ad_lazarum/",
    "html": "<a href=\"/drautomatica/articulos/ad_lazarum/\">Falacias 4: Falacia ad lazarum</a>",
    "icon": "fa-li fa fa-file-code",
    "articleSlug": "ad_lazarum",
    "sections": [
      "inicio",
      "miscelanea"
    ],
    "order": {
      "inicio": 32,
      "miscelanea": 4
    }
  },
  {
    "id": "falsa-causa",
    "kind": "local",
    "title": "Falacias 5: Falacia de falsa causa",
    "href": "/drautomatica/articulos/falsa_causa/",
    "html": "<a href=\"/drautomatica/articulos/falsa_causa/\">Falacias 5: Falacia de falsa causa</a>",
    "icon": "fa-li fa fa-file-code",
    "articleSlug": "falsa_causa",
    "sections": [
      "inicio",
      "miscelanea"
    ],
    "order": {
      "inicio": 33,
      "miscelanea": 5
    }
  },
  {
    "id": "falsa-dicotomia",
    "kind": "local",
    "title": "Falacias 6: Falacia de falsa dicotomía",
    "href": "/drautomatica/articulos/falsa_dicotomia/",
    "html": "<a href=\"/drautomatica/articulos/falsa_dicotomia/\">Falacias 6: Falacia de falsa dicotomía</a>",
    "icon": "fa-li fa fa-file-code",
    "articleSlug": "falsa_dicotomia",
    "sections": [
      "inicio",
      "miscelanea"
    ],
    "order": {
      "inicio": 34,
      "miscelanea": 6
    }
  },
  {
    "id": "pdfcompress-reduce-el-tamano-de-archivos-pdf",
    "kind": "external",
    "title": "pdfcompress : Reduce el tamaño de archivos PDF",
    "href": "https://pdfcompress-psi.vercel.app/",
    "html": "<a href=\"https://pdfcompress-psi.vercel.app/\"><strong>pdfcompress</strong>: Reduce el tamaño de archivos PDF</a>",
    "icon": "fa-li fa fa-cloud",
    "sections": [
      "inicio",
      "python"
    ],
    "order": {
      "inicio": 35,
      "python": 3
    }
  },
  {
    "id": "pdf2eps-convierte-archivos-pdf-a-eps",
    "kind": "external",
    "title": "pdf2eps : Convierte archivos PDF a EPS",
    "href": "https://pdf2eps.vercel.app/",
    "html": "<a href=\"https://pdf2eps.vercel.app/\"><strong>pdf2eps</strong>: Convierte archivos PDF a EPS</a>",
    "icon": "fa-li fa fa-cloud",
    "sections": [
      "inicio",
      "python"
    ],
    "order": {
      "inicio": 36,
      "python": 4
    }
  },
  {
    "id": "pdfcrop-recorta-margenes-vacios-en-paginas-pdf",
    "kind": "external",
    "title": "pdfcrop : Recorta márgenes vacíos en páginas PDF",
    "href": "https://pdfcrop.vercel.app/",
    "html": "<a href=\"https://pdfcrop.vercel.app/\"><strong>pdfcrop</strong>: Recorta márgenes vacíos en páginas PDF</a>",
    "icon": "fa-li fa fa-cloud",
    "sections": [
      "inicio",
      "python"
    ],
    "order": {
      "inicio": 37,
      "python": 5
    }
  },
  {
    "id": "simplificador-de-expresiones-booleanas",
    "kind": "external",
    "title": "Simplificador de expresiones booleanas",
    "href": "https://logic-liard.vercel.app/",
    "html": "<a href=\"https://logic-liard.vercel.app/\">Simplificador de expresiones booleanas</a>",
    "icon": "fa-li fa fa-cloud",
    "sections": [
      "inicio",
      "python"
    ],
    "order": {
      "inicio": 38,
      "python": 6
    }
  },
  {
    "id": "calculadora-de-integrales",
    "kind": "external",
    "title": "Calculadora de integrales",
    "href": "https://integrador-zeta-liard.vercel.app/",
    "html": "<a href=\"https://integrador-zeta-liard.vercel.app/\">Calculadora de integrales</a>",
    "icon": "fa-li fa fa-cloud",
    "sections": [
      "inicio",
      "python"
    ],
    "order": {
      "inicio": 39,
      "python": 7
    }
  },
  {
    "id": "suma-de-riemann",
    "kind": "external",
    "title": "Suma de Riemann",
    "href": "https://riemann-omega.vercel.app/",
    "html": "<a href=\"https://riemann-omega.vercel.app/\">Suma de Riemann</a>",
    "icon": "fa-li fa fa-cloud",
    "sections": [
      "inicio",
      "python"
    ],
    "order": {
      "inicio": 40,
      "python": 8
    }
  },
  {
    "id": "calculadora-de-laplace",
    "kind": "external",
    "title": "Calculadora de Laplace",
    "href": "https://laplace-psi.vercel.app/",
    "html": "<a href=\"https://laplace-psi.vercel.app/\">Calculadora de Laplace</a>",
    "icon": "fa-li fa fa-cloud",
    "sections": [
      "inicio",
      "python"
    ],
    "order": {
      "inicio": 41,
      "python": 9
    }
  },
  {
    "id": "resolucion-simbolica-de-ecuaciones",
    "kind": "external",
    "title": "Resolución simbólica de ecuaciones",
    "href": "https://solver-liart.vercel.app/",
    "html": "<a href=\"https://solver-liart.vercel.app/\">Resolución simbólica de ecuaciones</a>",
    "icon": "fa-li fa fa-cloud",
    "sections": [
      "inicio",
      "python"
    ],
    "order": {
      "inicio": 42,
      "python": 10
    }
  },
  {
    "id": "regresion-lineal-por-minimos-cuadrados",
    "kind": "external",
    "title": "Regresión lineal por mínimos cuadrados",
    "href": "https://reglin.vercel.app/",
    "html": "<a href=\"https://reglin.vercel.app/\">Regresión lineal por mínimos cuadrados</a>",
    "icon": "fa-li fa fa-cloud",
    "sections": [
      "inicio",
      "python"
    ],
    "order": {
      "inicio": 43,
      "python": 11
    }
  },
  {
    "id": "area-bajo-la-curva-normal",
    "kind": "external",
    "title": "Área bajo la curva normal",
    "href": "https://normal-virid.vercel.app/",
    "html": "<a href=\"https://normal-virid.vercel.app/\">Área bajo la curva normal</a>",
    "icon": "fa-li fa fa-cloud",
    "sections": [
      "inicio",
      "python"
    ],
    "order": {
      "inicio": 44,
      "python": 12
    }
  },
  {
    "id": "epanet-network-map",
    "kind": "external",
    "title": "EPANET Network Map",
    "href": "https://epanetmap.vercel.app/",
    "html": "<a href=\"https://epanetmap.vercel.app/\">EPANET Network Map</a>",
    "icon": "fa-li fa fa-cloud",
    "sections": [
      "inicio",
      "python"
    ],
    "order": {
      "inicio": 45,
      "python": 13
    }
  },
  {
    "id": "filtro-de-kalman-tutorial-interactivo",
    "kind": "external",
    "title": "Filtro de Kalman — Tutorial interactivo",
    "href": "https://kalman-rho.vercel.app/",
    "html": "<a href=\"https://kalman-rho.vercel.app/\">Filtro de Kalman — Tutorial interactivo</a>",
    "icon": "fa-li fa fa-cloud",
    "sections": [
      "inicio",
      "python"
    ],
    "order": {
      "inicio": 46,
      "python": 14
    }
  },
  {
    "id": "derivacion-paso-a-paso-tutorial-interactivo",
    "kind": "external",
    "title": "Derivación paso a paso — Tutorial interactivo",
    "href": "https://derivada-psi.vercel.app/",
    "html": "<a href=\"https://derivada-psi.vercel.app/\">Derivación paso a paso — Tutorial interactivo</a>",
    "icon": "fa-li fa fa-cloud",
    "sections": [
      "inicio",
      "python"
    ],
    "order": {
      "inicio": 47,
      "python": 15
    }
  },
  {
    "id": "forma-escalonada-reducida-por-renglones-tutorial-interactivo",
    "kind": "external",
    "title": "Forma escalonada reducida por renglones — Tutorial interactivo",
    "href": "https://rref-three.vercel.app/",
    "html": "<a href=\"https://rref-three.vercel.app/\">Forma escalonada reducida por renglones — Tutorial interactivo</a>",
    "icon": "fa-li fa fa-cloud",
    "sections": [
      "inicio"
    ],
    "order": {
      "inicio": 48
    }
  },
  {
    "id": "perplexity",
    "kind": "local",
    "title": "Perplexity: Respuestas claras sin alucinar",
    "href": "/drautomatica/articulos/perplexity/",
    "html": "<a href=\"/drautomatica/articulos/perplexity/\" >Perplexity: Respuestas claras sin alucinar</a>",
    "icon": "fa-li fa fa-file-code",
    "articleSlug": "perplexity",
    "sections": [
      "inicio",
      "miscelanea"
    ],
    "order": {
      "inicio": 49,
      "miscelanea": 14
    }
  },
  {
    "id": "mindmaps",
    "kind": "local",
    "title": "Mapas mentales con PlantUML",
    "href": "/drautomatica/articulos/mindmaps/",
    "html": "<a href=\"/drautomatica/articulos/mindmaps/\" >Mapas mentales con PlantUML</a>",
    "icon": "fa-li fa fa-file-code",
    "articleSlug": "mindmaps",
    "sections": [
      "inicio",
      "modelado",
      "miscelanea"
    ],
    "order": {
      "inicio": 50,
      "modelado": 6,
      "miscelanea": 13
    }
  },
  {
    "id": "la-energia-conceptos-y-desafios",
    "kind": "external",
    "title": "La energía: Conceptos y desafíos",
    "href": "https://medium.com/p/2ba248831a15",
    "html": "<a href=\"https://medium.com/p/2ba248831a15\">La energía: Conceptos y desafíos</a>",
    "icon": "fa-li fa-brands fa-medium",
    "sections": [
      "inicio",
      "miscelanea"
    ],
    "order": {
      "inicio": 51,
      "miscelanea": 15
    }
  },
  {
    "id": "resolucion-de-ecuaciones-diferenciales-en-python-con-scipy-nbsp",
    "kind": "external",
    "title": "Resolución de ecuaciones diferenciales en Python con SciPy &nbsp;",
    "href": "https://medium.com/p/b4eb5ed4c188",
    "html": "<a href=\"https://medium.com/p/b4eb5ed4c188\">Resolución de ecuaciones diferenciales en Python con SciPy</a>&nbsp;<a href=\"/drautomatica/pdf/ode_scipy.pdf\"><i class=\"far fa-file-pdf\"></i></a>",
    "icon": "fa-li fa-brands fa-medium",
    "sections": [
      "inicio"
    ],
    "order": {
      "inicio": 52
    }
  },
  {
    "id": "pueden-las-maquinas-realmente-aprender",
    "kind": "external",
    "title": "¿Pueden las máquinas realmente aprender?",
    "href": "https://medium.com/p/2176e573da98",
    "html": "<a href=\"https://medium.com/p/2176e573da98\">¿Pueden las máquinas realmente aprender?</a>",
    "icon": "fa-li fa-brands fa-medium",
    "sections": [
      "inicio",
      "miscelanea"
    ],
    "order": {
      "inicio": 53,
      "miscelanea": 7
    }
  },
  {
    "id": "como-se-prueba-una-hipotesis-estadistica-en-ciencias-e-ingenieria",
    "kind": "external",
    "title": "Cómo se prueba una hipótesis estadística en ciencias e ingeniería",
    "href": "https://medium.com/p/87c6a398eedb",
    "html": "<a href=\"https://medium.com/p/87c6a398eedb\">Cómo se prueba una hipótesis estadística en ciencias e ingeniería</a>",
    "icon": "fa-li fa-brands fa-medium",
    "sections": [
      "inicio",
      "matlab"
    ],
    "order": {
      "inicio": 54,
      "matlab": 12
    }
  },
  {
    "id": "que-es-la-ciencia-y-para-que-sirve",
    "kind": "external",
    "title": "¿Qué es la ciencia y para qué sirve?",
    "href": "https://medium.com/p/256a1270d1a6",
    "html": "<a href=\"https://medium.com/p/256a1270d1a6\">¿Qué es la ciencia y para qué sirve?</a>",
    "icon": "fa-li fa-brands fa-medium",
    "sections": [
      "inicio",
      "miscelanea"
    ],
    "order": {
      "inicio": 55,
      "miscelanea": 8
    }
  },
  {
    "id": "la-publicacion-en-acceso-abierto",
    "kind": "external",
    "title": "La publicación en acceso abierto",
    "href": "https://medium.com/p/eac003f30c40",
    "html": "<a href=\"https://medium.com/p/eac003f30c40\">La publicación en acceso abierto</a>",
    "icon": "fa-li fa-brands fa-medium",
    "sections": [
      "inicio",
      "miscelanea"
    ],
    "order": {
      "inicio": 56,
      "miscelanea": 9
    }
  },
  {
    "id": "diagramas-en-latex-con-tikz",
    "kind": "external",
    "title": "Diagramas en LaTeX con TikZ",
    "href": "https://medium.com/p/bffe8b521473",
    "html": "<a href=\"https://medium.com/p/bffe8b521473\">Diagramas en LaTeX con TikZ</a>",
    "icon": "fa-li fa-brands fa-medium",
    "sections": [
      "inicio",
      "latex"
    ],
    "order": {
      "inicio": 57,
      "latex": 2
    }
  },
  {
    "id": "homogeneous-transformations-in-robotics-a-comprehensive-tutorial-with-examples",
    "kind": "external",
    "title": "Homogeneous transformations in Robotics: A comprehensive tutorial with examples",
    "href": "https://medium.com/p/e36cd3709f41",
    "html": "<a href=\"https://medium.com/p/e36cd3709f41\">Homogeneous transformations in Robotics: A comprehensive tutorial with examples</a>",
    "icon": "fa-li fa-brands fa-medium",
    "sections": [
      "inicio",
      "modelado",
      "simulacion",
      "control",
      "matlab"
    ],
    "order": {
      "inicio": 58,
      "modelado": 8,
      "simulacion": 3,
      "control": 4,
      "matlab": 13
    }
  },
  {
    "id": "rendering-latex-in-web-browsers-katex-vs-mathjax",
    "kind": "external",
    "title": "Rendering LaTeX in Web Browsers: KaTeX vs. MathJax",
    "href": "https://medium.com/p/0d78a817340b",
    "html": "<a href=\"https://medium.com/p/0d78a817340b\">Rendering LaTeX in Web Browsers: KaTeX vs. MathJax</a>",
    "icon": "fa-li fa-brands fa-medium",
    "sections": [
      "inicio",
      "latex"
    ],
    "order": {
      "inicio": 59,
      "latex": 3
    }
  },
  {
    "id": "events-in-python",
    "kind": "external",
    "title": "Events in Python",
    "href": "https://medium.com/p/e2b3cb76ac2d",
    "html": "<a href=\"https://medium.com/p/e2b3cb76ac2d\">Events in Python</a>",
    "icon": "fa-li fa-brands fa-medium",
    "sections": [
      "inicio",
      "modelado",
      "python"
    ],
    "order": {
      "inicio": 60,
      "modelado": 9,
      "python": 20
    }
  },
  {
    "id": "exceptions-in-python",
    "kind": "external",
    "title": "Exceptions in Python",
    "href": "https://medium.com/p/4e392143e623",
    "html": "<a href=\"https://medium.com/p/4e392143e623\">Exceptions in Python</a>",
    "icon": "fa-li fa-brands fa-medium",
    "sections": [
      "inicio",
      "python"
    ],
    "order": {
      "inicio": 61,
      "python": 21
    }
  },
  {
    "id": "introduccion-a-duckdb-la-base-de-datos-para-analisis-en-el-escritorio",
    "kind": "external",
    "title": "Introducción a DuckDB: la base de datos para análisis en el escritorio",
    "href": "https://medium.com/p/672b483b3a8f",
    "html": "<a href=\"https://medium.com/p/672b483b3a8f\">Introducción a DuckDB: la base de datos para análisis en el escritorio</a>",
    "icon": "fa-li fa-brands fa-medium",
    "sections": [
      "inicio",
      "python"
    ],
    "order": {
      "inicio": 62,
      "python": 22
    }
  },
  {
    "id": "introduccion-practica-al-machine-learning",
    "kind": "external",
    "title": "Introducción práctica al machine learning",
    "href": "https://medium.com/p/9d32143fa4a5",
    "html": "<a href=\"https://medium.com/p/9d32143fa4a5\">Introducción práctica al machine learning</a>",
    "icon": "fa-li fa-brands fa-medium",
    "sections": [
      "inicio",
      "modelado",
      "control",
      "matlab"
    ],
    "order": {
      "inicio": 63,
      "modelado": 10,
      "control": 5,
      "matlab": 14
    }
  },
  {
    "id": "introduccion-a-los-modelos-de-lenguaje-grande-llms",
    "kind": "external",
    "title": "Introducción a los Modelos de Lenguaje Grande (LLMs)",
    "href": "https://medium.com/p/ef99bf072d7c",
    "html": "<a href=\"https://medium.com/p/ef99bf072d7c\">Introducción a los Modelos de Lenguaje Grande (LLMs)</a>",
    "icon": "fa-li fa-brands fa-medium",
    "sections": [
      "inicio",
      "modelado",
      "python"
    ],
    "order": {
      "inicio": 64,
      "modelado": 5,
      "python": 23
    }
  },
  {
    "id": "graficos-mas-personalizables-en-matlab",
    "kind": "external",
    "title": "Gráficos más personalizables en MATLAB",
    "href": "https://medium.com/p/9ae4fbeb77d0",
    "html": "<a href=\"https://medium.com/p/9ae4fbeb77d0\">Gráficos más personalizables en MATLAB</a>",
    "icon": "fa-li fa-brands fa-medium",
    "sections": [
      "inicio",
      "matlab"
    ],
    "order": {
      "inicio": 65,
      "matlab": 15
    }
  },
  {
    "id": "solving-difference-equations-using-the-z-transform",
    "kind": "external",
    "title": "Solving difference equations using the Z-transform",
    "href": "https://medium.com/p/ec1dc0762b5e",
    "html": "<a href=\"https://medium.com/p/ec1dc0762b5e\">Solving difference equations using the Z-transform</a>",
    "icon": "fa-li fa-brands fa-medium",
    "sections": [
      "inicio",
      "modelado",
      "simulacion",
      "control",
      "matlab"
    ],
    "order": {
      "inicio": 66,
      "modelado": 11,
      "simulacion": 4,
      "control": 6,
      "matlab": 16
    }
  },
  {
    "id": "solving-ordinary-differential-equations-in-python-with-sympy",
    "kind": "external",
    "title": "Solving ordinary differential equations in Python with SymPy",
    "href": "https://medium.com/p/8bb28702d06e",
    "html": "<a href=\"https://medium.com/p/8bb28702d06e\">Solving ordinary differential equations in Python with SymPy</a>",
    "icon": "fa-li fa-brands fa-medium",
    "sections": [
      "inicio",
      "modelado",
      "simulacion",
      "control",
      "optimizacion",
      "python"
    ],
    "order": {
      "inicio": 67,
      "modelado": 12,
      "simulacion": 5,
      "control": 7,
      "optimizacion": 4,
      "python": 24
    }
  },
  {
    "id": "unlocking-python-s-regex-power-a-practical-guide",
    "kind": "external",
    "title": "Unlocking Python’s Regex Power: A Practical Guide",
    "href": "https://medium.com/p/bfa86979ddb3",
    "html": "<a href=\"https://medium.com/p/bfa86979ddb3\">Unlocking Python’s Regex Power: A Practical Guide</a>",
    "icon": "fa-li fa-brands fa-medium",
    "sections": [
      "inicio",
      "python"
    ],
    "order": {
      "inicio": 68,
      "python": 25
    }
  },
  {
    "id": "machine-learning-versus-deep-learning",
    "kind": "external",
    "title": "Machine Learning versus Deep Learning",
    "href": "https://medium.com/p/78d98a3d4256",
    "html": "<a href=\"https://medium.com/p/78d98a3d4256\">Machine Learning versus Deep Learning</a>",
    "icon": "fa-li fa-brands fa-medium",
    "sections": [
      "inicio",
      "modelado",
      "control",
      "matlab"
    ],
    "order": {
      "inicio": 69,
      "modelado": 13,
      "control": 8,
      "matlab": 17
    }
  },
  {
    "id": "mastering-curve-and-surface-plotting-in-matlab",
    "kind": "external",
    "title": "Mastering curve and surface plotting in MATLAB",
    "href": "https://medium.com/p/49a7c6b95c46",
    "html": "<a href=\"https://medium.com/p/49a7c6b95c46\">Mastering curve and surface plotting in MATLAB</a>",
    "icon": "fa-li fa-brands fa-medium",
    "sections": [
      "inicio",
      "matlab"
    ],
    "order": {
      "inicio": 70,
      "matlab": 18
    }
  },
  {
    "id": "detectores-de-texto-generado-por-ia-funcionamiento-limites-y-sesgos",
    "kind": "external",
    "title": "Detectores de texto generado por IA: Funcionamiento, límites y sesgos",
    "href": "https://medium.com/p/00d9f6503336",
    "html": "<a href=\"https://medium.com/p/00d9f6503336\">Detectores de texto generado por IA: Funcionamiento, límites y sesgos</a>",
    "icon": "fa-li fa-brands fa-medium",
    "sections": [
      "inicio",
      "miscelanea"
    ],
    "order": {
      "inicio": 71,
      "miscelanea": 10
    }
  },
  {
    "id": "optimizacion-global-con-algoritmos-geneticos-en-matlab-un-enfoque-practico",
    "kind": "external",
    "title": "Optimización global con algoritmos genéticos en MATLAB: Un enfoque práctico",
    "href": "https://medium.com/p/b4146bfa5246",
    "html": "<a href=\"https://medium.com/p/b4146bfa5246\">Optimización global con algoritmos genéticos en MATLAB: Un enfoque práctico</a>",
    "icon": "fa-li fa-brands fa-medium",
    "sections": [
      "inicio",
      "optimizacion",
      "matlab"
    ],
    "order": {
      "inicio": 72,
      "optimizacion": 0,
      "matlab": 19
    }
  },
  {
    "id": "iteradores-y-generadores-en-python",
    "kind": "external",
    "title": "Iteradores y generadores en Python",
    "href": "https://medium.com/p/3d0bb6b17471",
    "html": "<a href=\"https://medium.com/p/3d0bb6b17471\">Iteradores y generadores en Python</a>",
    "icon": "fa-li fa-brands fa-medium",
    "sections": [
      "inicio",
      "python"
    ],
    "order": {
      "inicio": 73,
      "python": 26
    }
  },
  {
    "id": "simulacion-de-dinamicas-continuas-con-matlab",
    "kind": "external",
    "title": "Simulación de dinámicas continuas con MATLAB",
    "href": "https://medium.com/p/1db4969870bc",
    "html": "<a href=\"https://medium.com/p/1db4969870bc\">Simulación de dinámicas continuas con MATLAB</a>",
    "icon": "fa-li fa-brands fa-medium",
    "sections": [
      "inicio",
      "modelado",
      "simulacion",
      "control",
      "optimizacion",
      "matlab"
    ],
    "order": {
      "inicio": 74,
      "modelado": 14,
      "simulacion": 6,
      "control": 9,
      "optimizacion": 5,
      "matlab": 20
    }
  },
  {
    "id": "analisis-hidraulico-y-simulacion-de-fugas-en-redes-de-distribucion-de-agua",
    "kind": "external",
    "title": "Análisis hidráulico y simulación de fugas en redes de distribución de agua",
    "href": "https://medium.com/p/38db6d644b46",
    "html": "<a href=\"https://medium.com/p/38db6d644b46\">Análisis hidráulico y simulación de fugas en redes de distribución de agua</a>",
    "icon": "fa-li fa-brands fa-medium",
    "sections": [
      "inicio",
      "modelado",
      "simulacion",
      "control",
      "optimizacion",
      "matlab"
    ],
    "order": {
      "inicio": 75,
      "modelado": 15,
      "simulacion": 7,
      "control": 10,
      "optimizacion": 6,
      "matlab": 21
    }
  },
  {
    "id": "modelado-dinamico-euler-lagrange-y-simulacion-usando-matlab",
    "kind": "external",
    "title": "Modelado dinámico Euler-Lagrange y simulación usando MATLAB",
    "href": "https://medium.com/p/11a1b797a66d",
    "html": "<a href=\"https://medium.com/p/11a1b797a66d\">Modelado dinámico Euler-Lagrange y simulación usando MATLAB</a>",
    "icon": "fa-li fa-brands fa-medium",
    "sections": [
      "inicio",
      "modelado",
      "simulacion",
      "control",
      "optimizacion",
      "matlab"
    ],
    "order": {
      "inicio": 76,
      "modelado": 3,
      "simulacion": 8,
      "control": 11,
      "optimizacion": 1,
      "matlab": 22
    }
  },
  {
    "id": "calculo-simbolico-con-sympy",
    "kind": "external",
    "title": "Cálculo simbólico con SymPy",
    "href": "https://medium.com/p/acf254ee2905",
    "html": "<a href=\"https://medium.com/p/acf254ee2905\">Cálculo simbólico con SymPy</a>",
    "icon": "fa-li fa-brands fa-medium",
    "sections": [
      "inicio",
      "simulacion",
      "python"
    ],
    "order": {
      "inicio": 77,
      "simulacion": 9,
      "python": 27
    }
  },
  {
    "id": "como-escribir-un-articulo-cientifico-en-latex",
    "kind": "external",
    "title": "Cómo escribir un artículo científico en LaTeX",
    "href": "https://medium.com/p/4506ebabd00a",
    "html": "<a href=\"https://medium.com/p/4506ebabd00a\">Cómo escribir un artículo científico en LaTeX</a>",
    "icon": "fa-li fa-brands fa-medium",
    "sections": [
      "inicio",
      "latex"
    ],
    "order": {
      "inicio": 78,
      "latex": 4
    }
  },
  {
    "id": "programacion-en-c-con-freertos-en-esp32",
    "kind": "external",
    "title": "Programación en C++ con FreeRTOS en ESP32",
    "href": "https://medium.com/p/1036e444e5f8",
    "html": "<a href=\"https://medium.com/p/1036e444e5f8\">Programación en C++ con FreeRTOS en ESP32</a>",
    "icon": "fa-li fa-brands fa-medium",
    "sections": [
      "inicio"
    ],
    "order": {
      "inicio": 79
    }
  },
  {
    "id": "diagramas-de-clases-uml-con-plantuml",
    "kind": "external",
    "title": "Diagramas de clases UML con PlantUML",
    "href": "https://medium.com/p/1a2d2f4792c4",
    "html": "<a href=\"https://medium.com/p/1a2d2f4792c4\">Diagramas de clases UML con PlantUML</a>",
    "icon": "fa-li fa-brands fa-medium",
    "sections": [
      "inicio",
      "modelado",
      "miscelanea",
      "python"
    ],
    "order": {
      "inicio": 80,
      "modelado": 16,
      "miscelanea": 12,
      "python": 28
    }
  },
  {
    "id": "domina-las-funciones-lambda-en-python",
    "kind": "external",
    "title": "Domina las funciones lambda en Python",
    "href": "https://medium.com/p/c797fbd29b81",
    "html": "<a href=\"https://medium.com/p/c797fbd29b81\">Domina las funciones lambda en Python</a>",
    "icon": "fa-li fa-brands fa-medium",
    "sections": [
      "inicio",
      "python"
    ],
    "order": {
      "inicio": 81,
      "python": 29
    }
  },
  {
    "id": "mastering-iterators-and-generators-in-python-a-practical-guide",
    "kind": "external",
    "title": "Mastering Iterators and Generators in Python: A Practical Guide",
    "href": "https://medium.com/p/1f77276e3b4d",
    "html": "<a href=\"https://medium.com/p/1f77276e3b4d\">Mastering Iterators and Generators in Python: A Practical Guide</a>",
    "icon": "fa-li fa-brands fa-medium",
    "sections": [
      "inicio",
      "python"
    ],
    "order": {
      "inicio": 82,
      "python": 30
    }
  },
  {
    "id": "mastering-json-in-python-oop-a-practical-guide",
    "kind": "external",
    "title": "Mastering JSON in Python OOP: A Practical Guide",
    "href": "https://medium.com/p/65b39e868c33",
    "html": "<a href=\"https://medium.com/p/65b39e868c33\">Mastering JSON in Python OOP: A Practical Guide</a>",
    "icon": "fa-li fa-brands fa-medium",
    "sections": [
      "inicio",
      "modelado",
      "python"
    ],
    "order": {
      "inicio": 83,
      "modelado": 17,
      "python": 31
    }
  },
  {
    "id": "mas-alla-de-los-contenidos-el-nuevo-rol-del-profesor-en-la-era-de-la-ia-generati",
    "kind": "external",
    "title": "Más allá de los contenidos: El nuevo rol del profesor en la era de la IA generativa",
    "href": "https://medium.com/p/dc539ffd403b",
    "html": "<a href=\"https://medium.com/p/dc539ffd403b\">Más allá de los contenidos: El nuevo rol del profesor en la era de la IA generativa</a>",
    "icon": "fa-li fa-brands fa-medium",
    "sections": [
      "inicio",
      "miscelanea"
    ],
    "order": {
      "inicio": 84,
      "miscelanea": 11
    }
  },
  {
    "id": "el-misterio-del-huevo-y-la-gallina",
    "kind": "external",
    "title": "El misterio del huevo y la gallina",
    "href": "https://medium.com/p/3a5bb61b76c9",
    "html": "<a href=\"https://medium.com/p/3a5bb61b76c9\">El misterio del huevo y la gallina</a>",
    "icon": "fa-li fa-brands fa-medium",
    "sections": [
      "inicio",
      "miscelanea"
    ],
    "order": {
      "inicio": 85,
      "miscelanea": 16
    }
  },
  {
    "id": "conoce-la-ingenieria-mecatronica",
    "kind": "external",
    "title": "Conoce la Ingeniería Mecatrónica",
    "href": "https://medium.com/p/2ec5acba9d4e",
    "html": "<a href=\"https://medium.com/p/2ec5acba9d4e\">Conoce la Ingeniería Mecatrónica</a>",
    "icon": "fa-li fa-brands fa-medium",
    "sections": [
      "inicio",
      "miscelanea"
    ],
    "order": {
      "inicio": 86,
      "miscelanea": 17
    }
  },
  {
    "id": "creacion-de-aplicaciones-gui-orientadas-a-objetos-en-matlab-mediante-codigo",
    "kind": "external",
    "title": "Creación de aplicaciones GUI orientadas a objetos en MATLAB mediante código",
    "href": "https://medium.com/p/2fc771b34714",
    "html": "<a href=\"https://medium.com/p/2fc771b34714\">Creación de aplicaciones GUI orientadas a objetos en MATLAB mediante código</a>",
    "icon": "fa-li fa-brands fa-medium",
    "sections": [
      "inicio",
      "modelado",
      "matlab"
    ],
    "order": {
      "inicio": 87,
      "modelado": 18,
      "matlab": 23
    }
  },
  {
    "id": "comunicacion-serie-entre-matlab-y-micropython",
    "kind": "external",
    "title": "Comunicación serie entre MATLAB y MicroPython",
    "href": "https://medium.com/p/61e1ff545166",
    "html": "<a href=\"https://medium.com/p/61e1ff545166\">Comunicación serie entre MATLAB y MicroPython</a>",
    "icon": "fa-li fa-brands fa-medium",
    "sections": [
      "inicio",
      "python",
      "matlab"
    ],
    "order": {
      "inicio": 88,
      "python": 32,
      "matlab": 24
    }
  },
  {
    "id": "dataclass-en-python",
    "kind": "external",
    "title": "Dataclass en Python",
    "href": "https://medium.com/p/cb9332d772c7",
    "html": "<a href=\"https://medium.com/p/cb9332d772c7\">Dataclass en Python</a>",
    "icon": "fa-li fa-brands fa-medium",
    "sections": [
      "inicio",
      "python"
    ],
    "order": {
      "inicio": 89,
      "python": 33
    }
  },
  {
    "id": "expresiones-regulares-en-matlab",
    "kind": "external",
    "title": "Expresiones regulares en MATLAB",
    "href": "https://medium.com/p/6e5b796668aa",
    "html": "<a href=\"https://medium.com/p/6e5b796668aa\">Expresiones regulares en MATLAB</a>",
    "icon": "fa-li fa-brands fa-medium",
    "sections": [
      "inicio"
    ],
    "order": {
      "inicio": 90
    }
  },
  {
    "id": "una-plantilla-de-papel-milimetrico-con-latex-y-tikz-en-minutos",
    "kind": "external",
    "title": "Una plantilla de papel milimétrico con LaTeX y TikZ en minutos",
    "href": "https://medium.com/p/20d7ed275e60",
    "html": "<a href=\"https://medium.com/p/20d7ed275e60\">Una plantilla de papel milimétrico con LaTeX y TikZ en minutos</a>",
    "icon": "fa-li fa-brands fa-medium",
    "sections": [
      "inicio"
    ],
    "order": {
      "inicio": 91
    }
  },
  {
    "id": "lo-cortes-no-quita-lo-valiente-pero-si-cuesta-el-costo-millonario-de-ser-amable-",
    "kind": "external",
    "title": "Lo cortés no quita lo valiente, pero sí cuesta: El costo millonario de ser amable con la IA",
    "href": "https://medium.com/p/049b610fe567",
    "html": "<a href=\"https://medium.com/p/049b610fe567\">Lo cortés no quita lo valiente, pero sí cuesta: El costo millonario de ser amable con la IA</a>",
    "icon": "fa-li fa-brands fa-medium",
    "sections": [
      "inicio"
    ],
    "order": {
      "inicio": 92
    }
  },
  {
    "id": "resolucion-de-ecuaciones-diferenciales-en-python-con-scipy",
    "kind": "external",
    "title": "Resolución de ecuaciones diferenciales en Python con SciPy",
    "href": "https://medium.com/p/b4eb5ed4c188",
    "html": "<a href=\"https://medium.com/p/b4eb5ed4c188\">Resolución de ecuaciones diferenciales en Python con SciPy</a>",
    "icon": "fa-li fa fa-file-lines",
    "sections": [
      "modelado",
      "simulacion",
      "control",
      "optimizacion",
      "python"
    ],
    "order": {
      "modelado": 7,
      "simulacion": 2,
      "control": 3,
      "optimizacion": 3,
      "python": 19
    }
  },
  {
    "id": "control-de-aprendizaje-iterativo",
    "kind": "asset",
    "title": "Control de aprendizaje iterativo",
    "href": "/drautomatica/pdf/ilc.pdf",
    "html": "<a href=\"/drautomatica/pdf/ilc.pdf\">Control de aprendizaje iterativo</a>",
    "icon": "fa-li fa fa-file-pdf",
    "sections": [
      "simulacion",
      "control"
    ],
    "order": {
      "simulacion": 0,
      "control": 0
    }
  },
  {
    "id": "math-notebook-cuaderno-interactivo-para-matematicas-simbolicas-en-python",
    "kind": "external",
    "title": "Math Notebook: Cuaderno interactivo para matemáticas simbólicas en Python",
    "href": "https://mnotebook.vercel.app/",
    "html": "<a href=\"https://mnotebook.vercel.app/\">Math Notebook: Cuaderno interactivo para matemáticas simbólicas en Python</a>✨🆕",
    "icon": "fa-li fa fa-cloud",
    "sections": [
      "python"
    ],
    "order": {
      "python": 0
    }
  },
  {
    "id": "pdfextract-script-para-extraer-paginas-especificas-de-un-archivo-pdf",
    "kind": "external",
    "title": "pdfextract : Script para extraer páginas específicas de un archivo PDF.",
    "href": "https://github.com/isantosruiz/pdfextract",
    "html": "<a href=\"https://github.com/isantosruiz/pdfextract\"><b>pdfextract</b></a>:\n                Script para extraer páginas específicas de un archivo PDF.\n                <a href=\"https://github.com/isantosruiz/pdfextract\"><i class=\"fa-brands fa-github\"></i></a>",
    "icon": "fa-li fa fa-file-code",
    "sections": [
      "python"
    ],
    "order": {
      "python": 1
    }
  },
  {
    "id": "mov2mp4-script-que-convierte-mov-a-mp4-usando-ffmpeg-via-subprocess",
    "kind": "external",
    "title": "mov2mp4 : Script que convierte .mov a .mp4 usando ffmpeg vía subprocess .",
    "href": "https://github.com/isantosruiz/mov2mp4",
    "html": "<a href=\"https://github.com/isantosruiz/mov2mp4\"><b>mov2mp4</b></a>:\n                Script que convierte <b>.mov</b> a <b>.mp4</b> usando <b>ffmpeg</b> vía <code>subprocess</code>.\n                <a href=\"https://github.com/isantosruiz/mov2mp4\"><i class=\"fa-brands fa-github\"></i></a>",
    "icon": "fa-li fa fa-file-code",
    "sections": [
      "python"
    ],
    "order": {
      "python": 2
    }
  },
  {
    "id": "moody-matlab-code-to-plot-the-moody-chart-showing-the-relationship-between-the-f",
    "kind": "external",
    "title": "Moody : MATLAB code to plot the Moody chart, showing the relationship between the friction factor and the Reynolds number for different roughness coefficients in a pipe.",
    "href": "https://la.mathworks.com/matlabcentral/fileexchange/72248-moody-chart",
    "html": "<a href=\"https://la.mathworks.com/matlabcentral/fileexchange/72248-moody-chart\"><b>Moody</b></a>:\n                MATLAB code to plot the Moody chart, showing the relationship between the friction factor and the Reynolds number for different roughness coefficients in a pipe.<br>\n                <a href=\"https://la.mathworks.com/matlabcentral/fileexchange/72248-moody-chart\"><img src=\"https://www.mathworks.com/matlabcentral/images/matlab-file-exchange.svg\" alt=\"Abrir en File Exchange\" /></a>",
    "icon": "fa-li fa fa-file-code",
    "sections": [
      "matlab"
    ],
    "order": {
      "matlab": 0
    }
  },
  {
    "id": "hurwitz-matlab-function-to-compute-the-hurwitz-matrix-and-the-principal-minors-f",
    "kind": "external",
    "title": "Hurwitz : MATLAB function to compute the Hurwitz matrix and the principal minors for a given polynomial.",
    "href": "https://la.mathworks.com/matlabcentral/fileexchange/71689-hurwitz-matrix",
    "html": "<a href=\"https://la.mathworks.com/matlabcentral/fileexchange/71689-hurwitz-matrix\"><b>Hurwitz</b></a>:\n                MATLAB function to compute the Hurwitz matrix and the principal minors for a given polynomial.<br>\n                <a href=\"https://la.mathworks.com/matlabcentral/fileexchange/71689-hurwitz-matrix\"><img src=\"https://www.mathworks.com/matlabcentral/images/matlab-file-exchange.svg\" alt=\"Abrir en File Exchange\" /></a>",
    "icon": "fa-li fa fa-file-code",
    "sections": [
      "matlab"
    ],
    "order": {
      "matlab": 1
    }
  },
  {
    "id": "rsolve-a-matlab-function-for-automatically-solving-linear-difference-equations-u",
    "kind": "external",
    "title": "rsolve : A MATLAB function for automatically solving linear difference equations using the Z-transform method.",
    "href": "https://la.mathworks.com/matlabcentral/fileexchange/181285-rsolve-difference-equation-solver",
    "html": "<a href=\"https://la.mathworks.com/matlabcentral/fileexchange/181285-rsolve-difference-equation-solver\"><b>rsolve</b></a>:\n                A MATLAB function for automatically solving linear difference equations using the Z-transform method.<br>\n                <a href=\"https://la.mathworks.com/matlabcentral/fileexchange/181285-rsolve-difference-equation-solver\"><img src=\"https://www.mathworks.com/matlabcentral/images/matlab-file-exchange.svg\" alt=\"Abrir en File Exchange\" /></a>",
    "icon": "fa-li fa fa-file-code",
    "sections": [
      "matlab"
    ],
    "order": {
      "matlab": 2
    }
  },
  {
    "id": "epanetonmap-matlab-code-to-read-epanet-inp-files-and-plot-pipelines-and-junction",
    "kind": "external",
    "title": "epanetOnMap : MATLAB code to read EPANET .INP files and plot pipelines and junction/reservoir markers on MATLAB geographic basemaps.",
    "href": "https://la.mathworks.com/matlabcentral/fileexchange/73001-epanetonmap",
    "html": "<a href=\"https://la.mathworks.com/matlabcentral/fileexchange/73001-epanetonmap\"><b>epanetOnMap</b></a>:\n                MATLAB code to read EPANET .INP files and plot pipelines and junction/reservoir markers on MATLAB geographic basemaps.<br>\n                <a href=\"https://la.mathworks.com/matlabcentral/fileexchange/73001-epanetonmap\"><img src=\"https://www.mathworks.com/matlabcentral/images/matlab-file-exchange.svg\" alt=\"Abrir en File Exchange\" /></a>",
    "icon": "fa-li fa fa-file-code",
    "sections": [
      "matlab"
    ],
    "order": {
      "matlab": 3
    }
  },
  {
    "id": "getfigdata-matlab-function-to-extract-the-xyz-data-from-a-fig-file",
    "kind": "external",
    "title": "getfigdata : MATLAB function to extract the xyz data from a FIG file.",
    "href": "https://la.mathworks.com/matlabcentral/fileexchange/72980-getfigdata",
    "html": "<a href=\"https://la.mathworks.com/matlabcentral/fileexchange/72980-getfigdata\"><b>getfigdata</b></a>:\n                MATLAB function to extract the xyz data from a FIG file.<br>\n                <a href=\"https://la.mathworks.com/matlabcentral/fileexchange/72980-getfigdata\"><img src=\"https://www.mathworks.com/matlabcentral/images/matlab-file-exchange.svg\" alt=\"Abrir en File Exchange\" /></a>",
    "icon": "fa-li fa fa-file-code",
    "sections": [
      "matlab"
    ],
    "order": {
      "matlab": 4
    }
  },
  {
    "id": "water-properties-matlab-class-to-compute-some-physical-properties-of-water-depen",
    "kind": "external",
    "title": "Water Properties : MATLAB class to compute some physical properties of water dependent on temperature, from 1 to 99 celsius.",
    "href": "https://la.mathworks.com/matlabcentral/fileexchange/71072-water-properties",
    "html": "<a href=\"https://la.mathworks.com/matlabcentral/fileexchange/71072-water-properties\"><b>Water Properties</b></a>:\n                MATLAB class to compute some physical properties of water dependent on temperature, from 1 to 99 celsius.<br>\n                <a href=\"https://la.mathworks.com/matlabcentral/fileexchange/71072-water-properties\"><img src=\"https://www.mathworks.com/matlabcentral/images/matlab-file-exchange.svg\" alt=\"Abrir en File Exchange\" /></a>",
    "icon": "fa-li fa fa-file-code",
    "sections": [
      "matlab"
    ],
    "order": {
      "matlab": 5
    }
  },
  {
    "id": "trapezoidal-matlab-function-to-simulate-linear-dynamic-systems-using-trapezoidal",
    "kind": "external",
    "title": "Trapezoidal : MATLAB function to simulate linear dynamic systems using trapezoidal integration method with constant time step.",
    "href": "https://la.mathworks.com/matlabcentral/fileexchange/71106-trapezoidal",
    "html": "<a href=\"https://la.mathworks.com/matlabcentral/fileexchange/71106-trapezoidal\"><b>Trapezoidal</b></a>:\n                MATLAB function to simulate linear dynamic systems using trapezoidal integration method with constant time step.<br>\n                <a href=\"https://la.mathworks.com/matlabcentral/fileexchange/71106-trapezoidal\"><img src=\"https://www.mathworks.com/matlabcentral/images/matlab-file-exchange.svg\" alt=\"Abrir en File Exchange\" /></a>",
    "icon": "fa-li fa fa-file-code",
    "sections": [
      "matlab"
    ],
    "order": {
      "matlab": 6
    }
  },
  {
    "id": "inequalityplot-matlab-function-to-plot-inequalities-in-2-d-space",
    "kind": "external",
    "title": "inequalityplot : MATLAB function to plot inequalities in 2-D space.",
    "href": "https://la.mathworks.com/matlabcentral/fileexchange/114895-inequalityplot",
    "html": "<a href=\"https://la.mathworks.com/matlabcentral/fileexchange/114895-inequalityplot\"><b>inequalityplot</b></a>:\n                MATLAB function to plot inequalities in 2-D space.<br>\n                <a href=\"https://la.mathworks.com/matlabcentral/fileexchange/114895-inequalityplot\"><img src=\"https://www.mathworks.com/matlabcentral/images/matlab-file-exchange.svg\" alt=\"Abrir en File Exchange\" /></a>",
    "icon": "fa-li fa fa-file-code",
    "sections": [
      "matlab"
    ],
    "order": {
      "matlab": 7
    }
  },
  {
    "id": "friction-and-roughness-matlab-code-to-compute-the-darcy-weisbach-friction-factor",
    "kind": "external",
    "title": "Friction and Roughness : MATLAB code to compute the Darcy-Weisbach friction factor and estimate the relative roughness coefficient of a pipeline.",
    "href": "https://la.mathworks.com/matlabcentral/fileexchange/70165-friction-and-roughness",
    "html": "<a href=\"https://la.mathworks.com/matlabcentral/fileexchange/70165-friction-and-roughness\"><b>Friction and Roughness</b></a>:\n                MATLAB code to compute the Darcy-Weisbach friction factor and estimate the relative roughness coefficient of a pipeline.<br>\n                <a href=\"https://la.mathworks.com/matlabcentral/fileexchange/70165-friction-and-roughness\"><img src=\"https://www.mathworks.com/matlabcentral/images/matlab-file-exchange.svg\" alt=\"Abrir en File Exchange\" /></a>",
    "icon": "fa-li fa fa-file-code",
    "sections": [
      "matlab"
    ],
    "order": {
      "matlab": 8
    }
  },
  {
    "id": "gemelos-digitales-en-robotica-y-automatizacion-2",
    "kind": "external",
    "title": "Gemelos digitales en robótica y automatización",
    "href": "https://medium.com/p/105bee9e7f23",
    "html": "<a href=\"https://medium.com/p/105bee9e7f23\">Gemelos digitales en robótica y automatización</a>",
    "icon": "fa-li fa fa-file-lines",
    "sections": [
      "matlab"
    ],
    "order": {
      "matlab": 10
    }
  }
] as const satisfies readonly CatalogEntry[];
