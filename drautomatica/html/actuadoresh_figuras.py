"""Diagramas originales de actuadoresh.html.

Genera PNG recortados al contenido sin cambiar el espaciado de la plantilla.
Ejecutar con MPLCONFIGDIR en un directorio escribible.
"""
from pathlib import Path
import io
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, Polygon, FancyBboxPatch, Arc
from PIL import Image, ImageChops
from actuadoresn_figuras import setup, line, text, arrow, rect, spring, leader, INK, TEAL, ORANGE, GRAY, METAL, PALE

OUT = Path(__file__).resolve().parent
OIL = '#e0efeb'
GAS = '#e8eff8'


def save(fig, name):
    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=260, bbox_inches='tight', pad_inches=.025, facecolor='white')
    buf.seek(0)
    im = Image.open(buf).convert('RGB')
    diff = ImageChops.difference(im, Image.new('RGB', im.size, 'white'))
    box = diff.convert('L').point(lambda v: 255 if v > 12 else 0).getbbox()
    assert box is not None
    im.crop((0, max(0, box[1]-3), im.width, min(im.height, box[3]+3))).save(
        OUT / f'actuadoresh-{name}.png', optimize=True)
    plt.close(fig)


def central():
    fig, ax = setup(10, 5.0, xlim=(-.2, 12.2), ylim=(-.2, 6.0))
    # Diagrama funcional; los bloques de mando no representan símbolos ISO.
    ax.add_patch(Circle((.65, 4.1), .48, fc=PALE, ec=INK, lw=1.5))
    text(ax, .65, 4.1, 'M', fontsize=15)
    line(ax, [1.13, 1.92], [4.1, 4.1], lw=2)
    ax.add_patch(Circle((2.5, 4.1), .58, fc='white', ec=INK, lw=1.5))
    ax.add_patch(Polygon([(2.62,3.92),(2.62,4.28),(3.0,4.1)], fc=INK))
    text(ax, .65, 5.1, 'Motor\neléctrico', fontsize=10)
    text(ax, 2.5, 5.1, 'Bomba', fontsize=11)
    for x, label, width in [(5.5, 'Válvula\ndireccional', 2.1), (9.15, 'Cilindro\ny carga', 2.25)]:
        rect(ax, x, 3.25, width, 1.7, fc=OIL)
        text(ax, x+width/2, 4.1, label, fontsize=11)
    line(ax, [3.08,5.5], [4.1,4.1], color=TEAL, lw=2)
    arrow(ax,(4.65,4.1),(5.35,4.1))
    text(ax, 5.24, 4.42, 'P', fontsize=12, color=TEAL)
    arrow(ax, (7.6,4.57), (9.15,4.57), TEAL, lw=2)
    arrow(ax, (9.15,3.62), (7.6,3.62), GRAY, lw=2)
    text(ax, 8.37,4.87, 'A', fontsize=12, color=TEAL)
    text(ax, 8.37,3.3, 'B', fontsize=12, color=GRAY)
    # Un único retorno desde T al depósito.
    line(ax,[6.55,6.55,3.7,3.7],[3.25,1.0,1.0,.78],color=GRAY,lw=1.8)
    arrow(ax,(5.8,1.),(4.8,1.),GRAY)
    text(ax,6.83,2.9,'T',fontsize=12,color=GRAY)
    text(ax,5.4,.59,'Retorno',fontsize=10,color=GRAY)
    # Depósito abierto, con aspiración sumergida.
    rect(ax,1.3,.1,3.1,.65,fc=OIL,ec='none')
    line(ax,[1.3,1.3,4.4,4.4],[1.05,.1,.1,1.05])
    line(ax,[1.3,4.4],[.75,.75],color=TEAL,lw=1)
    text(ax,2.85,-.13,'Depósito',fontsize=11)
    line(ax,[2.5,2.5],[.45,3.52],color=TEAL,lw=1.8)
    arrow(ax,(2.5,2.0),(2.5,2.75))
    text(ax,1.82,2.5,'Aspiración',rotation=90,fontsize=10,color=GRAY)
    # Alivio en derivación desde la descarga; su salida entra al mismo depósito.
    line(ax,[4.,4.],[4.1,2.92],color=ORANGE,lw=1.5)
    ax.add_patch(Circle((4.,4.1),.045,fc=INK))
    rect(ax,3.55,2.05,.9,.87,fc='white',ec=ORANGE)
    arrow(ax,(4.,2.8),(4.,2.15),ORANGE,lw=1.2)
    line(ax,[4.,4.],[2.05,.78],color=ORANGE,lw=1.5)
    text(ax,4.75,2.5,'Alivio',ha='left',fontsize=10,color=ORANGE)
    # Mando eléctrico identificado mediante trazo discontinuo.
    line(ax,[6.55,6.55],[5.75,4.95],color=GRAY,lw=1.3,ls='--')
    arrow(ax,(6.55,5.25),(6.55,4.96),GRAY,lw=1.2)
    text(ax,6.55,5.91,'Mando eléctrico',fontsize=10,color=GRAY)
    text(ax,9.4,1.65,'El aceite retorna al depósito.\nFiltrado y enfriamiento según el equipo.',fontsize=10,color=GRAY)
    save(fig,'central')


def simple():
    fig,ax=setup(8.5,5.5,xlim=(.1,9.6),ylim=(-.2,6.3))
    # Cilindro de émbolo buzo: aceite debajo, retorno por el peso exterior.
    rect(ax,2.,.8,2.6,3.6,fc=PALE)
    rect(ax,2.12,.93,2.36,3.25,fc=OIL,ec='none')
    rect(ax,2.57,2.0,1.46,2.9,fc=METAL)
    rect(ax,1.9,.7,2.8,.22,fc=METAL)
    rect(ax,2.,4.23,2.6,.22,fc=METAL)
    rect(ax,2.52,4.23,1.56,.2,fc=TEAL,ec='none')
    rect(ax,2.67,4.22,1.26,.24,fc=METAL,ec='none')
    rect(ax,1.9,4.9,2.8,.65,fc='#e8e0d4')
    text(ax,3.3,5.23,'Carga',fontsize=12)
    arrow(ax,(3.3,6.1),(3.3,5.58),ORANGE,lw=2)
    text(ax,4.05,5.9,'Peso',fontsize=11,color=ORANGE)
    arrow(ax,(1.25,3.0),(1.25,4.1))
    text(ax,.85,3.55,'Elevación',rotation=90,fontsize=10,color=TEAL)
    # Un puerto único: la misma conexión conduce el caudal en ambos sentidos.
    rect(ax,2.,1.05,.18,.22,fc=OIL,ec='none')
    line(ax,[.65,2.2],[1.05,1.05]);line(ax,[.65,2.2],[1.27,1.27])
    arrow(ax,(.7,.55),(1.7,.55));arrow(ax,(1.7,.12),(.7,.12),GRAY)
    text(ax,3.1,1.4,'Aceite',fontsize=11,color=TEAL)
    leader(ax,'Émbolo buzo',(3.85,3.1),(6.65,3.8),fontsize=11)
    leader(ax,'Guía y sello',(4.02,4.35),(6.65,4.7),fontsize=11)
    leader(ax,'Conexión única',(.8,1.16),(6.45,1.1),fontsize=11)
    text(ax,6.5,2.3,'La carga desciende al\npermitir un retorno\ncontrolado del aceite.',fontsize=11,color=GRAY)
    save(fig,'simple')


def doble():
    fig,ax=setup(10,4.1,xlim=(.5,11.0),ylim=(-.3,4.2))
    rect(ax,1.4,1.,6.3,1.7,fc=OIL)
    rect(ax,1.3,.9,.22,1.9,fc=METAL);rect(ax,7.6,.9,.3,1.9,fc=METAL)
    rect(ax,4.25,1.02,.28,1.66,fc=METAL)
    rect(ax,4.53,1.7,5.1,.3,fc=METAL)
    rect(ax,7.6,1.5,.34,.7,fc='#d8e0e4')
    line(ax,[4.29,4.29],[1.05,2.65],color=TEAL,lw=2)
    text(ax,2.9,1.98,r'$p_A,\ A_p$',fontsize=16,color=TEAL)
    text(ax,6.1,2.29,r'$p_B,\ A_a$',fontsize=16,color=GRAY)
    for x in [2.2,7.]:
        rect(ax,x-.08,.96,.16,.15,fc=OIL,ec='none')
        line(ax,[x-.08,x-.08],[.3,1.12]);line(ax,[x+.08,x+.08],[.3,1.12])
    arrow(ax,(2.2,.35),(2.2,1.4));arrow(ax,(7.,1.4),(7.,.35),GRAY)
    text(ax,2.2,-.02,r'A · $Q_A$ entra',fontsize=11,color=TEAL)
    text(ax,7.,-.02,r'B · $Q_B$ sale',fontsize=11,color=GRAY)
    arrow(ax,(8.4,3.25),(9.8,3.25))
    text(ax,9.1,3.65,r'Avance $v>0$',fontsize=12,color=TEAL)
    arrow(ax,(3.55,3.28),(4.6,3.28));text(ax,3.25,3.3,r'$p_A A_p$',ha='right',fontsize=14,color=TEAL)
    arrow(ax,(6.55,3.28),(5.5,3.28),ORANGE);text(ax,6.8,3.3,r'$p_B A_a$',ha='left',fontsize=14,color=ORANGE)
    leader(ax,'Vástago',(9.,1.98),(9.25,2.6),fontsize=10)
    save(fig,'doble')


def valvula():
    fig,ax=setup(10,4.8,xlim=(-1.0,11.8),ylim=(-1.3,4.2))
    x0,y,w,h=1.6,.4,2.35,1.9
    for j in range(3):
        x=x0+j*w;rect(ax,x,y,w,h)
        a,b=x+.48,x+w-.48
        if j==0:
            arrow(ax,(a,y+.05),(a,y+h-.05),INK,lw=1.4)
            arrow(ax,(b,y+h-.05),(b,y+.05),INK,lw=1.4)
        elif j==2:
            arrow(ax,(a,y+.06),(b,y+h-.06),INK,lw=1.4)
            arrow(ax,(a,y+h-.06),(b,y+.06),INK,lw=1.4)
        else:
            for xp in [a,b]:
                line(ax,[xp,xp],[y,y+.45]);line(ax,[xp-.2,xp+.2],[y+.45,y+.45])
                line(ax,[xp,xp],[y+h,y+h-.45]);line(ax,[xp-.2,xp+.2],[y+h-.45,y+h-.45])
        text(ax,x+w/2,3.65,['Avance','Centro cerrado','Retroceso'][j],fontsize=11)
    # Conexiones externas referidas al cuadro central.
    a,b=x0+w+.48,x0+2*w-.48
    for xp,label in [(a,'A'),(b,'B')]:
        line(ax,[xp,xp],[y+h,3.0]);text(ax,xp,3.23,label,fontsize=13)
    for xp,label in [(a,'P'),(b,'T')]:
        line(ax,[xp,xp],[y,-.18]);text(ax,xp,-.43,label,fontsize=13)
    # Resortes de centrado y accionamientos por solenoide.
    spring(ax,.45,1.6,1.35,amp=.2,coils=5)
    spring(ax,8.65,9.8,1.35,amp=.2,coils=5)
    for x in [-.3,9.8]:
        rect(ax,x,1.,.75,.7);line(ax,[x+.08,x+.67],[1.07,1.63])
    text(ax,.45,.15,'Solenoide\ny resorte',fontsize=9)
    text(ax,9.8,.15,'Solenoide\ny resorte',fontsize=9)
    text(ax,5.1,-1.02,'P: alimentación · T: depósito · A y B: cámaras del cilindro',fontsize=11,color=GRAY)
    save(fig,'valvula')


def motor():
    fig,ax=setup(8.8,4.1,xlim=(-.2,9.7),ylim=(-.2,4.3))
    # Símbolo de motor reversible; triángulos sólidos dirigidos hacia el centro.
    c=(4.3,1.85);r=1.17
    ax.add_patch(Circle(c,r,fc='white',ec=INK,lw=1.8))
    for s in [-1,1]:
        x=c[0]+s*.9
        ax.add_patch(Polygon([(x,c[1]-.25),(x,c[1]+.25),(x-s*.48,c[1])],fc=INK))
    line(ax,[.65,3.13],[1.85,1.85],color=TEAL,lw=1.8)
    arrow(ax,(1.25,1.85),(2.3,1.85),TEAL)
    line(ax,[5.47,8.7],[1.85,1.85],color=GRAY,lw=1.8)
    arrow(ax,(7.,1.85),(8.1,1.85),GRAY)
    text(ax,1.8,2.35,r'$Q,\ p_{\mathrm{entrada}}$',fontsize=13,color=TEAL)
    text(ax,7.3,2.35,r'$p_{\mathrm{salida}}$',fontsize=13,color=GRAY)
    text(ax,4.3,.18,'Motor hidráulico reversible',fontsize=11)
    # Eje mecánico perpendicular a los puertos, con flecha de giro circular.
    line(ax,[4.3,4.3],[3.02,3.65],lw=3)
    ax.add_patch(Arc((4.3,3.45),1.1,.6,theta1=15,theta2=310,color=ORANGE,lw=1.7))
    theta=np.deg2rad(310)
    end=(4.3+.55*np.cos(theta),3.45+.3*np.sin(theta))
    prev=(4.3+.55*np.cos(theta-.16),3.45+.3*np.sin(theta-.16))
    arrow(ax,prev,end,ORANGE,lw=1.7)
    text(ax,5.3,3.55,r'$\tau,\ \omega$',fontsize=16,color=ORANGE)
    text(ax,4.3,4.1,'Salida mecánica al eje',fontsize=11)
    save(fig,'motor')


def acumulador():
    fig,ax=setup(8.2,5.0,xlim=(-.4,9.4),ylim=(-.2,5.8))
    shell=FancyBboxPatch((2.,.75),2.5,4.3,boxstyle='round,pad=0,rounding_size=1.1',fc=OIL,ec=INK,lw=1.8)
    ax.add_patch(shell)
    # Vejiga de gas unida a la válvula superior.
    gas=FancyBboxPatch((2.35,2.28),1.8,2.5,boxstyle='round,pad=0,rounding_size=.8',fc=GAS,ec=GRAY,lw=1.5)
    ax.add_patch(gas)
    line(ax,[3.25,3.25],[4.78,5.55],color=GRAY,lw=1.6)
    rect(ax,3.08,5.18,.34,.27,fc=METAL)
    text(ax,3.25,5.78,'Carga de nitrógeno',fontsize=11)
    text(ax,3.25,3.65,r'$p_{\mathrm{abs}},\ V$',fontsize=16)
    text(ax,3.25,3.05,'Gas',fontsize=11,color=GRAY)
    text(ax,3.25,1.52,'Aceite',fontsize=11,color=TEAL)
    rect(ax,3.1,.72,.3,.35,fc=OIL,ec='none')
    line(ax,[3.1,3.1],[.18,1.04]);line(ax,[3.4,3.4],[.18,1.04])
    arrow(ax,(2.15,.18),(2.9,.18),TEAL)
    arrow(ax,(3.6,.18),(4.35,.18),GRAY)
    text(ax,3.25,-.13,'Conexión al circuito',fontsize=10)
    leader(ax,'Vejiga flexible',(4.02,2.85),(6.8,4.1),fontsize=11)
    leader(ax,'Recipiente resistente',(4.49,1.9),(6.9,2.7),fontsize=11)
    text(ax,6.8,1.2,'Entra aceite → el gas se comprime.\nSale aceite → el gas se expande.',fontsize=10,color=GRAY)
    save(fig,'acumulador')


def control():
    fig,ax=setup(10.2,3.8,xlim=(-.3,14.8),ylim=(-1.5,3.8))
    blocks=[(1.6,2.3,'Controlador'),(4.75,2.4,'Válvula\nproporcional'),(8.0,2.4,'Cilindro\ny carga')]
    for x,w,label in blocks:
        rect(ax,x,.75,w,1.15,fc=OIL)
        text(ax,x+w/2,1.325,label,fontsize=11)
    ax.add_patch(Circle((.6,1.325),.26,fc='white',ec=INK,lw=1.3))
    text(ax,.6,1.325,'+',fontsize=12)
    arrow(ax,(-.2,1.325),(.34,1.325),INK)
    text(ax,.2,2.25,r'$x_{\mathrm{ref}}$',fontsize=14)
    for a,b in [(.86,1.6),(3.9,4.75),(7.15,8.0),(10.4,11.75)]:
        arrow(ax,(a,1.325),(b,1.325),INK,lw=1.3)
    text(ax,11.95,1.325,r'$x$',fontsize=16,ha='left')
    text(ax,4.3,2.3,'Mando',fontsize=9,color=GRAY)
    text(ax,7.6,2.3,'Caudal',fontsize=9,color=GRAY)
    text(ax,9.2,3.2,'Central hidráulica',fontsize=11,color=TEAL)
    arrow(ax,(9.2,2.85),(9.2,1.9),TEAL)
    # Realimentación tomada de la posición física de salida.
    line(ax,[11.2,11.2,8.65],[1.325,-.65,-.65],color=GRAY,lw=1.3)
    ax.add_patch(Circle((11.2,1.325),.045,fc=INK))
    rect(ax,4.8,-1.12,3.85,.95,fc=PALE)
    text(ax,6.725,-.645,'Transductor de posición',fontsize=10)
    line(ax,[4.8,.6,.6],[-.65,-.65,1.065],color=GRAY,lw=1.3)
    arrow(ax,(.6,.45),(.6,1.065),GRAY,lw=1.3)
    text(ax,.95,.7,'−',fontsize=15,color=GRAY)
    save(fig,'control')


if __name__ == '__main__':
    for draw in [central, simple, doble, valvula, motor, acumulador, control]:
        draw()
    D,d,L,Q,pA,pB,Ff=.05,.03,.25,12e-3/60,100e5,5e5,500
    Ap=np.pi*D**2/4;Aa=Ap-np.pi*d**2/4
    print({'Ap_mm2':Ap*1e6,'Aa_mm2':Aa*1e6,'F_avance_N':pA*Ap-pB*Aa-Ff,
           'F_retroceso_N':pA*Aa-pB*Ap-Ff,'v_avance_m_s':Q/Ap,
           'v_retroceso_m_s':Q/Aa,'t_avance_s':L*Ap/Q,'t_retroceso_s':L*Aa/Q,
           'Q_salida_retroceso_L_min':Q*Ap/Aa*60000,
           'motor_rpm':.9*15e-3/50e-6,'motor_torque_Nm':.85*80e5*50e-6/(2*np.pi)})
