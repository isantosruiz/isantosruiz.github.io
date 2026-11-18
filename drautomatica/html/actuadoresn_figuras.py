"""Ilustraciones técnicas originales de actuadoresn.html, en PNG y SVG.
Los PNG se recortan al contenido; el espaciado editorial lo conserva la plantilla.
"""
from pathlib import Path
import io
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, Polygon, Wedge, Arc, FancyBboxPatch
from PIL import Image, ImageChops

OUT=Path(__file__).resolve().parent
INK,TEAL,ORANGE,GRAY='#263f50','#197b80','#bd7129','#687b87'
AIR,METAL,PALE='#dcefee','#b5c3cc','#f3f5f6'
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,'mathtext.fontset':'stix',
                     'figure.facecolor':'white','svg.fonttype':'path'})

def setup(w=9,h=3.7,xlim=(0,11),ylim=(-.4,4.2)):
 fig,ax=plt.subplots(figsize=(w,h));ax.set(xlim=xlim,ylim=ylim,aspect='equal');ax.axis('off');return fig,ax

def line(ax,x,y,color=INK,lw=1.5,**kw):return ax.plot(x,y,color=color,lw=lw,**kw)
def text(ax,x,y,t,**kw):
 kw.setdefault('ha','center');kw.setdefault('va','center');kw.setdefault('color',INK)
 return ax.text(x,y,t,**kw)
def arrow(ax,a,b,color=TEAL,lw=1.6,**kw):
 return ax.annotate('',xy=b,xytext=a,arrowprops={'arrowstyle':'-|>','color':color,'lw':lw,'mutation_scale':12,**kw})
def rect(ax,x,y,w,h,fc='white',ec=INK,lw=1.5,**kw):
 p=Rectangle((x,y),w,h,facecolor=fc,edgecolor=ec,lw=lw,**kw);ax.add_patch(p);return p
def spring(ax,x1,x2,y,amp=.22,coils=8):
 x=np.linspace(x1+.15,x2-.15,2*coils+1);z=np.zeros_like(x);z[1:-1:2]=amp;z[2:-1:2]=-amp
 line(ax,[x1,x1+.15],[y,y]);line(ax,x,y+z);line(ax,[x2-.15,x2],[y,y])
def leader(ax,label,p,at,**kw):
 kw.setdefault('ha','center');kw.setdefault('va','center');kw.setdefault('color',INK)
 return ax.annotate(label,xy=p,xytext=at,
                    arrowprops={'arrowstyle':'-','color':GRAY,'lw':.85,'shrinkA':5,'shrinkB':2},**kw)
def save(fig,name):
 fig.savefig(OUT/f'actuadoresn-{name}.svg',bbox_inches='tight',pad_inches=.02,facecolor='white')
 buf=io.BytesIO();fig.savefig(buf,format='png',dpi=250,bbox_inches='tight',pad_inches=.02,facecolor='white');buf.seek(0)
 im=Image.open(buf).convert('RGBA');bg=Image.new('RGBA',im.size,'white');bg.alpha_composite(im)
 d=ImageChops.difference(bg.convert('RGB'),Image.new('RGB',im.size,'white'))
 box=d.convert('L').point(lambda x:255 if x>12 else 0).getbbox()
 assert box,name
 y0=max(0,box[1]-2);y1=min(im.height,box[3]+2)
 im.crop((0,y0,im.width,y1)).save(OUT/f'actuadoresn-{name}.png',optimize=True)
 plt.close(fig)


def cadena():
 fig,ax=setup(10,3.3,xlim=(0,13),ylim=(-1.4,3.2))
 blocks=[(.25,'Controlador'),(3.55,'Electroválvula'),(6.85,'Actuador'),(10.15,'Carga')]
 for x,t in blocks:
  ax.add_patch(FancyBboxPatch((x,.25),2.55,1,boxstyle='round,pad=.02,rounding_size=.06',fc='#edf5f4',ec=TEAL,lw=1.3));text(ax,x+1.275,.75,t)
 for x in [2.8,6.1,9.4]:arrow(ax,(x,.75),(x+.75,.75),INK,lw=1.25)
 text(ax,3.15,1.55,'Mando eléctrico',fontsize=10,color=GRAY)
 text(ax,6.5,1.55,'Aire dirigido',fontsize=10,color=GRAY)
 text(ax,9.75,1.55,'Fuerza y movimiento',fontsize=10,color=GRAY)
 text(ax,4.825,2.8,'Red de aire · filtrado · regulación',fontsize=11,color=TEAL)
 arrow(ax,(4.825,2.4),(4.825,1.25),TEAL)
 line(ax,[11.425,11.425,1.525,1.525],[.25,-.65,-.65,.25],color=GRAY,lw=1.2)
 arrow(ax,(1.525,-.2),(1.525,.25),GRAY,lw=1.2)
 text(ax,6.5,-1.02,'Realimentación: posición, presión, fuerza o presencia de pieza',fontsize=10,color=GRAY)
 save(fig,'cadena')


def cilindro(simple=False):
 fig,ax=setup(10,4.1,xlim=(.5,10.8),ylim=(-.15,4.25))
 rect(ax,1.4,1.0,6.3,1.7,fc=PALE)
 rect(ax,1.45,1.05,2.8,1.6,fc=AIR,ec='none')
 rect(ax,1.3,.9,.22,1.9,fc=METAL);rect(ax,7.6,.9,.3,1.9,fc=METAL)
 rect(ax,4.25,1.02,.28,1.66,fc=METAL)
 rect(ax,4.53,1.72,5.05,.26,fc=METAL)
 rect(ax,7.6,1.5,.34,.7,fc='#d8e0e4')
 # El sello rodea el émbolo y separa las cámaras.
 line(ax,[4.29,4.29],[1.05,2.65],color=TEAL,lw=2)
 leader(ax,'Émbolo',(4.39,2.65),(4.05,3.45),fontsize=11)
 leader(ax,'Vástago',(8.9,1.98),(8.9,2.7),fontsize=11)
 arrow(ax,(8.5,3.25),(9.75,3.25));text(ax,9.1,3.58,'Avance',fontsize=11,color=TEAL)
 # Puerto A hacia la cámara posterior.
 rect(ax,2.12,.96,.16,.14,fc=AIR,ec='none')
 line(ax,[2.12,2.12],[.45,1.12]);line(ax,[2.28,2.28],[.45,1.12])
 arrow(ax,(2.2,.48),(2.2,1.45))
 text(ax,2.7,.12,'A · alimentación / escape' if simple else 'A · cámara posterior',fontsize=10)
 text(ax,2.8,2.0,'Aire comprimido' if simple else r'$p_A$',fontsize=12,color=TEAL)
 if simple:
  spring(ax,4.55,7.58,1.85,amp=.33,coils=7)
  text(ax,6.0,2.45,'Resorte',fontsize=10)
  # El lado del resorte comunica con la atmósfera.
  rect(ax,6.9,2.62,.18,.18,fc='white',ec='none')
  line(ax,[6.9,6.9,7.08,7.08],[2.6,3.05,3.05,2.6],color=GRAY,lw=1)
  leader(ax,'Respiradero',(7.0,3.05),(6.8,3.85),fontsize=10)
  arrow(ax,(9.6,1.15),(8.55,1.15),ORANGE)
  text(ax,9.1,.8,'Retorno por resorte',fontsize=10,color=ORANGE)
 else:
  text(ax,6.3,2.27,r'$p_B$',fontsize=13,color=GRAY)
  rect(ax,6.92,.96,.16,.14,fc=PALE,ec='none')
  line(ax,[6.92,6.92],[.45,1.12]);line(ax,[7.08,7.08],[.45,1.12])
  arrow(ax,(7.,1.45),(7.,.48),GRAY)
  text(ax,7.0,.12,'B · cámara del vástago',fontsize=10)
  text(ax,5.9,3.8,'Posición mostrada: avance, A presurizada y B al escape',fontsize=10,color=GRAY)
 save(fig,'simple' if simple else 'doble')


def valvula():
 fig,ax=setup(9.5,4.1,xlim=(-.6,8.5),ylim=(-1.3,3.2))
 # Dos posiciones; la contigua al resorte es la de reposo.
 x0,y,w,h=1.0,.45,2.5,1.75
 for j in range(2):
  x=x0+j*w;rect(ax,x,y,w,h,fc='white')
  r,p,s=x+.38,x+1.25,x+2.12;a,b=x+.58,x+1.92
  if j==0:
   arrow(ax,(p,y+.05),(a,y+h-.05),INK,lw=1.35)
   arrow(ax,(b,y+h-.05),(s,y+.05),INK,lw=1.35)
   line(ax,[r,r],[y,y+.35]);line(ax,[r-.17,r+.17],[y+.35,y+.35])
  else:
   arrow(ax,(p,y+.05),(b,y+h-.05),INK,lw=1.35)
   arrow(ax,(a,y+h-.05),(r,y+.05),INK,lw=1.35)
   line(ax,[s,s],[y,y+.35]);line(ax,[s-.17,s+.17],[y+.35,y+.35])
  text(ax,x+w/2,2.65,'Accionada' if j==0 else 'Reposo',fontsize=11)
 # Conexiones exteriores del cuadro de reposo.
 x=x0+w
 for pos,lab in [(x+.58,'2 (A)'),(x+1.92,'4 (B)')]:
  line(ax,[pos,pos],[y+h,2.55]);text(ax,pos,2.97,lab,fontsize=11)
 for pos,lab in [(x+.38,'3 (R)'),(x+1.25,'1 (P)'),(x+2.12,'5 (S)')]:
  line(ax,[pos,pos],[y,-.05]);text(ax,pos,-.38,lab,fontsize=11)
 rect(ax,.3,.97,.7,.7,fc='white');line(ax,[.36,.94],[1.02,1.62]);line(ax,[-.2,.3],[1.32,1.32])
 text(ax,.53,.3,'Bobina',fontsize=10)
 spring(ax,6.,7.25,1.32,amp=.22,coils=5)
 text(ax,6.7,.57,'Resorte',fontsize=10)
 text(ax,3.85,-.96,'P: suministro · A y B: utilización · R y S: escape',fontsize=11,color=GRAY)
 save(fig,'valvula')


def ventosa():
 fig,ax=setup(8.6,4.5,xlim=(.4,8.7),ylim=(-1.0,4.3))
 rect(ax,.8,.15,7.4,.32,fc='#d3dce1')
 # Sección de una ventosa: cámara sellada y labios apoyados en la pieza.
 chamber=[(2,.47),(2.6,.75),(3.45,1.6),(3.6,2.45),(5.4,2.45),(5.55,1.6),(6.4,.75),(7,.47)]
 ax.add_patch(Polygon(chamber,closed=True,fc=AIR,ec='none'))
 line(ax,[2,2.6,3.45,3.6,4.3],[.47,.75,1.6,2.45,2.45],TEAL,lw=4)
 line(ax,[4.7,5.4,5.55,6.4,7],[2.45,2.45,1.6,.75,.47],TEAL,lw=4)
 line(ax,[4.3,4.3],[2.45,3.5],TEAL,lw=2);line(ax,[4.7,4.7],[2.45,3.5],TEAL,lw=2)
 arrow(ax,(4.5,2.7),(4.5,3.8),TEAL)
 text(ax,5.8,3.7,'Al generador\nde vacío',fontsize=11)
 text(ax,4.5,1.92,r'$p_{\mathrm{vac}}$',fontsize=15,color=TEAL)
 arrow(ax,(4.5,.58),(4.5,1.4),ORANGE,lw=2)
 text(ax,4.85,.98,r'$F$',fontsize=16,color=ORANGE)
 for x in [2.7,6.2]:arrow(ax,(x,-.55),(x,.11),GRAY)
 text(ax,4.5,-.76,r'$p_{\mathrm{atm}}>p_{\mathrm{vac}}$',fontsize=14,color=GRAY)
 text(ax,7.6,.9,'Pieza',fontsize=11)
 save(fig,'ventosa')


def diafragma():
 fig,ax=setup(8.2,4.8,xlim=(.5,8.5),ylim=(0,5.9))
 # Cámara superior y cámara inferior ventilada.
 dome=[(2,3)]+[(4+2*np.cos(t),3+1.55*np.sin(t)) for t in np.linspace(np.pi,0,80)]+[(6,1.4),(2,1.4)]
 ax.add_patch(Polygon(dome,closed=True,fc=PALE,ec=INK,lw=1.5))
 upper=[(2,3)]+[(4+2*np.cos(t),3+1.55*np.sin(t)) for t in np.linspace(np.pi,0,80)]+[(4.8,2.72),(3.2,2.72)]
 ax.add_patch(Polygon(upper,closed=True,fc=AIR,ec='none'))
 line(ax,[2,3.2,4.8,6],[3,2.72,2.72,3],TEAL,lw=3)
 rect(ax,3.2,2.58,1.6,.14,fc=METAL)
 rect(ax,3.88,.35,.24,2.25,fc=METAL)
 # Resorte axial alrededor del vástago, apoyado en la base.
 yy=np.linspace(1.53,2.48,13);xx=np.full_like(yy,4.);xx[1:-1:2]=3.68;xx[2:-1:2]=4.32
 line(ax,xx,yy,lw=1.3)
 line(ax,[3.9,3.9],[4.52,5.2]);line(ax,[4.1,4.1],[4.52,5.2])
 arrow(ax,(4.,5.58),(4.,4.85));text(ax,4.0,5.85,'Presión de mando',fontsize=11,color=TEAL)
 leader(ax,'Diafragma',(5.5,2.9),(7.0,3.65),fontsize=11)
 leader(ax,'Resorte',(4.28,1.9),(6.6,2.0),fontsize=11)
 leader(ax,'Vástago',(4.,.6),(6.4,.6),fontsize=11)
 text(ax,4.,3.75,r'$p_g A_{\mathrm{ef}}$',fontsize=15,color=TEAL)
 arrow(ax,(4.,3.45),(4.,2.98))
 line(ax,[2.,1.6],[1.85,1.85],color=GRAY);text(ax,1.3,1.25,'Cámara\nventilada',fontsize=10,color=GRAY)
 save(fig,'diafragma')


def giratorio():
 fig,ax=setup(8.2,5.5,xlim=(.2,8.4),ylim=(-.1,5.9))
 c=(4.,2.8);R=1.9;angle=40
 ax.add_patch(Wedge(c,R,270,360+angle,fc=AIR,ec='none'))
 ax.add_patch(Wedge(c,R,angle,270,fc=PALE,ec='none'))
 ax.add_patch(Circle(c,R,fill=False,ec=INK,lw=2))
 # Separador fijo y paleta móvil unidos al alojamiento y al eje, respectivamente.
 rect(ax,3.89,.9,.22,1.55,fc=METAL)
 tt=np.deg2rad(angle);rr=np.array([.35,R-.04]);perp=np.array([-np.sin(tt),np.cos(tt)])*.09
 ends=[np.array(c)+r*np.array([np.cos(tt),np.sin(tt)]) for r in rr]
 ax.add_patch(Polygon([ends[0]+perp,ends[1]+perp,ends[1]-perp,ends[0]-perp],fc=TEAL,ec=INK,lw=1.0))
 ax.add_patch(Circle(c,.38,fc=METAL,ec=INK,lw=1.3))
 line(ax,[5.9,6.85],[2.8,2.8]);line(ax,[1.15,2.1],[2.8,2.8])
 text(ax,7.25,2.8,'A',fontsize=13,color=TEAL);text(ax,.75,2.8,'B',fontsize=13,color=GRAY)
 text(ax,5.13,1.75,r'$p_A$',fontsize=14,color=TEAL);text(ax,3.05,3.4,r'$p_B$',fontsize=14,color=GRAY)
 ax.add_patch(Arc(c,4.7,4.7,theta1=55,theta2=130,color=ORANGE,lw=1.8))
 end=np.array(c)+2.35*np.array([np.cos(np.deg2rad(130)),np.sin(np.deg2rad(130))])
 start=np.array(c)+2.35*np.array([np.cos(np.deg2rad(122)),np.sin(np.deg2rad(122))])
 arrow(ax,start,end,ORANGE,lw=1.8);text(ax,4.1,5.5,r'$\theta$',fontsize=17,color=ORANGE)
 leader(ax,'Paleta móvil',tuple(ends[1]),(7.0,4.5),fontsize=11)
 leader(ax,'Separador fijo',(4.,1.45),(6.5,.45),fontsize=11)
 save(fig,'giratorio')


def pinza():
 fig,ax=setup(7.5,4.8,xlim=(.7,8.4),ylim=(-.7,5.0))
 ax.add_patch(FancyBboxPatch((2.4,1.5),4.2,2.1,boxstyle='round,pad=0,rounding_size=.08',fc='#e7eff1',ec=INK,lw=1.5))
 text(ax,4.5,2.7,'Pistón y mecanismo\nde transmisión',fontsize=12)
 line(ax,[4.4,4.4],[3.6,4.4]);line(ax,[4.6,4.6],[3.6,4.4]);arrow(ax,(4.5,4.7),(4.5,3.9))
 text(ax,6.3,4.45,'Aire comprimido',fontsize=11,color=TEAL)
 # Mordazas paralelas en vista exterior funcional; el mecanismo no se representa en corte.
 ax.add_patch(Polygon([(2.8,1.5),(3.6,1.5),(3.6,-.05),(3.25,-.05),(3.25,.85),(2.8,.85)],fc=METAL,ec=INK,lw=1.3))
 ax.add_patch(Polygon([(5.4,1.5),(6.2,1.5),(6.2,.85),(5.75,.85),(5.75,-.05),(5.4,-.05)],fc=METAL,ec=INK,lw=1.3))
 rect(ax,3.65,.02,1.7,1.0,fc='#ead5af',ec=ORANGE)
 arrow(ax,(2.65,.5),(3.2,.5),ORANGE);arrow(ax,(6.35,.5),(5.8,.5),ORANGE)
 text(ax,4.5,-.4,'Pieza',fontsize=11,color=ORANGE)
 leader(ax,'Mordaza',(3.25,1.1),(1.3,1.15),fontsize=11)
 save(fig,'pinza')


if __name__=='__main__':
 cadena();cilindro(True);cilindro(False);valvula();ventosa();diafragma();giratorio();pinza()
 print('Ocho ilustraciones generadas: PNG recortados y fuentes SVG.')
