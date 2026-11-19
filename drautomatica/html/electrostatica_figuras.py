"""Ilustraciones originales para electrostatica.html.

Las líneas del dipolo se calculan integrando la dirección del campo de dos
cargas puntuales opuestas. Las restantes figuras son esquemas conceptuales.
Los PNG se recortan verticalmente al contenido sin alterar el HTML editorial.
"""
from pathlib import Path
import io
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle, Ellipse, Polygon
from scipy.integrate import solve_ivp
from PIL import Image, ImageChops

OUT = Path(__file__).resolve().parent
INK, TEAL, GRAY = '#263f50', '#197b80', '#6e7c85'
POS, NEG, ORANGE = '#ba5844', '#3e6aa7', '#bd7129'
plt.rcParams.update({'font.family':'DejaVu Sans', 'font.size':11,
                     'mathtext.fontset':'stix', 'figure.facecolor':'white'})


def setup(w=9, h=4.5, xlim=(0,10), ylim=(0,5)):
    fig, ax = plt.subplots(figsize=(w,h))
    ax.set(xlim=xlim, ylim=ylim, aspect='equal')
    ax.axis('off')
    return fig,ax


def text(ax,x,y,s,**kw):
    kw.setdefault('ha','center');kw.setdefault('va','center');kw.setdefault('color',INK)
    return ax.text(x,y,s,**kw)


def line(ax,x,y,color=INK,lw=1.5,**kw):
    return ax.plot(x,y,color=color,lw=lw,**kw)


def arrow(ax,a,b,color=TEAL,lw=1.8,**kw):
    return ax.annotate('',xy=b,xytext=a,
        arrowprops={'arrowstyle':'-|>','mutation_scale':13,'color':color,'lw':lw,**kw})


def charge(ax,x,y,sign=1,r=.25):
    color=POS if sign>0 else NEG
    ax.add_patch(Circle((x,y),r,fc='#fcf0ec' if sign>0 else '#edf3fb',ec=color,lw=1.5,zorder=5))
    text(ax,x,y,'+' if sign>0 else '−',color=color,fontsize=17,zorder=6)


def save(fig,name):
    buf=io.BytesIO()
    fig.savefig(buf,format='png',dpi=260,bbox_inches='tight',pad_inches=.025,facecolor='white')
    buf.seek(0);im=Image.open(buf).convert('RGB')
    d=ImageChops.difference(im,Image.new('RGB',im.size,'white'))
    box=d.convert('L').point(lambda v:255 if v>12 else 0).getbbox()
    assert box is not None
    im.crop((0,max(0,box[1]-3),im.width,min(im.height,box[3]+3))).save(
        OUT/f'electrostatica-{name}.png',optimize=True)
    plt.close(fig)


def polarizacion():
    fig,ax=setup(9.3,4.6,xlim=(0,10),ylim=(-.2,4.8))
    ax.add_patch(Ellipse((2.15,2.65),2.05,2.7,fc='#e5edf8',ec=NEG,lw=1.7))
    ax.add_patch(Polygon([(2.12,1.31),(1.97,1.07),(2.33,1.07)],fc=NEG,ec=NEG))
    line(ax,[2.14,2.04,2.21,2.1],[1.06,.7,.35,.02],color=GRAY,lw=1.2)
    for x,y in [(1.7,3.2),(2.45,3.35),(1.65,2.4),(2.58,2.55),(2.,1.82)]:
        text(ax,x,y,'−',fontsize=19,color=NEG)
    text(ax,2.1,4.5,'Globo con carga negativa',fontsize=12,color=NEG)
    ax.add_patch(Rectangle((6.15,1.45),2.55,1.85,fc='#faf7ee',ec=GRAY,lw=1.3))
    for y in [1.85,2.37,2.89]:
        text(ax,6.65,y,'+',fontsize=19,color=POS)
        text(ax,8.15,y,'−',fontsize=19,color=NEG)
    text(ax,7.42,4.5,'Papel con carga total nula',fontsize=12)
    text(ax,7.42,3.7,'Ligera separación de las cargas',fontsize=10,color=GRAY)
    arrow(ax,(7.5,.8),(5.4,.8),ORANGE,lw=2.2)
    text(ax,6.45,.34,'Fuerza resultante de atracción',fontsize=11,color=ORANGE)
    text(ax,4.5,2.6,'Sin contacto',fontsize=11,color=GRAY)
    save(fig,'polarizacion')


def fuerzas():
    fig,ax=setup(9,4.7,xlim=(0,10),ylim=(0,5.6))
    text(ax,5,5.3,'Cargas del mismo signo: repulsión',fontsize=12)
    text(ax,5,2.5,'Cargas de signos opuestos: atracción',fontsize=12)
    for y,s2 in [(4.35,1),(1.55,-1)]:
        charge(ax,3,y,1,r=.32);charge(ax,7,y,s2,r=.32)
        if s2>0:
            arrow(ax,(2.62,y),(1.15,y),ORANGE,lw=2)
            arrow(ax,(7.38,y),(8.85,y),ORANGE,lw=2)
            text(ax,1.8,y+.48,r'$\vec{F}$',fontsize=17,color=ORANGE)
            text(ax,8.2,y+.48,r'$\vec{F}$',fontsize=17,color=ORANGE)
        else:
            arrow(ax,(3.38,y),(4.85,y),ORANGE,lw=2)
            arrow(ax,(6.62,y),(5.15,y),ORANGE,lw=2)
            text(ax,4.15,y+.48,r'$\vec{F}$',fontsize=17,color=ORANGE)
            text(ax,5.85,y+.48,r'$\vec{F}$',fontsize=17,color=ORANGE)
        line(ax,[3,3,7,7],[y-.7,y-.9,y-.9,y-.7],color=GRAY,lw=1)
        text(ax,5,y-.94,r'$r$',fontsize=16,color=GRAY,va='top')
    save(fig,'fuerzas')


def campo():
    fig,ax=setup(7.1,5.5,xlim=(-2.8,2.8),ylim=(-2.55,2.7))
    for theta in np.linspace(0,2*np.pi,12,endpoint=False):
        u=np.array([np.cos(theta),np.sin(theta)])
        line(ax,[.37*u[0],2.25*u[0]],[.37*u[1],2.25*u[1]],color=TEAL,lw=1.3)
        arrow(ax,1.32*u,1.63*u,TEAL,lw=1.5)
    charge(ax,0,0,1,r=.34)
    text(ax,-.62,.36,r'$Q>0$',fontsize=15,color=POS)
    # Un vector local, tangente a su línea radial.
    p=np.array([1.28,1.28]);u=p/np.linalg.norm(p)
    ax.plot(*p,'o',color=INK,ms=3)
    arrow(ax,p,p+.72*u,ORANGE,lw=2.2)
    text(ax,1.72,2.18,r'$\vec{E}$',fontsize=20,color=ORANGE)
    text(ax,1.47,1.08,'P',fontsize=11)
    save(fig,'campo')


def potencial():
    fig,ax=setup(8.6,5.5,xlim=(-2.3,3.7),ylim=(-2.25,2.25))
    for r,V in [(.6,60),(1.2,30),(1.8,20)]:
        ax.add_patch(Circle((0,0),r,fill=False,ec=TEAL,lw=1.6))
        # Líneas de llamada horizontales, separadas de los rótulos.
        theta=np.deg2rad(45)
        px,py=r*np.cos(theta),r*np.sin(theta)
        line(ax,[px,2.5],[py,py],color=GRAY,lw=.8)
        text(ax,2.62,py,f'{V} V',ha='left',fontsize=12,color=TEAL,
             bbox={'fc':'white','ec':'none','pad':1})
    for theta in np.deg2rad([180,225,270,315]):
        u=np.array([np.cos(theta),np.sin(theta)])
        arrow(ax,.4*u,2.05*u,ORANGE,lw=1.3)
    charge(ax,0,0,1,r=.23)
    text(ax,2.65,-.75,'Mismo potencial\nen cada circunferencia',fontsize=11)
    text(ax,2.65,-1.65,'El campo apunta\nhacia potenciales menores',fontsize=10,color=ORANGE)
    save(fig,'potencial')


def placas():
    fig,ax=setup(9,5.1,xlim=(0,8.4),ylim=(-.7,4.6))
    ax.add_patch(Rectangle((.9,.05),.18,3.7,fc=POS,ec=POS))
    ax.add_patch(Rectangle((7.,.05),.18,3.7,fc=NEG,ec=NEG))
    for y in [.35,1.15,1.95,2.75,3.55]:
        text(ax,.62,y,'+',fontsize=15,color=POS)
        text(ax,7.47,y,'−',fontsize=15,color=NEG)
    for x,V in [(3.05,6),(5.08,3)]:
        line(ax,[x,x],[.1,3.75],color=GRAY,lw=1,ls=(0,(4,4)))
        text(ax,x,4.1,f'{V} V',fontsize=12,color=GRAY)
    for y in [.5,3.3]:
        for x in [1.35,3.45,5.55]:arrow(ax,(x,y),(x+1.1,y),TEAL,lw=1.4)
    charge(ax,3.65,2.35,1,r=.22);arrow(ax,(3.94,2.35),(4.78,2.35),ORANGE)
    text(ax,4.4,2.75,r'$\vec{F}_{+}$',fontsize=16,color=ORANGE)
    charge(ax,5.7,1.3,-1,r=.22);arrow(ax,(5.41,1.3),(4.57,1.3),ORANGE)
    text(ax,4.4,.95,r'$\vec{F}_{-}$',fontsize=16,color=ORANGE)
    text(ax,1.,4.1,'9 V',fontsize=12,color=POS)
    text(ax,7.1,4.1,'0 V',fontsize=12,color=NEG)
    line(ax,[1.08,1.08,7.,7.],[-.13,-.38,-.38,-.13],color=GRAY,lw=1)
    text(ax,4.04,-.58,r'$d=5\ \mathrm{mm}$',fontsize=14)
    text(ax,4.04,3.65,r'$\vec{E}$',fontsize=16,color=TEAL)
    save(fig,'placas')


def dipolo():
    fig,ax=setup(8.5,5.3,xlim=(-2.5,2.5),ylim=(-2.5,2.5))
    plus=np.array([-1.35,0.]);minus=np.array([1.35,0.])
    def field(_,p):
        a=p-plus;b=p-minus
        e=a/np.linalg.norm(a)**3-b/np.linalg.norm(b)**3
        return e/np.linalg.norm(e)
    def endpoint(_,p):return np.linalg.norm(p-minus)-.20
    endpoint.terminal=True;endpoint.direction=-1
    for degrees in [-75,-55,-35,35,55,75]:
        th=np.deg2rad(degrees);p=plus+.23*np.array([np.cos(th),np.sin(th)])
        sol=solve_ivp(field,(0,25),p,max_step=.018,rtol=1e-7,atol=1e-9,events=endpoint)
        xy=sol.y.T
        ax.plot(xy[:,0],xy[:,1],color=TEAL,lw=1.2)
        idx=np.argmin(abs(xy[:,0]))
        if idx+4<len(xy):arrow(ax,xy[max(0,idx-3)],xy[idx+4],TEAL,lw=1.2)
    line(ax,[-1.12,1.12],[0,0],color=TEAL,lw=1.2)
    line(ax,[0,0],[-1.95,1.95],color=GRAY,lw=1,ls=(0,(4,4)))
    charge(ax,*plus,1,r=.23);charge(ax,*minus,-1,r=.23)
    text(ax,-1.92,0,r'$+Q$',fontsize=15,color=POS)
    text(ax,1.92,0,r'$-Q$',fontsize=15,color=NEG)
    ax.plot(0,0,'o',color=INK,ms=4)
    text(ax,-.17,-.20,'P',fontsize=11)
    arrow(ax,(.12,0),(.82,0),ORANGE,lw=2.3)
    text(ax,.58,.23,r'$\vec{E}$',fontsize=18,color=ORANGE)
    text(ax,0,2.25,'Potencial nulo sobre la mediatriz',fontsize=11,color=GRAY)
    text(ax,0,-2.25,r'$V(P)=0,\qquad E(P)>0$',fontsize=17)
    save(fig,'dipolo')


def voltimetro():
    fig,ax=setup(8.8,5.4,xlim=(-.3,8.8),ylim=(0,5.8))
    # Fuente de 9 V, resistencia y voltímetro en paralelo. Sin cruces ambiguos.
    line(ax,[1.,1.,7.,7.],[3.1,5.,5.,3.8],lw=1.6)
    line(ax,[1.,1.,7.,7.],[2.65,.8,.8,2.2],lw=1.6)
    line(ax,[.42,1.58],[3.1,3.1],lw=2.2)
    line(ax,[.72,1.28],[2.65,2.65],lw=2.2)
    text(ax,.15,3.13,'+',fontsize=16,color=POS)
    text(ax,.15,2.65,'−',fontsize=16,color=NEG)
    text(ax,.15,4.05,'Pila\n9 V',fontsize=12)
    ax.add_patch(Rectangle((6.65,2.2),.7,1.6,fc='#f5f0e5',ec=INK,lw=1.6))
    text(ax,8.0,3.,'Resistencia',fontsize=11)
    # Instrumento con sus dos terminales conectados a los mismos nodos A y B.
    ax.add_patch(Circle((4.,2.9),.58,fc='#f1f6f5',ec=TEAL,lw=1.6))
    text(ax,4.,2.9,'V',fontsize=22,color=TEAL)
    line(ax,[4.,4.],[5.,3.48],color=POS,lw=1.6)
    line(ax,[4.,4.],[2.32,.8],color=NEG,lw=1.6)
    for x,y in [(4.,5.),(4.,.8)]:ax.add_patch(Circle((x,y),.045,fc=INK))
    text(ax,4.3,4.35,'+',fontsize=14,color=POS)
    text(ax,4.3,1.5,'−',fontsize=14,color=NEG)
    text(ax,4.,5.45,'A',fontsize=13)
    text(ax,4.,.35,'B',fontsize=13)
    text(ax,5.05,1.6,'Lectura: +9 V',fontsize=11,color=TEAL,ha='left')
    save(fig,'voltimetro')


if __name__=='__main__':
    for fn in [polarizacion,fuerzas,campo,potencial,placas,dipolo,voltimetro]:fn()
    print('Siete ilustraciones generadas en PNG.')
