"""Geometría del PCA y vigilancia de cambios con datos sintéticos.

Ejecutar sin argumentos muestra las figuras. La opción --guardar CARPETA
exporta las ilustraciones del artículo sin abrir ventanas.
"""

# %% datos
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA

# RandomState conserva la secuencia de np.random.seed(42) del ejemplo inicial.
rng = np.random.RandomState(42)
n = 500
escalas = np.array([5.0, 3.0, 0.81])
U = np.column_stack([
    rng.normal(0.0, escala, n) for escala in escalas
])
R, _ = np.linalg.qr(rng.randn(3, 3))
mu_generadora = np.array([2.0, -1.0, 4.0])
X = U @ R.T + mu_generadora

# %% ajuste
pca = PCA(n_components=3, svd_solver="full", whiten=False)
scores = pca.fit_transform(X)
media = pca.mean_
V = pca.components_.T
lambdas = pca.explained_variance_
proporciones = pca.explained_variance_ratio_
Xc = X - media
S = Xc.T @ Xc / (n - 1)

# %% proyecciones
r = 2
Vr = V[:, :r]
P = Vr @ Vr.T
P_perp = np.eye(X.shape[1]) - P
Z = Xc @ Vr
X_proy = media + Z @ Vr.T
E = X - X_proy
residuo_firmado = Xc @ V[:, 2]
error_medio = np.mean(np.sum(E**2, axis=1))

# %% verificacion
valores, vectores = np.linalg.eigh(S)
orden = np.argsort(valores)[::-1]
valores = valores[orden]
vectores = vectores[:, orden]

np.testing.assert_allclose(valores, lambdas, rtol=1e-12)
np.testing.assert_allclose(S @ V, V * lambdas, atol=1e-12)
np.testing.assert_allclose(V.T @ V, np.eye(3), atol=1e-12)
np.testing.assert_allclose(P @ P, P, atol=1e-12)
np.testing.assert_allclose(P @ P_perp, 0.0, atol=1e-12)
np.testing.assert_allclose(E @ Vr, 0.0, atol=1e-12)
np.testing.assert_allclose(X, X_proy + E, atol=1e-12)
np.testing.assert_allclose(
    Z.T @ Z / (n - 1), np.diag(lambdas[:r]), atol=1e-12
)
np.testing.assert_allclose(
    error_medio, (n - 1) / n * lambdas[r:].sum(), atol=1e-12
)

# %% estadisticos
def evaluar(Y):
    """Usa siempre la media y las direcciones del ajuste de referencia."""
    Yc = np.asarray(Y) - media
    z = Yc @ Vr
    e = Yc - z @ Vr.T
    t2 = np.sum(z**2 / lambdas[:r], axis=1)
    spe = np.sum(e**2, axis=1)
    return z, e, t2, spe


# %% calibracion
def nuevas_muestras(cantidad):
    latentes = np.column_stack([
        rng.normal(0.0, escala, cantidad) for escala in escalas
    ])
    return latentes @ R.T + mu_generadora


# Datos sanos distintos de los usados para ajustar PCA.
X_cal = nuevas_muestras(2000)
_, _, t2_cal, q_cal = evaluar(X_cal)
alpha = 0.01
limite_t2 = np.quantile(t2_cal, 1 - alpha, method="higher")
limite_q = np.quantile(q_cal, 1 - alpha, method="higher")

# %% cambios
# Tres tramos independientes de 200 muestras; no es un modelo dinámico.
X_base = nuevas_muestras(600)
X_test = X_base.copy()
cambio_residual = 4 * np.sqrt(lambdas[2]) * V[:, 2]
cambio_principal = 4 * np.sqrt(lambdas[0]) * V[:, 0]
X_test[200:400] += cambio_residual
X_test[400:600] += cambio_principal

Z_test, E_test, t2_test, q_test = evaluar(X_test)
alarma_t2 = t2_test > limite_t2
alarma_q = q_test > limite_q
alarma = alarma_t2 | alarma_q
tramos = [slice(0, 200), slice(200, 400), slice(400, 600)]
tasas = np.array([
    [alarma_t2[s].mean(), alarma_q[s].mean(), alarma[s].mean()]
    for s in tramos
])

# Comprobación geométrica: los cambios elegidos no invaden el otro subespacio.
Z_base, E_base, _, _ = evaluar(X_base)
np.testing.assert_allclose(Z_test[200:400], Z_base[200:400], atol=1e-12)
np.testing.assert_allclose(E_test[400:], E_base[400:], atol=1e-12)

# %% graficas
COLORES = dict(datos="#2878ad", plano="#89b8bd", proy="#c66a21",
               v1="#a93455", v2="#20816b", v3="#6756a0")


def figuras_geometricas():
    """Las cuatro etapas del ejemplo con escalas espaciales iguales."""
    figuras = {}
    extremos = np.vstack([X, X_proy, media + 2*np.sqrt(lambdas)[:, None]*V.T])
    radio = 1.07 * np.max(np.abs(extremos - media))
    s1 = np.linspace(scores[:, 0].min(), scores[:, 0].max(), 12)
    s2 = np.linspace(scores[:, 1].min(), scores[:, 1].max(), 12)
    A, B = np.meshgrid(s1, s2)
    plano = media + A[..., None]*V[:, 0] + B[..., None]*V[:, 1]

    def ejes3d(titulo):
        fig = plt.figure(figsize=(8.2, 7.2))
        ax = fig.add_subplot(projection="3d")
        for j, setter in enumerate([ax.set_xlim, ax.set_ylim, ax.set_zlim]):
            setter(media[j]-radio, media[j]+radio)
        ax.set_box_aspect([1, 1, 1])
        ax.view_init(elev=24, azim=-50)
        ax.set(xlabel=r"$x_1$", ylabel=r"$x_2$", zlabel=r"$x_3$")
        ax.set_title(titulo, pad=18)
        ax.tick_params(labelsize=9)
        for eje in [ax.xaxis, ax.yaxis, ax.zaxis]:
            eje.pane.fill = False
            eje._axinfo["grid"]["color"] = (0.7, 0.75, 0.77, 0.3)
        fig.subplots_adjust(left=0.02, right=0.86, bottom=0.04, top=0.91)
        return fig, ax

    def superficie(ax):
        ax.plot_surface(plano[..., 0], plano[..., 1], plano[..., 2],
                        alpha=0.18, color=COLORES["plano"], shade=False)

    def direcciones(ax):
        for j in range(3):
            flecha = 2*np.sqrt(lambdas[j])*V[:, j]
            ax.quiver(*media, *flecha, color=COLORES[f"v{j+1}"],
                      linewidth=1.8, arrow_length_ratio=0.12,
                      label=rf"$2\sqrt{{\lambda_{j+1}}}\,\mathbf{{v}}_{j+1}$")
        ax.scatter(*media, color="#222222", s=28, label=r"Media $\boldsymbol{\mu}$")

    fig, ax = ejes3d("Tres variables, una nube casi plana")
    ax.scatter(*X.T, color=COLORES["datos"], s=10, alpha=0.55,
               edgecolors="none", depthshade=False)
    figuras["pca-nube"] = fig

    fig, ax = ejes3d("Direcciones propias y plano principal")
    superficie(ax)
    ax.scatter(*X.T, color=COLORES["datos"], s=8, alpha=0.3,
               edgecolors="none", depthshade=False)
    direcciones(ax)
    ax.legend(loc="upper left", frameon=False, fontsize=10)
    figuras["pca-plano"] = fig

    fig, ax = ejes3d("Proyección y segmentos residuales")
    superficie(ax)
    ax.scatter(*X.T, color=COLORES["datos"], s=9, alpha=0.25,
               edgecolors="none", depthshade=False, label="Datos originales")
    ax.scatter(*X_proy.T, color=COLORES["proy"], s=9, alpha=0.6,
               edgecolors="none", depthshade=False, label="Reconstrucción")
    for k in range(0, n, 10):
        segmento = np.vstack([X[k], X_proy[k]])
        ax.plot(*segmento.T, color=COLORES["v3"], linewidth=0.8, alpha=0.8,
                label="Residuo (una de cada 10 muestras)" if k == 0 else None)
    ax.legend(loc="upper left", frameon=False, fontsize=9)
    figuras["pca-proyeccion"] = fig

    fig, ax = plt.subplots(figsize=(8, 6), constrained_layout=True)
    ax.scatter(*Z.T, color=COLORES["proy"], s=13, alpha=0.6, edgecolors="none")
    for j in range(2):
        delta = np.zeros(2)
        delta[j] = 2*np.sqrt(lambdas[j])
        ax.annotate("", xy=delta, xytext=(0, 0),
                    arrowprops=dict(arrowstyle="->", color=COLORES[f"v{j+1}"], lw=2))
        ax.annotate(rf"$2\sqrt{{\lambda_{j+1}}}\,\mathbf{{e}}_{j+1}$",
                    xy=delta, xytext=(7, 6), textcoords="offset points",
                    color=COLORES[f"v{j+1}"])
    ax.axhline(0, color="#879298", lw=0.7)
    ax.axvline(0, color="#879298", lw=0.7)
    ax.set_aspect("equal", adjustable="box")
    ax.set(xlabel=f"Puntuación $z_1$ ({100*proporciones[0]:.2f} %)",
           ylabel=f"Puntuación $z_2$ ({100*proporciones[1]:.2f} %)",
           title=f"Coordenadas principales: {100*proporciones[:2].sum():.2f} % de varianza")
    ax.grid(alpha=0.18)
    figuras["pca-coordenadas"] = fig
    return figuras


def figuras_monitorizacion():
    from matplotlib.patches import Ellipse

    figuras = {}
    nombres = ["Referencia sana", "Cambio residual", "Cambio principal"]
    colores = ["#68777e", "#b73755", "#127c7c"]
    k = np.arange(1, 601)

    def marcar_tramos(ax):
        for limite in [200.5, 400.5]:
            ax.axvline(limite, color="#8c959a", linestyle=":", lw=1)
        ax.set_xlim(1, 600)
        ax.grid(axis="y", alpha=0.2)

    fig, axes = plt.subplots(3, 1, figsize=(10, 7.5), sharex=True,
                             constrained_layout=True)
    for j, ax in enumerate(axes):
        for s, nombre, color in zip(tramos, nombres, colores):
            ax.plot(k[s], X_test[s, j], color=color, lw=0.8, alpha=0.85, label=nombre)
        ax.set_ylabel(rf"$x_{j+1}$")
        marcar_tramos(ax)
    axes[0].legend(loc="upper center", ncol=3, frameon=False, fontsize=10)
    axes[0].set_title("Mediciones originales: cambios sobre la misma variabilidad de fondo", pad=26)
    axes[-1].set_xlabel("Número de muestra (no representa una escala de tiempo)")
    figuras["pca-senales"] = fig

    fig, axes = plt.subplots(2, 1, figsize=(10, 6.8), sharex=True,
                             constrained_layout=True)
    for ax, estadistico, limite, etiqueta in zip(
            axes, [t2_test, q_test], [limite_t2, limite_q],
            [r"$T^2$", r"$Q_{\mathrm{SPE}}$"]):
        for s, nombre, color in zip(tramos, nombres, colores):
            ax.plot(k[s], estadistico[s], color=color, lw=0.9, label=nombre)
        ax.axhline(limite, color="#222222", ls="--", lw=1.3,
                   label=f"Umbral empírico: {limite:.2f}")
        ax.set_ylabel(etiqueta)
        marcar_tramos(ax)
        ax.legend(loc="upper left", ncol=2, frameon=False, fontsize=9)
    axes[0].set_title("Dos indicadores para dos tipos de desviación")
    axes[-1].set_xlabel("Número de muestra")
    figuras["pca-monitoreo"] = fig

    fig, axes = plt.subplots(1, 2, figsize=(11, 5.0), constrained_layout=True)
    for s, nombre, color in zip(tramos, nombres, colores):
        axes[0].scatter(*Z_test[s].T, s=12, alpha=0.55, color=color,
                        edgecolors="none", label=nombre)
        e3 = E_test[s] @ V[:, 2]
        axes[1].scatter(Z_test[s, 0], e3, s=12, alpha=0.55, color=color,
                        edgecolors="none")
    axes[0].add_patch(Ellipse((0, 0), 2*np.sqrt(limite_t2*lambdas[0]),
                              2*np.sqrt(limite_t2*lambdas[1]),
                              fill=False, ls="--", lw=1.3, color="#222222"))
    axes[0].set(xlabel=r"$z_1$", ylabel=r"$z_2$", title="Vista dentro del plano principal")
    for signo in [-1, 1]:
        axes[1].axhline(signo*np.sqrt(limite_q), color="#222222", ls="--", lw=1.3)
    axes[1].set(xlabel=r"$z_1$", ylabel=r"$z_3$",
                title="Vista que recupera la dirección residual")
    for ax in axes:
        ax.grid(alpha=0.17)
    fig.legend(*axes[0].get_legend_handles_labels(), loc="outside lower center",
               ncol=3, fontsize=10, frameon=False)
    figuras["pca-dos-espacios"] = fig
    return figuras


def resumen():
    return {
        "media": media.tolist(), "eigenvalores": lambdas.tolist(),
        "eigenvectores_columnas": V.tolist(), "covarianza": S.tolist(),
        "porcentajes": (100*proporciones).tolist(),
        "error_cuadratico_medio": float(error_medio),
        "umbral_t2": float(limite_t2), "umbral_q": float(limite_q),
        "tasas_por_tramo": tasas.tolist(),
        "cambio_residual": cambio_residual.tolist(),
        "cambio_principal": cambio_principal.tolist(),
    }


if __name__ == "__main__":
    import argparse
    import json
    from pathlib import Path

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--guardar", type=Path, help="Carpeta para las figuras PNG")
    args = parser.parse_args()
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 11,
                         "mathtext.fontset": "stix", "axes.spines.top": False,
                         "axes.spines.right": False, "figure.facecolor": "white"})
    figuras = {**figuras_geometricas(), **figuras_monitorizacion()}
    print(json.dumps(resumen(), ensure_ascii=False, indent=2))
    if args.guardar:
        args.guardar.mkdir(parents=True, exist_ok=True)
        for nombre, fig in figuras.items():
            fig.savefig(args.guardar / f"{nombre}.png", dpi=180,
                        bbox_inches=None if nombre in {"pca-nube", "pca-plano", "pca-proyeccion"} else "tight",
                        facecolor="white")
        plt.close("all")
    else:
        plt.show()
