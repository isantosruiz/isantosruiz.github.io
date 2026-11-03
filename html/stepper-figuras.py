"""Figuras del tutorial stepper.html: esquemas y perfiles teóricos.
Requiere NumPy y Matplotlib. No contiene datos medidos de un motor.
"""
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, FancyArrowPatch, Polygon

OUT = Path(__file__).resolve().parent
INK, TEAL, ORANGE, GRAY = "#263f50", "#197b80", "#bd7129", "#687b87"
plt.rcParams.update({"font.family":"DejaVu Sans", "font.size":11,
                     "mathtext.fontset":"stix", "axes.spines.top":False,
                     "axes.spines.right":False, "figure.facecolor":"white"})

def line(ax,points,color=INK,lw=1.6,**kw):
    p=np.array(points);ax.plot(p[:,0],p[:,1],color=color,lw=lw,**kw)
def arrow(ax,a,b,color=INK,style="-|>",lw=1.5):
    ax.add_patch(FancyArrowPatch(a,b,arrowstyle=style,mutation_scale=12,
                 lw=lw,color=color,shrinkA=0,shrinkB=0))
def ground(ax,x,y,label=""):
    line(ax,[(x,y),(x,y-1.4)])
    for dy,w in [(1.4,4),(2.4,2.6),(3.4,1.3)]:
        line(ax,[(x-w/2,y-dy),(x+w/2,y-dy)])
    if label:ax.text(x,y-5,label,ha="center",va="top",fontsize=9,color=GRAY)
def dot(ax,x,y):ax.plot(x,y,"o",ms=3.5,color=INK)
def pin(ax,x,y):
    ax.add_patch(Circle((x,y),.4,fc="white",ec=INK,lw=1.2,zorder=4))
def box(ax,x,y,w,h,fill="white",**kw):
    ax.add_patch(Rectangle((x,y),w,h,fc=fill,ec=INK,lw=1.4,**kw))
def canvas(w,h,xmax,ymax):
    fig,ax=plt.subplots(figsize=(w,h));ax.set(xlim=(0,xmax),ylim=(0,ymax))
    ax.set_aspect("equal");ax.axis("off");return fig,ax
def save(fig,name):
    fig.savefig(OUT/f"{name}.png",dpi=190,bbox_inches="tight",facecolor="white")
    fig.savefig(OUT/f"{name}.svg",bbox_inches="tight",facecolor="white")
    plt.close(fig)

# 1. Referencias de corriente, no dibujo del dentado de un motor.
fig,axs=plt.subplots(1,2,figsize=(11.6,4.5),constrained_layout=True)
phi=np.linspace(0,np.pi/2,200);m=np.linspace(0,np.pi/2,9)
axs[0].plot(np.rad2deg(phi),np.cos(phi),color=TEAL,label=r"$i_A/I_{\rm pk}$")
axs[0].plot(np.rad2deg(phi),np.sin(phi),color=ORANGE,label=r"$i_B/I_{\rm pk}$")
axs[0].scatter(np.rad2deg(m),np.cos(m),color=TEAL,s=22)
axs[0].scatter(np.rad2deg(m),np.sin(m),color=ORANGE,s=22)
axs[0].set(xlabel=r"Ángulo eléctrico $\varphi$ (grados)",ylabel="Corriente normalizada",
           xlim=(0,90),ylim=(-.05,1.08),xticks=[0,22.5,45,67.5,90])
axs[0].grid(alpha=.18);axs[0].legend(frameon=False)
axs[0].set_title("Reparto de corriente entre las fases")
ax=axs[1];ax.set_aspect("equal")
ax.plot(np.cos(phi),np.sin(phi),color="#b3c7ca",ls="--")
for k in range(9):
    arrow(ax,(0,0),(np.cos(m[k]),np.sin(m[k])),TEAL if k==4 else "#a4b9bd",
          lw=2 if k==4 else 1)
ax.set(xlim=(-.05,1.15),ylim=(-.05,1.15),xlabel=r"$i_A/I_{\rm pk}$",
       ylabel=r"$i_B/I_{\rm pk}$",xticks=[0,.5,1],yticks=[0,.5,1])
ax.grid(alpha=.18);ax.set_title("Ocho incrementos en un cuadrante")
save(fig,"stepper-corrientes")

# 2. Etapa de potencia. Cuatro terminales, dos devanados independientes.
fig,ax=canvas(13,8.1,130,81)
box(ax,40,14,38,44,fill="#f7fafb")
ax.text(59,50,"Módulo\nTB6600",ha="center",fontsize=13)
box(ax,40,68,38,11)
ax.text(59,74,"Fuente 24 V CC",ha="center",va="center",fontsize=11)
for x,label in [(51,"+"),(68,"−")]:
    line(ax,[(x,68),(x,58)]);pin(ax,x,58)
    ax.text(x+2,63,label,fontsize=13)
ax.text(51,55,"V+",ha="center",fontsize=9)
ax.text(68,55,"V−",ha="center",fontsize=9)
for y,label,net in [(44,"PUL+","+5V_CTRL"),(38,"PUL−","Colector Q1"),
                    (30,"DIR+","+5V_CTRL"),(24,"DIR−","Colector Q2")]:
    line(ax,[(9,y),(40,y)],TEAL);pin(ax,40,y)
    ax.text(9,y+2,net,fontsize=10,color=TEAL)
    ax.text(42,y,label,va="center",fontsize=10)
for y,label in [(19,"ENA+"),(15,"ENA−")]:
    line(ax,[(35,y),(40,y)]);ax.plot(35,y,marker="x",color=GRAY,ms=6)
    ax.text(42,y,label,va="center",fontsize=9)
ax.text(8,16,"ENA sin conectar\nen el módulo de referencia",fontsize=9,color=GRAY)
box(ax,103,14,24,44,fill="#faf9f6")
ax.text(115,62,"NEMA 17",ha="center",fontsize=13)
for top,bottom,name,color in [(44,35,"A",TEAL),(28,19,"B",ORANGE)]:
    for y,suffix in [(top,"+"),(bottom,"−")]:
        line(ax,[(78,y),(111,y)],color);pin(ax,78,y)
        ax.text(76,y,name+suffix,ha="right",va="center",fontsize=10)
    u=np.linspace(0,1,160)
    ax.plot(111+2*np.abs(np.sin(4*np.pi*u)),top-(top-bottom)*u,color=color,lw=1.8)
    ax.text(119,(top+bottom)/2,"Fase "+name,rotation=90,ha="center",va="center",fontsize=10)
ax.text(65,6,"Las entradas optoacopladas y la alimentación de potencia son circuitos distintos.",
        ha="center",fontsize=10,color=GRAY)
save(fig,"stepper-potencia")

# 3. Dos canales NPN con resistencia de base y de descarga.
fig,axes=plt.subplots(1,2,figsize=(12.4,6.5))
for ax,(gpio,pref,num) in zip(axes,[(18,"PUL",1),(19,"DIR",2)]):
    ax.set(xlim=(0,64),ylim=(-3,64));ax.set_aspect("equal");ax.axis("off")
    ax.text(31,61,f"Canal {pref}",ha="center",fontsize=15,color=INK,weight="semibold")
    # Input and base resistor
    line(ax,[(3,18),(12,18)]);pin(ax,3,18)
    ax.text(3,21,f"GPIO{gpio}",fontsize=10,color=TEAL)
    box(ax,12,16,8,4);line(ax,[(20,18),(34,18)])
    ax.text(16,23,"1 kΩ",ha="center",fontsize=10)
    dot(ax,25,18);line(ax,[(25,18),(25,12)])
    box(ax,23,6,4,6);line(ax,[(25,6),(25,3)]);ground(ax,25,3)
    ax.text(20,9,"10 kΩ",ha="right",va="center",fontsize=9)
    # NPN base, collector, emitter with outgoing arrow
    line(ax,[(34,13),(34,23)],lw=2)
    line(ax,[(34,21),(42,27),(42,34)])
    line(ax,[(34,15),(42,9),(42,3)])
    arrow(ax,(37,12.75),(41,9.75))
    ax.text(46,20,f"Q{num}\nBC337",fontsize=10)
    ground(ax,42,3)
    ax.text(34,-2,"GND_CTRL",ha="center",va="top",fontsize=9,color=GRAY)
    # Internal resistor and LED, bounded as the module input
    box(ax,34,34,17,19,fill="#f5f8f8",linestyle="--")
    line(ax,[(42,53),(42,50)])
    box(ax,40.5,45,3,5);line(ax,[(42,45),(42,43)])
    ax.add_patch(Polygon([[40,43],[44,43],[42,39.5]],closed=True,fill=False,ec=INK,lw=1.4))
    line(ax,[(40,39.5),(44,39.5)])
    line(ax,[(42,39.5),(42,34)])
    arrow(ax,(45,42),(48,45),GRAY,lw=1)
    arrow(ax,(45,39.5),(48,42.5),GRAY,lw=1)
    ax.text(32,47,r"$R_{\rm int}$",ha="right",fontsize=10)
    for y,label in [(53,pref+"+"),(34,pref+"−")]:
        pin(ax,42,y);ax.text(53,y,label,va="center",fontsize=10)
    line(ax,[(42,53),(42,56)])
    ax.text(42,57,"+5V_CTRL",ha="center",fontsize=10,color=TEAL)
fig.subplots_adjust(wspace=.15)
save(fig,"stepper-interfaz")

# 4. Timing specified in PasoDir.h. HIGH drives the NPN and LED current.
fig,axes=plt.subplots(3,1,figsize=(10,5.7),sharex=True,constrained_layout=True)
t=np.array([-20,0,0,20,20,40,40,60,100])
levels=[np.array([0,0,0,0,1,1,0,0,0]),np.array([0,0,0,0,1,1,0,0,0]),
        np.array([0,0,1,1,1,1,1,1,1])]
for ax,y,label,color in zip(axes,levels,["GPIO18 · PUL","Corriente del opto","GPIO19 · DIR"],[TEAL,ORANGE,INK]):
    ax.plot(t,y,color=color,lw=2)
    ax.set(ylim=(-.2,1.8),yticks=[0,1],ylabel=label,xlim=(-20,100))
    ax.grid(alpha=.15)
for a,b,label in [(0,20,r"$t_{\rm DIR}=20\,\mu s$"),(20,40,r"$t_{\rm PUL}=20\,\mu s$"),(40,60,r"$t_{\rm hold}=20\,\mu s$")]:
    arrow(axes[0],(a,1.35),(b,1.35),style="<->",lw=1)
    axes[0].text((a+b)/2,1.52,label,ha="center",fontsize=10)
for ax in axes:
    for x in [0,20,40,60]:ax.axvline(x,color=GRAY,ls=":",lw=.7)
axes[-1].set_xlabel("Tiempo (µs)")
save(fig,"stepper-pulsos")

# 5. Ideal rest-to-rest profiles in pulse coordinates, converted to degrees.
fig,axes=plt.subplots(2,2,figsize=(11.5,6.6),constrained_layout=True)
for col,(d,color) in enumerate([(400,TEAL),(1600,ORANGE)]):
    a=800.;v=min(800.,np.sqrt(a*d));ta=v/a;tc=max(0.,(d-v*v/a)/v);T=2*ta+tc
    t=np.linspace(0,T,501);q=np.empty_like(t);vel=np.empty_like(t)
    for k,x in enumerate(t):
        if x<ta:q[k]=.5*a*x*x;vel[k]=a*x
        elif x<ta+tc:q[k]=.5*a*ta*ta+v*(x-ta);vel[k]=v
        else:q[k]=d-.5*a*(T-x)**2;vel[k]=a*(T-x)
    axes[0,col].plot(t,q*.225,color=color,lw=2)
    axes[1,col].plot(t,vel*.225,color=color,lw=2)
    axes[0,col].set_title(f"{d} pulsos · {d*.225:g}° · T ≈ {T:.2f} s")
    for ax in axes[:,col]:ax.grid(alpha=.18);ax.set_xlim(0,T)
    axes[1,col].set_xlabel("Tiempo (s)")
axes[0,0].set_ylabel(r"Posición solicitada $\theta_d$ (°)")
axes[1,0].set_ylabel(r"Velocidad solicitada $\dot{\theta}_d$ (°/s)")
save(fig,"stepper-perfiles")

# 6. Conceptual horizontal slide with lead screw, not a construction drawing.
fig,ax=canvas(13,5.5,130,55)
box(ax,4,18,18,22,fill="#edf3f5");ax.text(13,29,"NEMA\n17",ha="center",va="center",fontsize=12)
box(ax,23,27,7,4,fill="#dde6e9");line(ax,[(22,29),(23,29)],lw=3)
line(ax,[(30,29),(122,29)],GRAY,lw=2)
for x in np.arange(31,121,2.4):line(ax,[(x,27.5),(x+1.4,30.5)],GRAY,lw=.9)
for y in [18,40]:line(ax,[(31,y),(122,y)],GRAY,lw=3)
box(ax,66,15,19,28,fill="#e4f1f0")
box(ax,71,25,9,8,fill="#f7e2c8")
ax.text(75.5,47,"Carro y tuerca",ha="center",fontsize=11)
ax.text(105,33,"Husillo",ha="center",fontsize=10)
arrow(ax,(88,46),(114,46),TEAL);ax.text(101,49,r"$+x$",ha="center",fontsize=13)
for x,label in [(32,"HOME"),(121,"Límite +")]:
    box(ax,x-3,8,6,4,fill="#f2f3f4")
    line(ax,[(x,12),(x+3,16)])
    ax.text(x,4,label,ha="center",fontsize=10)
ax.plot([43,43],[13,42],ls="--",color=TEAL,lw=1)
ax.text(43,47,r"$x=0$",ha="center",fontsize=12,color=TEAL)
arrow(ax,(32,1),(43,1),style="<->",lw=1)
ax.text(38,-2,"Retirada de 5 mm",ha="center",fontsize=9,color=GRAY)
ax.text(91,1,"Origen útil separado del contacto HOME",ha="center",fontsize=10,color=GRAY)
save(fig,"stepper-mesa")

# 7. Input circuits with external pull-ups for NC sensors.
fig,axes=plt.subplots(1,3,figsize=(12.2,5.2))
for ax,(gpio,label,nc) in zip(axes,[(32,"HOME",True),(33,"Límite positivo",True),(27,"Pulsador del indexador",False)]):
    ax.set(xlim=(0,44),ylim=(0,55));ax.set_aspect("equal");ax.axis("off")
    ax.text(22,51,label,ha="center",fontsize=12,weight="semibold",color=INK)
    line(ax,[(18,43),(18,38)]);ax.text(18,45,"3V3",ha="center",fontsize=10)
    box(ax,16,30,4,8);line(ax,[(18,30),(18,22),(37,22)])
    dot(ax,18,22);pin(ax,37,22)
    ax.text(39,22,f"GPIO{gpio}",ha="left",va="center",fontsize=9,color=TEAL)
    ax.text(24,34,"10 kΩ" if nc else "Pull-up\ninterno",va="center",fontsize=10)
    line(ax,[(18,22),(18,18)])
    line(ax,[(18,10),(18,18)] if nc else [(18,10),(13,17)])
    pin(ax,18,10);pin(ax,18,18)
    ax.text(10,14,"NC" if nc else "NO",ha="right",va="center",fontsize=10)
    line(ax,[(18,10),(18,7)]);ground(ax,18,7)
    ax.text(22,0,"Abierto → HIGH" if nc else "Pulsado → LOW",ha="center",fontsize=10,color=GRAY)
fig.subplots_adjust(wspace=.45)
save(fig,"stepper-entradas")
