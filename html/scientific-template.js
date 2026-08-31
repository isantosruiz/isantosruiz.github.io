(function () {
  "use strict";

  var currentScript = document.currentScript;
  var settings = {
    mathEngine: readData("math-engine", "mathjax"),
    codeLanguages: readData("codehl-languages", "python,matlab"),
    tabjaxEndpoint: readData(
      "tabjax-endpoint",
      "https://tabjax.vercel.app/api/render-table"
    ),
    codehlBase: readData("codehl-base", "https://codehl.vercel.app"),
    mathjaxSrc: readData(
      "mathjax-src",
      "https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js"
    ),
    codeTheme: readData("codehl-theme", "github"),
    codeCopyButton: readData("codehl-copy-button", "true")
  };

  function readData(name, fallback) {
    if (!currentScript || !currentScript.dataset) return fallback;
    return currentScript.dataset[toCamel(name)] || fallback;
  }

  function toCamel(value) {
    return value.replace(/-([a-z])/g, function (_, letter) {
      return letter.toUpperCase();
    });
  }

  function onceReady(callback) {
    if (document.readyState === "loading") {
      document.addEventListener("DOMContentLoaded", callback, { once: true });
    } else {
      callback();
    }
  }

  function loadScript(src, attributes) {
    var existing = document.querySelector('script[src="' + src + '"]');
    if (existing) return Promise.resolve(existing);

    return new Promise(function (resolve, reject) {
      var script = document.createElement("script");
      script.src = src;
      script.defer = true;

      Object.keys(attributes || {}).forEach(function (key) {
        script.setAttribute(key, attributes[key]);
      });

      script.addEventListener("load", function () {
        resolve(script);
      });
      script.addEventListener("error", function () {
        reject(new Error("No se pudo cargar " + src));
      });

      document.head.appendChild(script);
    });
  }

  function configureMathJax() {
    if (settings.mathEngine !== "mathjax") return Promise.resolve();

    window.MathJax = window.MathJax || {};
    window.MathJax.tex = Object.assign(
      {
        inlineMath: [
          ["$", "$"],
          ["\\(", "\\)"]
        ],
        displayMath: [
          ["$$", "$$"],
          ["\\[", "\\]"]
        ],
        processEscapes: true,
        tags: "ams"
      },
      window.MathJax.tex || {}
    );
    window.MathJax.options = Object.assign(
      {
        skipHtmlTags: ["script", "noscript", "style", "textarea", "pre", "code"]
      },
      window.MathJax.options || {}
    );

    return loadScript(settings.mathjaxSrc, { id: "scientific-mathjax" }).then(
      function () {
        return window.MathJax.startup && window.MathJax.startup.promise
          ? window.MathJax.startup.promise
          : undefined;
      }
    );
  }

  function typesetMath(root) {
    if (
      settings.mathEngine !== "mathjax" ||
      !window.MathJax ||
      typeof window.MathJax.typesetPromise !== "function"
    ) {
      return Promise.resolve();
    }

    if (typeof window.MathJax.typesetClear === "function") {
      window.MathJax.typesetClear([root || document.body]);
    }

    return window.MathJax.typesetPromise([root || document.body]);
  }

  function loadCodeHighlighters() {
    var languages = settings.codeLanguages
      .split(",")
      .map(function (language) {
        return language.trim().toLowerCase();
      })
      .filter(Boolean);

    return Promise.all(
      languages.map(function (language) {
        return loadScript(settings.codehlBase + "/" + language + ".js", {
          "data-theme": settings.codeTheme,
          "data-default-block-styles": "false",
          "data-transparent-background": "false",
          "data-copy-button": settings.codeCopyButton
        }).catch(function (error) {
          console.warn("[scientific-template] " + error.message);
        });
      })
    );
  }

  function normalizeLatex(source) {
    var lines = String(source || "").replace(/\r\n/g, "\n").split("\n");
    while (lines.length && lines[0].trim() === "") lines.shift();
    while (lines.length && lines[lines.length - 1].trim() === "") lines.pop();
    return lines.join("\n");
  }

  function createStatus(message, className) {
    var status = document.createElement("div");
    status.className = className || "tabjax-meta";
    status.textContent = message;
    return status;
  }

  function renderTabJaxBlock(scriptNode) {
    if (scriptNode.dataset.tabjaxProcessed === "true") {
      return Promise.resolve();
    }

    var latex = normalizeLatex(scriptNode.textContent);
    var wrapper = document.createElement("div");
    var output = document.createElement("div");
    var caption = scriptNode.dataset.caption;

    wrapper.className = "table-block";
    output.className = "tabjax-output";
    output.setAttribute("aria-live", "polite");
    output.appendChild(createStatus("Renderizando tabla..."));

    if (caption) {
      var captionNode = document.createElement("div");
      captionNode.className = "table-caption";
      captionNode.textContent = caption;
      wrapper.appendChild(captionNode);
    }

    wrapper.appendChild(output);
    scriptNode.dataset.tabjaxProcessed = "true";
    scriptNode.parentNode.replaceChild(wrapper, scriptNode);

    return fetch(settings.tabjaxEndpoint, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        latex: latex,
        options: {
          addClasses: true,
          mathMode: scriptNode.dataset.mathMode || "preserve",
          headerMode: scriptNode.dataset.headerMode || "auto"
        }
      })
    })
      .then(function (response) {
        return response.json().then(function (payload) {
          if (!response.ok || !payload.ok) {
            throw new Error(
              payload && payload.error && payload.error.message
                ? payload.error.message
                : "No se pudo renderizar la tabla."
            );
          }
          return payload;
        });
      })
      .then(function (payload) {
        output.innerHTML = payload.html;

        if (payload.meta) {
          output.parentNode.appendChild(
            createStatus(
              "Tabla generada: " +
                payload.meta.rows +
                " filas, " +
                payload.meta.columns +
                " columnas."
            )
          );
        }

        if (payload.warnings && payload.warnings.length) {
          payload.warnings.forEach(function (warning) {
            output.parentNode.appendChild(
              createStatus(warning.message, "tabjax-warning")
            );
          });
        }

        return typesetMath(output);
      })
      .catch(function (error) {
        output.innerHTML = "";
        output.appendChild(
          createStatus(
            "TabJax no pudo generar esta tabla: " + error.message,
            "tabjax-warning"
          )
        );
      });
  }

  function renderTabJaxTables() {
    var tables = document.querySelectorAll('script[type="text/tabjax"]');
    return Promise.all(
      Array.prototype.map.call(tables, function (scriptNode) {
        return renderTabJaxBlock(scriptNode);
      })
    );
  }

  onceReady(function () {
    configureMathJax()
      .then(function () {
        return Promise.all([renderTabJaxTables(), loadCodeHighlighters()]);
      })
      .then(function () {
        return typesetMath(document.body);
      })
      .catch(function (error) {
        console.warn("[scientific-template] " + error.message);
      });
  });
})();
