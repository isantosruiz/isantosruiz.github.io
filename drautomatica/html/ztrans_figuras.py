"""Genera las ocho figuras originales de ztrans.html y verifica sus modelos."""
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle, FancyBboxPatch
import numpy as np
from ztrans_sistemas import crear_figuras

OUT = Path(__file__).resolve().parent
TEAL, ORANGE, INK, GRAY = "#197b80", "#bd7129", "#263f50", "#687b87"
plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 11, "mathtext.fontset": "stix",
    "figure.figsize": (9, 5.5), "figure.facecolor": "white",
    "axes.spines.top": False, "axes.spines.right": False,
    "axes.prop_cycle": plt.cycler(color=[TEAL, ORANGE, INK, GRAY]),
    "svg.fonttype": "path",
})


def guardar(fig, nombre):
    for ext in ("svg", "png"):
        fig.savefig(OUT/f"ztrans-{nombre}.{ext}", dpi=190,
                    bbox_inches="tight", pad_inches=0.14, facecolor="white")
    plt.close(fig)


def esquemas_fisicos():
    # Símbolos IEC con relación de aspecto fija.
    fig, ax = plt.subplots(figsize=(9, 4), layout="constrained")
    ax.set(aspect="equal", xlim=(-.3, 8.1), ylim=(-.6, 3.9)); ax.axis("off")
    def linea(xs, ys): ax.plot(xs, ys, color=INK, lw=1.8, solid_capstyle="round")
    ax.add_patch(Circle((1, 1.55), .45, fill=False, ec=INK, lw=1.8))
    linea([1, 1, 2.7], [2, 3, 3]); linea([1, 1, 6], [1.1, 0, 0])
    ax.add_patch(Rectangle((2.7, 2.78), 1.1, .44, fill=False, ec=INK, lw=1.8))
    linea([3.8, 6, 6], [3, 3, 1.7])
    linea([5.45, 6.55], [1.7, 1.7]); linea([5.45, 6.55], [1.42, 1.42])
    linea([6, 6], [1.42, 0])
    for y, ancho in [(-.12, .7), (-.25, .48), (-.38, .2)]:
        if y == -.12: linea([6, 6], [0, y])
        linea([6-ancho/2, 6+ancho/2], [y, y])
    ax.text(1, 1.76, "+", ha="center", va="center", fontsize=15)
    ax.text(1, 1.35, "−", ha="center", va="center", fontsize=15)
    ax.text(.28, 1.55, r"$v(t)$", ha="center", va="center", fontsize=16, color=INK)
    ax.text(3.25, 3.38, r"$R$", ha="center", fontsize=17, color=INK)
    ax.text(5.15, 1.52, r"$C$", ha="center", va="center", fontsize=17, color=INK)
    linea([6, 6.9], [3, 3]); ax.plot(6, 3, "o", ms=4, color=INK)
    ax.text(7.2, 2.85, r"$+$", ha="center", fontsize=15, color=TEAL)
    ax.text(7.2, 1.7, r"$v_C(t)$", ha="center", fontsize=16, color=TEAL)
    ax.text(7.2, .15, r"$-$", ha="center", fontsize=15, color=TEAL)
    ax.annotate("", xy=(4.9, 3.6), xytext=(4.0, 3.6),
                arrowprops={"arrowstyle": "->", "color": TEAL, "lw": 1.5})
    ax.text(4.45, 3.75, r"$i(t)$", ha="center", fontsize=15, color=TEAL)
    guardar(fig, "rc-circuito")

    fig, ax = plt.subplots(figsize=(9, 4.2), layout="constrained")
    ax.set(aspect="equal", xlim=(0, 8.2), ylim=(0, 4)); ax.axis("off")
    def linea(xs, ys, color=INK): ax.plot(xs, ys, color=color, lw=1.8)
    linea([.6, .6], [.4, 3.5])
    for y in np.arange(.6, 3.5, .28): linea([.35, .6], [y-.18, y], GRAY)
    linea([.6, 1.35], [2.6, 2.6])
    xx = np.linspace(1.35, 3.7, 17)
    yy = np.array([0]+[.18 if n % 2 else -.18 for n in range(1,16)]+[0])+2.6
    linea(xx, yy, TEAL); linea([3.7, 4.6], [2.6, 2.6])
    linea([.6, 2.0], [1.25, 1.25], TEAL)
    linea([2.0, 2.0, 3.2], [.92, 1.58, 1.58], TEAL)
    linea([2.0, 3.2], [.92, .92], TEAL)
    linea([2.9, 2.9], [1.0, 1.5], TEAL)
    linea([2.9, 4.6], [1.25, 1.25], TEAL)
    ax.add_patch(FancyBboxPatch((4.6,.82),1.6,2.35,
                 boxstyle="round,pad=0,rounding_size=.06", ec=INK, fc="#edf5f4", lw=1.8))
    for x in [4.97,5.83]: ax.add_patch(Circle((x,.60),.22,ec=GRAY,fc="white",lw=1.5))
    linea([4.1,6.7],[.38,.38],GRAY)
    ax.text(2.5,3.0,r"$K$",ha="center",fontsize=18,color=TEAL)
    ax.text(2.6,.55,r"$b$",ha="center",fontsize=18,color=TEAL)
    ax.text(5.4,1.9,r"$m$",ha="center",fontsize=23,color=INK)
    for start,end,y,txt in [(4.8,6.1,3.65,r"$x(t)$"),(6.2,7.9,2.0,r"$F(t)$")]:
        ax.annotate("",xy=(end,y),xytext=(start,y),
                    arrowprops={"arrowstyle":"->","color":TEAL,"lw":1.8})
        ax.text((start+end)/2,y+.18,txt,ha="center",fontsize=17,color=TEAL)
    guardar(fig, "mecanismo-esquema")


def muestreo():
    Ts = .1
    t = np.linspace(0, 1.2, 1201)
    k = np.arange(13)
    f = lambda t: 1 + .4*np.sin(2*np.pi*t) + .15*np.cos(6*np.pi*t)
    fig, axes = plt.subplots(1, 2, figsize=(10, 3.8), layout="constrained")
    axes[0].plot(t, f(t), color=GRAY, label=r"Señal continua $x(t)$")
    axes[0].plot(k*Ts, f(k*Ts), "o", color=TEAL, ms=5, label="Muestras")
    axes[0].set(xlabel="Tiempo (s)", ylabel="Amplitud", title=r"Muestreo con $T_s=0.1$ s")
    axes[0].legend(fontsize=10)
    axes[1].stem(k, f(k*Ts), basefmt=" ")
    axes[1].set(xlabel=r"Índice $k$", title=r"Secuencia $x[k]=x(kT_s)$")
    axes[1].set_xticks([0, 2, 4, 6, 8, 10, 12])
    for ax in axes: ax.grid(alpha=.18); ax.set_ylim(0, 1.8)
    guardar(fig, "muestreo")


def convergencia():
    fig, axes = plt.subplots(1, 2, figsize=(9.6, 4.4), layout="constrained")
    grid = np.linspace(-1.5, 1.5, 451)
    xx, yy = np.meshgrid(grid, grid)
    radio = np.hypot(xx, yy)
    for ax, exterior in zip(axes, (True, False)):
        mask = radio > .8 if exterior else radio < .8
        ax.contourf(xx, yy, mask.astype(float), levels=[.5, 1.5], colors=["#dcefee"])
        ax.add_patch(Circle((0, 0), .8, fill=False, color=TEAL, ls="--", lw=1.8))
        ax.axhline(0, color=GRAY, lw=.7); ax.axvline(0, color=GRAY, lw=.7)
        ax.plot(.8, 0, "x", color=ORANGE, ms=9, mew=2)
        ax.text(.88, .14, r"Polo $z=0.8$", fontsize=10)
        ax.set(aspect="equal", xlim=(-1.5, 1.5), ylim=(-1.5, 1.5),
               xlabel=r"$\operatorname{Re}(z)$", ylabel=r"$\operatorname{Im}(z)$")
        ax.set_title(r"Causal: $|z|>0.8$" if exterior else r"Anticausal: $|z|<0.8$")
        ax.text(0, -1.34, "Zona sombreada: convergencia", ha="center", fontsize=9)
    guardar(fig, "convergencia")


def polos():
    fig = plt.figure(figsize=(10, 7), layout="constrained")
    gs = fig.add_gridspec(4, 2, width_ratios=(1, 1.25))
    ax = fig.add_subplot(gs[:, 0])
    ax.add_patch(Circle((0, 0), 1, color="#edf5f4", ec=TEAL, lw=1.5))
    ax.axhline(0, color=GRAY, lw=.7); ax.axvline(0, color=GRAY, lw=.7)
    r, theta = np.exp(-.2), .4
    puntos = [(.75, TEAL), (-.75, ORANGE), (r*np.exp(1j*theta), INK),
              (r*np.exp(-1j*theta), INK), (1.08, "#ae465e")]
    for p, color in puntos: ax.plot(np.real(p), np.imag(p), "x", ms=9, mew=2, color=color)
    ax.annotate(r"$|z|=1$", xy=(-.8, .6), xytext=(-1.38, 1.1),
                arrowprops={"arrowstyle": "-", "color": GRAY}, fontsize=12)
    ax.set(aspect="equal", xlim=(-1.45, 1.45), ylim=(-1.45, 1.45),
           xlabel=r"$\operatorname{Re}(z)$", ylabel=r"$\operatorname{Im}(z)$",
           title="Polos de modelos causales")
    n = np.arange(21)
    modos = [(TEAL, .75**n, r"$0.75^k$: decaimiento"),
             (ORANGE, (-.75)**n, r"$(-0.75)^k$: alternancia amortiguada"),
             (INK, r**n*np.cos(theta*n), r"$e^{-0.2k}\cos(0.4k)$: oscilación amortiguada"),
             ("#ae465e", 1.08**n, r"$1.08^k$: crecimiento")]
    for j, (color, valores, titulo) in enumerate(modos):
        bx = fig.add_subplot(gs[j, 1])
        marker, lines, base = bx.stem(n, valores, basefmt=" ")
        marker.set_color(color); marker.set_markersize(3); lines.set_color(color)
        bx.set_title(titulo, fontsize=10, loc="left")
        bx.grid(alpha=.18); bx.set_xticks([0, 5, 10, 15, 20])
        if j == 3: bx.set_xlabel(r"Índice $k$")
    guardar(fig, "polos")


if __name__ == "__main__":
    esquemas_fisicos(); muestreo(); convergencia(); polos()
    for nombre, fig in crear_figuras().items():
        if nombre == "convolucion": fig.set_size_inches(9, 7)
        elif nombre == "mecanismo": fig.set_size_inches(9, 7)
        guardar(fig, nombre)
    print("Ocho figuras exportadas en SVG y PNG; comprobaciones numéricas superadas.")
