"""Figuras de motor.html. Requiere NumPy, Matplotlib y Schemdraw 0.22.
Los esquemas usan símbolos de biblioteca con cuerpo de tamaño fijo.
Las curvas corresponden a modelos didácticos, no a mediciones.
"""
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import schemdraw
import schemdraw.elements as elm
from schemdraw.segments import SegmentArc, SegmentPoly

OUT=Path(__file__).resolve().parent
INK,TEAL,ORANGE,GRAY='#263f50','#197b80','#bd7129','#687b87'
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,'mathtext.fontset':'stix',
 'axes.spines.top':False,'axes.spines.right':False,'figure.facecolor':'white'})

def drawing():
 d=schemdraw.Drawing(show=False,backend='matplotlib')
 d.config(unit=2.4,inches_per_unit=.40,fontsize=11,font='DejaVu Sans',lw=1.25,color=INK)
 return d

def wire(d,a,b,**kw):return d.add(elm.Line(**kw).at(a).to(b).color(INK))
def node(d,p):d.add(elm.Dot(radius=.055).at(p))
def label(d,p,text,**kw):
 kw.setdefault('halign','center');kw.setdefault('valign','center')
 return d.add(elm.Label().at(p).right().label(text,loc='center',ofst=0,fontsize=kw.pop('fontsize',11),**kw))
def rail(d,p,text,up=True):
 d.add((elm.Vdd() if up else elm.Vss()).at(p).label(text,fontsize=11))
def gnd(d,p):d.add(elm.Ground().at(p))
def save_schematic(d,name):
 backend=d.draw(show=False);fig=backend.getfig()
 for ext in ['svg','png']:
  fig.savefig(OUT/f'{name}.{ext}',dpi=220,bbox_inches='tight',pad_inches=.12,
              facecolor='white',bbox_extra_artists=backend.ax.get_default_bbox_extra_artists())
 plt.close('all')
def save(fig,name):
 fig.savefig(OUT/f'{name}.png',dpi=190,bbox_inches='tight',facecolor='white')
 fig.savefig(OUT/f'{name}.svg',bbox_inches='tight',facecolor='white');plt.close(fig)


def esquema_modelo():
 d=drawing()
 d.add(elm.SourceV().at((0,0)).up().length(3));label(d,(-.9,1.5),r'$v_a$',fontsize=13)
 d.add(elm.ResistorIEC().at((0,3)).right().length(3));label(d,(1.5,3.65),r'$R_a$',fontsize=13)
 d.add(elm.Inductor2(loops=4).at((3,3)).right().length(3));label(d,(4.5,3.65),r'$L_a$',fontsize=13)
 wire(d,(6,3),(8,3))
 d.add(elm.SourceV().at((8,0)).up().length(3));label(d,(9.15,2.25),r'$e=K_e\omega$',fontsize=13)
 wire(d,(0,0),(8,0))
 d.add(elm.Arrow().at((.8,4.35)).right().length(1.4).label(r'$i_a$',loc='top').color(TEAL))
 # Cilindro con eje horizontal: las caras elípticas indican su volumen.
 rotor=elm.Element().at((0,0)).right()
 rx,ry,yc=.43,1.2,1.5
 left=np.linspace(np.pi/2,3*np.pi/2,60)
 right=np.linspace(-np.pi/2,np.pi/2,60)
 outline=[(11.1+rx*np.cos(t),yc+ry*np.sin(t)) for t in left]
 outline += [(13.3+rx*np.cos(t),yc+ry*np.sin(t)) for t in right]
 face=[(13.3+rx*np.cos(t),yc+ry*np.sin(t)) for t in np.linspace(0,2*np.pi,120)]
 rotor.segments.extend([
  SegmentPoly(outline,closed=True,fill='#f3f6f7',color=INK),
  SegmentPoly(face,closed=True,fill='#e4edef',color=INK),
  SegmentPoly([(13.3,1.43),(14.95,1.43),(14.95,1.57),(13.3,1.57)],
              closed=True,fill='#e4edef',color=INK),
  SegmentArc((14.55,yc),width=.9,height=1.85,theta1=-50,theta2=235,
             arrow='ccw',arrowlength=.22,arrowwidth=.16,color=TEAL,lw=1.6)
 ])
 d.add(rotor)
 label(d,(12.0,1.45),'Rotor\ny carga',fontsize=11)
 label(d,(12.2,-.4),r'$J,\ b,\ \tau_L$',fontsize=12)
 d.add(elm.Line().at((8.5,1.5)).to((10.67,1.5)).linestyle('--').color(GRAY))
 label(d,(14.55,2.7),r'$\omega$',fontsize=14,color=TEAL)
 label(d,(5.2,-1),r'$\tau_m=K_t i_a$',fontsize=13)
 save_schematic(d,'motor-modelo')


def esquema_pushpull():
 d=drawing()
 u=d.add(elm.Opamp().at((0,0)).right().flip())
 label(d,(1.1,-2.85),'U1\nOPA197',fontsize=11)
 # Las señales + y − se invierten verticalmente al voltear el símbolo.
 wire(d,(-3,.625),u.in2)
 d.add(elm.Dot(open=True).at((-3,.625)).label(r'$v_c$',loc='left'))
 minus=(-.8,-.625);wire(d,minus,u.in1);node(d,minus)
 d.add(elm.ResistorIEC().at(minus).to((-3,-.625)).label(r'$R_g$'+'\n10 kΩ',loc='bottom'))
 wire(d,(-3,-.625),(-3,-2));gnd(d,(-3,-2))
 # Alimentación del operacional, trazada hasta sus pines de potencia.
 top=max([u.vd,u.vs],key=lambda p:p.y);bottom=min([u.vd,u.vs],key=lambda p:p.y)
 wire(d,top,(top.x,1.45));rail(d,(top.x,1.45),'+9 V')
 wire(d,bottom,(bottom.x,-1.45));rail(d,(bottom.x,-1.45),'−9 V',False)
 wire(d,u.out,(3,0));node(d,(3,0))
 # Símbolos de cuerpo fijo; los cables se prolongan desde sus anclajes.
 q1=d.add(elm.BjtNpn(circle=True).at((7.248333333333333,3.5)).right())
 q2=d.add(elm.BjtPnp(circle=True).at((7.248333333333333,-3.5)).right())
 wire(d,q1.emitter,(8,1.5));wire(d,q2.emitter,(8,-1.5))
 label(d,(9.1,4.25),'Q1\nBD139 (NPN)',halign='left',fontsize=10)
 label(d,(9.1,-4.25),'Q2\nBD140 (PNP)',halign='left',fontsize=10)
 for q,y,name in [(q1,3.5,'Rb1'),(q2,-3.5,'Rb2')]:
  wire(d,(3,0),(3,y))
  d.add(elm.ResistorIEC().at((3,y)).to((5.5,y)).label(f'{name}\n100 Ω',loc='top' if y>0 else 'bottom'))
  wire(d,(5.5,y),q.base);node(d,(6,y))
 wire(d,q1.collector,(8,6.2));rail(d,(8,6.2),'+9 V')
 wire(d,q2.collector,(8,-6.2));rail(d,(8,-6.2),'−9 V',False)
 d.add(elm.ResistorIEC().at((8,1.5)).to((8,0)))
 d.add(elm.ResistorIEC().at((8,-1.5)).to((8,0)))
 label(d,(8.6,.75),'Re1\n0.47 Ω',halign='left',fontsize=10)
 label(d,(8.6,-.75),'Re2\n0.47 Ω',halign='left',fontsize=10)
 # D3: ánodo en emisor NPN y cátodo en base. D4: ánodo en base PNP.
 wire(d,(8,1.5),(6,1.5));node(d,(8,1.5))
 d.add(elm.Diode().at((6,1.5)).to((6,3.5)))
 label(d,(5.55,2.5),'D3\n1N4148',halign='right',fontsize=10)
 wire(d,(8,-1.5),(6,-1.5));node(d,(8,-1.5))
 d.add(elm.Diode().at((6,-3.5)).to((6,-1.5)))
 label(d,(5.55,-2.5),'D4\n1N4148',halign='right',fontsize=10)
 wire(d,(8,0),(15.5,0));node(d,(8,0));node(d,(11.6,0));node(d,(13.2,0))
 label(d,(14.2,.45),r'$v_a$',fontsize=13,color=TEAL)
 d.add(elm.Schottky().at((11.6,0)).to((11.6,6.2)))
 label(d,(12.1,3.1),'D1\nSS14',halign='left')
 rail(d,(11.6,6.2),'+9 V')
 d.add(elm.Schottky().at((11.6,-6.2)).to((11.6,0)))
 label(d,(12.1,-3.1),'D2\nSS14',halign='left')
 rail(d,(11.6,-6.2),'−9 V',False)
 m=d.add(elm.Motor().at((15.5,0)).down().length(3).label('M',loc='center',ofst=0))
 label(d,(16.4,-1.5),'M1',halign='left')
 wire(d,(15.5,-3),(15.5,-4));gnd(d,(15.5,-4))
 # Realimentación completa: no se deja como un terminal flotante.
 wire(d,(13.2,0),(13.2,-8))
 wire(d,(13.2,-8),(5,-8))
 d.add(elm.ResistorIEC().at((5,-8)).to((2.5,-8)).label(r'$R_f$'+' = 10 kΩ',loc='bottom'))
 wire(d,(2.5,-8),(-.8,-8));wire(d,(-.8,-8),minus)
 label(d,(7,-9.35),'Desacoplamiento de ambos rieles junto a U1 y a la etapa de potencia.',fontsize=10,color=GRAY)
 save_schematic(d,'motor-pushpull')


def esquema_mosfet():
 d=drawing()
 q=d.add(elm.NMos(diode=True,circle=True).at((6,0)).right())
 label(d,(7.15,-1),'Q1\nAO3400A',halign='left')
 wire(d,q.source,(6,-4));gnd(d,(6,-4))
 wire(d,(0,q.gate.y),(.5,q.gate.y))
 d.add(elm.Dot(open=True).at((0,q.gate.y)).label('GPIO25',loc='left'))
 d.add(elm.ResistorIEC().at((.5,q.gate.y)).to((2.9,q.gate.y)).label('Rg\n220 Ω',loc='top'))
 wire(d,(2.9,q.gate.y),q.gate);node(d,(3.65,q.gate.y))
 d.add(elm.ResistorIEC().at((3.65,q.gate.y)).to((3.65,-4)))
 label(d,(3.1,(q.gate.y-4)/2),'Rgs\n47 kΩ',halign='right')
 wire(d,(3.65,-4),(14,-4));node(d,(6,-4))
 wire(d,q.drain,(6,1.5));node(d,(6,.75))
 m=d.add(elm.Motor().at((6,4.5)).to((6,1.5)).label('M',loc='center',ofst=0))
 label(d,(5.1,3),'M1',halign='right')
 wire(d,(6,4.5),(6,5.5));wire(d,(6,5.5),(14,5.5));rail(d,(6,5.5),'+6 V')
 wire(d,(6,.75),(9,.75))
 d.add(elm.Schottky().at((9,.75)).to((9,5.5)))
 label(d,(8.5,3.125),'D1\nSS34',halign='right')
 node(d,(9,5.5))
 d.add(elm.Capacitor2(polar=True).at((11.5,5.5)).to((11.5,-4)))
 label(d,(11.0,-.1),'C1\n100 µF / 16 V',halign='right',fontsize=10)
 d.add(elm.Capacitor().at((14,5.5)).to((14,-4)))
 label(d,(14.6,.75),'C2\n100 nF',halign='left',fontsize=10)
 for x in [11.5,14]:node(d,(x,5.5));node(d,(x,-4))
 label(d,(7,-5.3),'GND común: ESP32, fuente y etapa de potencia.',fontsize=10,color=GRAY)
 save_schematic(d,'motor-mosfet')


def esquema_puente():
 d=drawing()
 for off,title,closed in [(0,'Giro positivo',{1,4}),(8.5,'Giro negativo',{2,3}),(17,'Frenado dinámico',{2,4})]:
  label(d,(off+2.75,6.6),title,fontsize=12)
  wire(d,(off,5),(off+5.5,5));rail(d,(off+2.75,5),r'$V_s$')
  wire(d,(off,0),(off+5.5,0));gnd(d,(off+2.75,0))
  for x,upper,lower in [(off,1,2),(off+5.5,3,4)]:
   for num,top,bottom in [(upper,5,2.5),(lower,2.5,0)]:
    sw=elm.Switch(nc=num in closed).at((x,top)).to((x,bottom)).color(TEAL if num in closed else INK)
    d.add(sw)
    label(d,(x-.6 if x==off else x+.6,(top+bottom)/2),f'S{num}',halign='right' if x==off else 'left',fontsize=10,color=TEAL if num in closed else INK)
   node(d,(x,2.5))
  m=d.add(elm.Motor().at((off,2.5)).to((off+5.5,2.5)).label('M',loc='center',ofst=0))
  label(d,(off+.9,2.95),'A',fontsize=10);label(d,(off+4.6,2.95),'B',fontsize=10)
  if closed=={1,4}:d.add(elm.Arrow().at((off+1.8,1.5)).to((off+3.7,1.5)).color(TEAL))
  if closed=={2,3}:d.add(elm.Arrow().at((off+3.7,1.5)).to((off+1.8,1.5)).color(TEAL))
  label(d,(off+2.75,-1.05),'Cerrados: '+', '.join('S'+str(x) for x in sorted(closed)),fontsize=10,color=TEAL)
 save_schematic(d,'motor-puente-h')


def esquema_modulo(alta=False):
 d=drawing();height=10 if alta else 8
 controls=[('PWM','PWM',25,.90),('INA','INA',26,.75),('INB','INB',27,.50),('ENA/DIAGA','ENA',32,.25),('ENB/DIAGB','ENB',33,.08)] if alta else [('PWMA','PWM',25,.84),('AIN1','INA',26,.69),('AIN2','INB',27,.54),('STBY','STBY',14,.39)]
 pins=[elm.IcPin(name=name,side='L',pos=pos,anchorname=anchor) for name,anchor,_,pos in controls]
 pins += [elm.IcPin(name='VDD' if alta else 'VCC',side='T',pos=.23,anchorname='VLOG'),elm.IcPin(name='VIN' if alta else 'VM',side='T',pos=.76,anchorname='VMOT'),elm.IcPin(name='GND',side='B',pos=.65,anchorname='GND')]
 pins += [elm.IcPin(name='OUTA' if alta else 'AO1',side='R',pos=.70,anchorname='OA'),elm.IcPin(name='OUTB' if alta else 'AO2',side='R',pos=.45,anchorname='OB')]
 if alta:
  pins += [elm.IcPin(name=n,side='R',pos=pos,anchorname=n) for n,pos in [('CS',.25),('CS_DIS',.13),('VOUT',.02)]]
 else:
  pins += [elm.IcPin(name=n,side='L',pos=pos,anchorname=n) for n,pos in [('BIN1',.23),('BIN2',.13),('PWMB',.03)]]
  pins += [elm.IcPin(name=n,side='R',pos=pos,anchorname=n) for n,pos in [('BO1',.23),('BO2',.10)]]
 ic=d.add(elm.Ic(size=(6.5,height),pins=pins,leadlen=.5,lsize=10).at((6,0)).right())
 label(d,(9.25,height-.9),'VNH5019 · #1451' if alta else 'TB6612FNG · #713',fontsize=11)
 label(d,(2.0,height+.7),'ESP32',fontsize=12)
 for name,anchor,gpio,pos in controls:
  p=getattr(ic,anchor)
  wire(d,(0,p.y),p)
  d.add(elm.Dot(open=True).at((0,p.y)))
  label(d,(0,p.y+.23),f'GPIO{gpio}',halign='left',fontsize=10,color=TEAL)
 # Resistencias reales de estado inicial, no solo una nota dentro del bloque.
 if alta:
  for anchor,x,number in [('INA',1.65,1),('INB',3.9,2)]:
   p=getattr(ic,anchor);node(d,(x,p.y))
   wire(d,(x,p.y),(x,p.y-.4))
   d.add(elm.ResistorIEC().at((x,p.y-.4)).to((x,p.y-1.7)))
   label(d,(x+.4,p.y-1.05),f'R{number}\n10 kΩ',halign='left',fontsize=9)
   d.add(elm.Ground(lead=False).at((x,p.y-1.7)))
  label(d,(2.2,-.15),'GPIO32 y GPIO33\nDrenador abierto',fontsize=10,color=GRAY)
 else:
  for anchor in ['BIN1','BIN2','PWMB']:
   p=getattr(ic,anchor);wire(d,(4.3,p.y),p);node(d,(4.3,p.y))
  wire(d,(4.3,ic.BIN1.y),(4.3,-2));wire(d,(4.3,-2),(18.8,-2))
 for anchor in (['CS','CS_DIS','VOUT'] if alta else ['BO1','BO2']):
  p=getattr(ic,anchor);d.add(elm.NoConnect().at(p))
 # Alimentación lógica separada de la del motor.
 p=ic.VLOG;wire(d,p,(p.x,height+1.25));rail(d,(p.x,height+1.25),'3V3')
 p=ic.VMOT;wire(d,p,(p.x,height+1.25));wire(d,(p.x,height+1.25),(20.8,height+1.25))
 rail(d,(p.x,height+1.25),'+12 V' if alta else '+6 V')
 wire(d,ic.GND,(ic.GND.x,-2));wire(d,(ic.GND.x,-2),(20.8,-2));gnd(d,(14,-2))
 for x in [18.5,20.8]:
  cap=elm.Capacitor2(polar=True) if x==18.5 else elm.Capacitor()
  d.add(cap.at((x,height+1.25)).to((x,-2)))
  label(d,(x-.6 if x==18.5 else x+.6,(height+1.25-2)/2),'C1\nReserva' if x==18.5 else 'C2\n100 nF',halign='right' if x==18.5 else 'left',fontsize=10)
  node(d,(x,height+1.25));node(d,(x,-2))
 # Salida diferencial: ninguna conexión del motor a GND.
 wire(d,ic.OA,(15.5,ic.OA.y));wire(d,ic.OB,(15.5,ic.OB.y))
 m=d.add(elm.Motor().at((15.5,ic.OA.y)).to((15.5,ic.OB.y)).label('M',loc='center',ofst=0))
 label(d,(16.4,(ic.OA.y+ic.OB.y)/2),'M1',halign='left',fontsize=10)
 label(d,(12,-3.25),'Fuente del motor externa al USB · GND común con el ESP32',fontsize=10,color=GRAY)
 save_schematic(d,'motor-vnh5019' if alta else 'motor-tb6612')


def generar_esquemas():
 esquema_modelo();esquema_pushpull();esquema_mosfet();esquema_puente()
 esquema_modulo();esquema_modulo(True)

# Solo se regeneran las gráficas si se ejecuta el archivo completo.
if __name__=='__main__':
 generar_esquemas()

 # 3. Tensiones PWM idealizadas y corriente de armadura en regimen periodico.
 f,axes=plt.subplots(3,2,figsize=(11.8,7.6),constrained_layout=True)
 for row,d in enumerate([.25,.5,.75]):
  t=np.linspace(0,150e-6,3001);v=6*((t*20000)%1<d)
  axes[row,0].plot(t*1e6,v,color=TEAL,lw=1.8);axes[row,0].axhline(6*d,color=ORANGE,ls='--',lw=1.3)
  axes[row,0].set(ylim=(-.5,7.4),ylabel='Tensión (V)',title=f'Ciclo de trabajo D = {d:.0%} · promedio ideal {6*d:g} V')
  axes[row,0].grid(alpha=.16);axes[row,0].set_yticks([0,3,6])
  if row==2:axes[row,0].set_xlabel('Tiempo (µs)')
  # Modelo de diodo ideal, R=4ohm, L=1mH, e=2V. Se recorta i >= 0.
  dt=1e-7;steps=int(.02/dt);i=0.;xs=[];ys=[]
  for k in range(steps):
   t0=k*dt;on=k % 500 < round(d*500);voltage=6 if on else 0
   i=max(0.,i+dt*(voltage-4*i-2)/.001)
   if k>=steps-1500:xs.append((k-(steps-1500))*dt*1e6);ys.append(i)
  axes[row,1].plot(xs,ys,color=TEAL,lw=1.8)
  axes[row,1].axhline(np.mean(ys),color=ORANGE,ls='--',lw=1.3)
  axes[row,1].set(ylabel='Corriente (A)',title='Corriente calculada · R = 4 Ω, L = 1 mH, e = 2 V')
  axes[row,1].grid(alpha=.16)
  if row==2:axes[row,1].set_xlabel('Tiempo (µs)')
 save(f,'motor-pwm')


 # 8. Perturbacion de carga con modelo promediado y regulador PI.
 R,L,Ke,Kt,J,b,Vs=2.,.002,.04,.04,.0002,.00002,12.
 w0=Kt*(.5*Vs)/(R*b+Kt*Ke);i0=b*w0/Kt
 Kp,Ki=.006,.08;dt=2e-5;T=2.5;N=int(T/dt)+1
 t=np.arange(N)*dt;states=np.array([[i0,w0],[i0,w0]],float);z=0.;history=np.zeros((N,6))
 for k,tk in enumerate(t):
  load=.02 if tk>=1 else 0.
  error=w0-states[1,1];raw=.5+Kp*error+Ki*z;duty=np.clip(raw,0,1)
  if 0<raw<1 or (raw>=1 and error<0) or (raw<=0 and error>0):z+=error*dt
  history[k]=[states[0,1],states[1,1],.5,duty,states[0,0],states[1,0]]
  for j,d in enumerate([.5,duty]):
   i,w=states[j];di=(d*Vs-R*i-Ke*w)/L;dw=(Kt*i-b*w-load)/J
   states[j]+=[dt*di,dt*dw]
 f,axes=plt.subplots(2,1,figsize=(10.8,7.0),sharex=True,constrained_layout=True)
 for ax in axes:ax.axvline(1,color=GRAY,ls=':',lw=1.4);ax.grid(alpha=.18)
 axes[0].plot(t,history[:,0]*60/(2*np.pi),color=ORANGE,label='Mando fijo, D = 0.5')
 axes[0].plot(t,history[:,1]*60/(2*np.pi),color=TEAL,label='PI de velocidad (simulado)')
 axes[0].axhline(w0*60/(2*np.pi),color=GRAY,ls='--',lw=1,label='Velocidad de referencia')
 axes[0].set(ylabel='Velocidad (rpm)',title='La misma perturbación de carga, dos formas de responder');axes[0].legend(frameon=False,loc='lower left')
 axes[1].plot(t,history[:,2],color=ORANGE);axes[1].plot(t,history[:,3],color=TEAL)
 axes[1].set(ylabel='Ciclo de trabajo D',xlabel='Tiempo (s)',ylim=(.47,.64))
 axes[1].annotate('Carga adicional de 0.02 N·m',xy=(1,.61),xytext=(1.18,.623),arrowprops=dict(arrowstyle='->',color=GRAY),fontsize=10)
 save(f,'motor-respuesta')
 print('Ocho figuras exportadas en PNG y SVG.')
 print(f'Modelo: velocidad inicial {w0:.6f} rad/s; corriente inicial {i0:.6f} A.')
 print(f'Velocidades finales: mando fijo {history[-1,0]:.6f}; PI {history[-1,1]:.6f} rad/s.')
