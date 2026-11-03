"""Ilustraciones deterministas del tutorial de servomotores.

Requiere NumPy y Matplotlib. Ejecutar en la carpeta del artículo.
Las curvas representan señales y consignas teóricas, no ensayos físicos.
"""
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, FancyArrowPatch, Arc
from matplotlib.path import Path as PlotPath

OUT = Path(__file__).resolve().parent
TEAL = "#197b80"
INK = "#243e50"
GRAY = "#657883"
ORANGE = "#c97725"
RED = "#bf3d4e"
plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 11,
    "mathtext.fontset": "stix", "axes.spines.top": False,
    "axes.spines.right": False, "figure.facecolor": "white",
})

def arrow(ax, start, end, color=INK, lw=1.6, style="-|>"):
    ax.add_patch(FancyArrowPatch(start, end, arrowstyle=style,
                                mutation_scale=13, lw=lw, color=color))

def wire(ax, points, color=INK, lw=2):
    p = np.array(points)
    ax.plot(p[:, 0], p[:, 1], color=color, lw=lw, solid_capstyle="round")

def box(ax, x, y, w, h, label, fill="#edf5f5", color=INK, size=11):
    ax.add_patch(Rectangle((x,y), w,h, fc=fill, ec=color, lw=1.5))
    ax.text(x+w/2,y+h/2,label,ha="center",va="center",fontsize=size,color=color)

def canvas(w,h,xmax,ymax):
    fig,ax=plt.subplots(figsize=(w,h))
    ax.set(xlim=(0,xmax),ylim=(0,ymax))
    ax.axis("off")
    return fig,ax

def save(fig,name):
    fig.savefig(OUT/f"{name}.png",dpi=180,bbox_inches="tight",facecolor="white")
    fig.savefig(OUT/f"{name}.svg",bbox_inches="tight",facecolor="white")
    plt.close(fig)

# 1. El lazo interno, separado del microcontrolador que entrega la consigna.
fig,ax=canvas(12,5.2,145,68)
ax.add_patch(Rectangle((19,5),124,55,fc="#fafcfc",ec="#a1b6bd",ls="--",lw=1.3))
ax.text(81,63,"Lazo de posición dentro del servo",ha="center",fontsize=16,color=INK)
ax.text(8,43,"ESP32\npulso $t_p$",ha="center",va="center",color=INK)
arrow(ax,(12,43),(24,43))
box(ax,24,35,23,16,"Decodificador\nconsigna",size=10)
arrow(ax,(47,43),(56,43))
ax.text(51,48,r"$\theta_d$",ha="center",fontsize=15)
ax.add_patch(Circle((59,43),3,fc="white",ec=INK,lw=1.5))
ax.text(57.8,43,"+",ha="center",va="center",fontsize=10)
ax.text(59,41.1,"−",ha="center",va="center",fontsize=10)
arrow(ax,(62,43),(70,43))
ax.text(66,48,r"$e$",ha="center",fontsize=15)
box(ax,70,35,25,16,"Controlador\ny potencia",size=10)
arrow(ax,(95,43),(103,43))
box(ax,103,35,27,16,"Motor y\nengranajes",size=10)
arrow(ax,(130,43),(141,43))
ax.text(138,49,r"$\theta$",ha="center",fontsize=16)
wire(ax,[(135,43),(135,16),(108,16)],TEAL)
arrow(ax,(111,16),(108,16),TEAL)
box(ax,77,9,31,14,"Sensor de posición",fill="#edf5f5",size=10)
wire(ax,[(77,16),(59,16),(59,35)],TEAL)
ax.text(67,20,r"$\theta_m$",ha="center",fontsize=15,color=TEAL)
arrow(ax,(59,34),(59,40),TEAL)
ax.plot(135,43,"o",color=TEAL,ms=4)
ax.text(11,15,"Sin retorno de\nposición por el\ncable de señal",ha="center",va="center",fontsize=9,color=GRAY)
save(fig,"servo-lazo")

# 2. Anchos de pulso: un periodo completo y un detalle del flanco.
fig,axes=plt.subplots(3,2,figsize=(11,6.2),sharex="col",sharey=True,constrained_layout=True)
for row,(ancho,color) in enumerate([(1.,TEAL),(1.5,ORANGE),(2.,RED)]):
    for col,lim in enumerate([20,2.5]):
        ax=axes[row,col]
        t=np.array([0,0,ancho,ancho,lim])
        y=np.array([0,1,1,0,0])
        ax.plot(t,y,color=color,lw=2.2)
        ax.fill_between(t,y,alpha=.08,color=color)
        ax.set(xlim=(-.05,lim+.05),ylim=(-.15,1.5),yticks=[0,1])
        ax.grid(alpha=.16)
        ax.text(lim*.53,1.12,rf"$t_p={ancho:g}\ \mathrm{{ms}}$",fontsize=13,color=color)
        if col==0: ax.set_ylabel("Nivel lógico")
    arrow(axes[row,1],(0,1.27),(ancho,1.27),color,1.2,"<->")
axes[0,0].set_title("Un periodo: $T=20$ ms")
axes[0,1].set_title("Detalle de los primeros 2.5 ms")
for ax in axes[-1]:ax.set_xlabel("Tiempo (ms)")
save(fig,"servo-pulsos")

# 3. Esquema eléctrico. Los símbolos GND representan el mismo nodo.
def ground(ax, x, y):
    wire(ax, [(x,y),(x,y-1.5)], lw=1.5)
    for dy,width in [(1.5,4),(2.5,2.8),(3.5,1.4)]:
        wire(ax, [(x-width/2,y-dy),(x+width/2,y-dy)], lw=1.5)

def supply(ax, x, y):
    wire(ax, [(x,y),(x,y+2)], lw=1.5)
    wire(ax, [(x-1.6,y+2),(x,y+4),(x+1.6,y+2),(x-1.6,y+2)], lw=1.5)
    ax.text(x,y+5,"3V3",ha="center",va="bottom",fontsize=10,color=INK)

def terminal(ax,x,y):
    ax.add_patch(Circle((x,y),.45,fc="white",ec=INK,lw=1.2,zorder=5))

fig,ax=canvas(12.8,10.2,128,102)
ax.set_aspect("equal",adjustable="box")
ax.text(4,98,"a) Servo y alimentación",fontsize=14,color=INK,weight="semibold")
box(ax,5,66,30,22,"ESP32",fill="white",size=13)
ax.text(33,81.8,"GPIO18",ha="right",fontsize=9,color=TEAL)
ax.text(20,68,"GND",ha="center",fontsize=9)
wire(ax,[(20,88),(20,92)],lw=1.5)
ax.text(20,93,"USB",ha="center",fontsize=10)
box(ax,61,69,27,19,"",fill="white")
ax.text(74.5,90,"Servo RC",ha="center",fontsize=12)
ax.text(63,80,"S",ha="left",va="center",fontsize=10)
ax.text(86,84,"V+",ha="right",va="center",fontsize=10)
ax.text(86,73,"GND",ha="right",va="center",fontsize=9)
ax.text(74.5,78,"M",ha="center",va="center",fontsize=13,color=GRAY)
wire(ax,[(35,80),(61,80)],TEAL,1.7)
ax.text(48,83,"0–3.3 V",ha="center",fontsize=10,color=TEAL)
ax.add_patch(Circle((106,79),5,fc="white",ec=INK,lw=1.5))
ax.text(106,81,"+",ha="center",va="center",fontsize=12)
ax.text(106,77,"−",ha="center",va="center",fontsize=12)
ax.text(113,79,"V1\n5 V CC",ha="left",va="center",fontsize=11)
wire(ax,[(106,84),(106,92),(94,92),(94,84),(88,84)],lw=1.5)
wire(ax,[(106,74),(106,58),(20,58),(20,66)],lw=1.5)
wire(ax,[(88,73),(94,73),(94,58)],lw=1.5)
ground(ax,70,58)
for x in [70,94]:ax.plot(x,58,"o",color=INK,ms=3.5)
ax.text(75,53.5,"GND común",va="center",fontsize=10)
for x,y in [(35,80),(20,66),(61,80),(88,84),(88,73)]:terminal(ax,x,y)

ax.text(4,44,"b) Mando con potenciómetro",fontsize=12,color=INK,weight="semibold")
supply(ax,20,31)
wire(ax,[(20,31),(20,24)],lw=1.5)
ax.add_patch(Rectangle((18,12),4,12,fc="white",ec=INK,lw=1.5))
ax.text(14,18,"RV1\n10 kΩ",ha="right",va="center",fontsize=11)
wire(ax,[(20,12),(20,6)],lw=1.5)
ground(ax,20,6)
ax.add_patch(FancyArrowPatch((30,18),(22,18),arrowstyle="-|>",mutation_scale=13,
                            color=INK,lw=1.5,shrinkA=0,shrinkB=0))
wire(ax,[(30,18),(58,18)],lw=1.5)
ax.text(58,20,"GPIO34",ha="right",fontsize=10,color=TEAL)
ax.text(58,24,"ADC1",ha="right",fontsize=10,color=GRAY)
terminal(ax,58,18)
ax.plot(40,18,"o",color=INK,ms=3.5)
wire(ax,[(40,18),(40,11)],lw=1.5)
wire(ax,[(37,11),(43,11)],lw=1.7)
wire(ax,[(37,9),(43,9)],lw=1.7)
wire(ax,[(40,9),(40,6)],lw=1.5)
ground(ax,40,6)
ax.text(45,9,"C1\n100 nF",va="center",fontsize=10)

ax.text(74,44,"c) Pulsador normalmente abierto",fontsize=12,color=INK,weight="semibold")
supply(ax,89,31)
ax.add_patch(Rectangle((87,24),4,7,fc="white",ec=INK,lw=1.5))
ax.text(95,28,"Pull-up interno\nINPUT_PULLUP",ha="left",va="center",fontsize=9,color=GRAY)
wire(ax,[(89,24),(89,20),(119,20)],lw=1.5)
ax.plot(89,20,"o",color=INK,ms=3.5)
terminal(ax,119,20)
ax.text(119,16.5,"GPIO27",ha="right",fontsize=10,color=TEAL)
wire(ax,[(89,20),(89,15)],lw=1.5)
wire(ax,[(89,8),(84,14)],lw=1.5)
terminal(ax,89,15);terminal(ax,89,8)
ax.text(79,11.5,"S1",ha="center",fontsize=11)
wire(ax,[(89,8),(89,6)],lw=1.5)
ground(ax,89,6)
ax.text(103,7,"Pulsado = LOW",ha="left",fontsize=10,color=GRAY)
save(fig,"servo-conexion")

# 4. Momento de las cargas respecto del eje de salida.
fig,ax=canvas(10,4.5,110,55)
ax.set_aspect("equal",adjustable="box")
box(ax,6,13,19,25,"Servo",fill="#e7f4f3",size=12)
ax.add_patch(Circle((25,29),3,fc="white",ec=INK,lw=1.7))
wire(ax,[(25,29),(92,29)],TEAL,7)
ax.add_patch(Rectangle((86,25),12,10,fc="#f8dfc0",ec=ORANGE,lw=1.5))
arrow(ax,(92,25),(92,9),RED,2)
ax.text(98,15,r"$m_c g$",color=RED,fontsize=16)
arrow(ax,(58.5,28),(58.5,13),RED,1.7)
ax.text(62,15,r"$m_b g$",color=RED,fontsize=16)
arrow(ax,(25,44),(92,44),GRAY,1.2,"<->")
ax.text(59,47,r"$L$",ha="center",fontsize=16)
arrow(ax,(25,39),(58.5,39),GRAY,1.2,"<->")
ax.text(42,40,r"$L/2$",ha="center",fontsize=14)
angles=np.linspace(np.deg2rad(25),np.deg2rad(155),80)
arc_points=np.column_stack((25+6.5*np.cos(angles),29+6.5*np.sin(angles)))
ax.add_patch(FancyArrowPatch(path=PlotPath(arc_points),arrowstyle="-|>",
                            mutation_scale=14,color=INK,lw=1.6,zorder=5))
ax.text(14,35,r"$\tau$",fontsize=16)
ax.text(59,2,"Brazo uniforme horizontal · carga en el extremo",ha="center",fontsize=12,color=GRAY)
save(fig,"servo-par")

# 5. Consigna cúbica de una barrera: 1.5 s, 3 s, 1.5 s.
fig=plt.figure(figsize=(12,6.4),constrained_layout=True)
gs=fig.add_gridspec(2,2,width_ratios=[.85,1.4])
ax=fig.add_subplot(gs[:,0])
ax.set(xlim=(-1,6),ylim=(-1,7));ax.set_aspect("equal");ax.axis("off")
box(ax,-.5,0,1,2,"",fill="#edf0f8")
ax.plot([-.9,5.8],[0,0],color=GRAY,lw=1)
base=np.array([0.,2.])
wire(ax,[base,base+np.array([5.,0.])],TEAL,7)
end=base+5*np.array([np.cos(np.deg2rad(80)),np.sin(np.deg2rad(80))])
ax.plot([base[0],end[0]],[base[1],end[1]],ls="--",color=ORANGE,lw=5)
ax.add_patch(Circle(base,.12,fc="white",ec=INK,zorder=4))
ax.add_patch(Arc(base,3,3,theta1=0,theta2=80,color=INK,lw=1.2))
ax.text(1.7,3.1,r"$\Delta\theta=80^\circ$",fontsize=13)
ax.text(2.8,1.5,"Cerrada",ha="center",color=TEAL)
ax.text(1.4,6.4,"Abierta",color=ORANGE)
ax.set_title("Barrera de maqueta\norientaciones nominales",fontsize=13)
t=np.linspace(0,6,601);q=np.empty_like(t);v=np.zeros_like(t)
for k,tk in enumerate(t):
    if tk<=1.5:
        u=tk/1.5;q[k]=20+80*(3*u*u-2*u**3);v[k]=80/1.5*(6*u-6*u*u)
    elif tk<=4.5:q[k]=100
    else:
        u=(tk-4.5)/1.5;q[k]=100-80*(3*u*u-2*u**3);v[k]=-80/1.5*(6*u-6*u*u)
axs=[fig.add_subplot(gs[0,1]),fig.add_subplot(gs[1,1])]
for a,y,color,label in zip(axs,[q,v],[TEAL,ORANGE],
                          [r"$\theta_d$ (grados)",r"$\dot{\theta}_d$ (grados/s)"]):
    a.plot(t,y,color=color,lw=2);a.set_ylabel(label);a.grid(alpha=.18)
    for lim in [1.5,4.5]:a.axvline(lim,color=GRAY,ls=":",lw=1)
    a.set_xlim(0,6)
axs[0].set_title("Consigna calculada, no posición medida",fontsize=13)
axs[0].text(.75,43,"Apertura",ha="center",fontsize=10)
axs[0].text(3,43,"Pausa",ha="center",fontsize=10)
axs[0].text(5.25,43,"Cierre",ha="center",fontsize=10)
axs[1].set_xlabel("Tiempo desde el inicio del ciclo (s)")
save(fig,"servo-trayectoria")
