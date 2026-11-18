"""Figuras complementarias de actuadoresm.html: actuación y ley de una leva."""
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

OUT=Path(__file__).resolve().parent
INK,TEAL,ORANGE,GRAY='#263f50','#197b80','#bd7129','#687b87'
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,'mathtext.fontset':'stix',
                     'figure.facecolor':'white','axes.spines.top':False,'axes.spines.right':False})
def save(fig,name):
 for ext in ['svg','png']:fig.savefig(OUT/f'actuadoresm-{name}.{ext}',bbox_inches='tight',pad_inches=.12,dpi=190,facecolor='white')
 plt.close(fig)

# Los sensores del motor y de la carga observan puntos diferentes de la cadena.
fig,ax=plt.subplots(figsize=(10,3.0),layout='constrained')
ax.set(xlim=(0,12),ylim=(-1.65,2.0));ax.axis('off')
boxes=[(.2,'Controlador'),(3.2,'Motor y\netapa de potencia'),(6.2,'Transmisión\nmecánica'),(9.2,'Carga\ny proceso')]
for x,t in boxes:
 ax.add_patch(FancyBboxPatch((x,.4),2.5,1.0,boxstyle='round,pad=.02,rounding_size=.06',facecolor='#eaf3f3',edgecolor=TEAL,lw=1.2))
 ax.text(x+1.25,.9,t,ha='center',va='center',color=INK,fontsize=11)
for x in [2.7,5.7,8.7]:ax.annotate('',xy=(x+.5,.9),xytext=(x,.9),arrowprops={'arrowstyle':'->','color':INK,'lw':1.3})
ax.text(1.45,1.72,'Consigna y comparación',ha='center',fontsize=10,color=GRAY)
ax.text(4.45,1.72,'Aporte de energía',ha='center',fontsize=10,color=GRAY)
ax.text(7.45,1.72,'Adaptación del movimiento',ha='center',fontsize=10,color=GRAY)
ax.text(10.45,1.72,'Magnitud de interés',ha='center',fontsize=10,color=GRAY)
ax.plot([10.45,10.45,1.45,1.45],[.4,-.65,-.65,.4],color=TEAL,lw=1.25)
ax.annotate('',xy=(1.45,.4),xytext=(1.45,-.05),arrowprops={'arrowstyle':'->','color':TEAL,'lw':1.25})
ax.text(6.1,-.97,'Sensor en la carga: posición, fuerza, presión u otra variable',ha='center',fontsize=10,color=TEAL)
ax.plot([4.45,4.45],[.4,-.14],color=ORANGE,lw=1.2)
ax.text(4.45,-.35,'Encoder del motor',ha='center',fontsize=9,color=ORANGE)
save(fig,'cadena')

# Ciclo 3–4–5: ascenso 120°, reposo 60°, retorno 120°, reposo 60°.
theta=np.linspace(0,360,1441);s=np.zeros_like(theta)
q=lambda u:10*u**3-15*u**4+6*u**5
up=(theta>=0)&(theta<120);high=(theta>=120)&(theta<180);down=(theta>=180)&(theta<300)
s[up]=q(theta[up]/120);s[high]=1;s[down]=1-q((theta[down]-180)/120)
assert abs(s[0])<1e-12 and abs(s[-1])<1e-12 and np.all((s>=-1e-12)&(s<=1+1e-12))
fig,ax=plt.subplots(figsize=(8.5,3.3),layout='constrained')
ax.plot(theta,s,color=TEAL,lw=2)
for lo,hi,txt in [(0,120,'Ascenso'),(120,180,'Reposo alto'),(180,300,'Descenso'),(300,360,'Reposo bajo')]:
 ax.axvspan(lo,hi,color=TEAL if 'Reposo' not in txt else ORANGE,alpha=.055)
 ax.text((lo+hi)/2,1.12,txt,ha='center',va='bottom',fontsize=10)
ax.set(xlim=(0,360),ylim=(-.08,1.3),xticks=[0,60,120,180,240,300,360],xlabel=r'Ángulo de la leva $\theta$ (°)',ylabel=r'Alzada relativa $s/h$')
ax.grid(alpha=.18);save(fig,'ciclo-leva')
print('Cadena de actuación y ciclo de leva generados y verificados.')
