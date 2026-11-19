"""Figuras originales y comprobación numérica de funtranc.html.

SciPy resuelve los mismos modelos continuos del archivo funtranc_matlab.m.
Las figuras son resultados del modelo, no registros experimentales.
"""
from pathlib import Path
import io
import json
import numpy as np
from scipy import signal
from scipy.integrate import quad
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, FancyBboxPatch
from PIL import Image, ImageChops

OUT=Path(__file__).resolve().parent
INK,TEAL,BLUE,ORANGE,GRAY,RED='#263f50','#197b80','#426da6','#b9752c','#71808a','#b65358'
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,
    'mathtext.fontset':'stix','figure.facecolor':'white',
    'axes.labelcolor':INK,'text.color':INK,'axes.edgecolor':GRAY,
    'xtick.color':GRAY,'ytick.color':GRAY,'axes.spines.top':False,
    'axes.spines.right':False,'legend.frameon':False,'lines.linewidth':1.8})

m,c,k=2.,4.,50.
F0=10.;dt=.002;t=np.arange(5001)*dt
z0=np.array([.08,-.10]);alpha=c/(2*m);wn=np.sqrt(k/m);wd=np.sqrt(wn**2-alpha**2)
A=np.array([[0,1],[-k/m,-c/m]]);B=np.array([[0],[1/m]]);C=np.array([[1,0]]);D=np.zeros((1,1))
sys=signal.StateSpace(A,B,C,D)


def text(ax,x,y,s,**kw):
    kw.setdefault('ha','center');kw.setdefault('va','center');kw.setdefault('color',INK)
    return ax.text(x,y,s,**kw)


def line(ax,x,y,color=INK,lw=1.5,**kw):return ax.plot(x,y,color=color,lw=lw,**kw)


def arrow(ax,a,b,color=TEAL,lw=1.6,**kw):
    return ax.annotate('',xy=b,xytext=a,
      arrowprops={'arrowstyle':'-|>','mutation_scale':12,'color':color,'lw':lw,**kw})


def setup(w=9,h=4,xlim=(0,11),ylim=(0,4.5)):
    fig,ax=plt.subplots(figsize=(w,h));ax.set(xlim=xlim,ylim=ylim,aspect='equal');ax.axis('off');return fig,ax


def block(ax,x,y,w,h,label,fc='#eef5f3',fontsize=12):
    ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle='round,pad=.02,rounding_size=.04',
                              fc=fc,ec=TEAL,lw=1.4))
    text(ax,x+w/2,y+h/2,label,fontsize=fontsize)


def plotsetup(w=9,h=4.6):
    fig,ax=plt.subplots(figsize=(w,h));ax.grid(alpha=.2);ax.set_xlabel('Tiempo (s)');return fig,ax


def save(fig,name):
    buf=io.BytesIO();fig.savefig(buf,format='png',dpi=240,bbox_inches='tight',pad_inches=.035,facecolor='white')
    buf.seek(0);im=Image.open(buf).convert('RGB')
    diff=ImageChops.difference(im,Image.new('RGB',im.size,'white'))
    box=diff.convert('L').point(lambda v:255 if v>12 else 0).getbbox();assert box
    im.crop((0,max(0,box[1]-3),im.width,min(im.height,box[3]+3))).save(OUT/f'funtranc-{name}.png',optimize=True)
    plt.close(fig)


def free(tt):
    return np.exp(-alpha*tt)*(z0[0]*np.cos(wd*tt)+(z0[1]+alpha*z0[0])/wd*np.sin(wd*tt))


def step(tt):
    tt=np.maximum(tt,0)
    return (1/k)*(1-np.exp(-alpha*tt)*(np.cos(wd*tt)+alpha/wd*np.sin(wd*tt)))


def h(tt):
    tt=np.asarray(tt);return np.where(tt>=0,np.exp(-alpha*np.maximum(tt,0))*np.sin(wd*np.maximum(tt,0))/(m*wd),0)


def mecanica():
    fig,ax=setup(9,4.1,xlim=(0,9),ylim=(0,4.25))
    # Resorte y amortiguador en paralelo, unidos a la misma masa.
    line(ax,[.8,.8],[.9,3.4],lw=2)
    for y in np.arange(1,3.5,.23):line(ax,[.55,.8],[y-.2,y],color=GRAY,lw=1)
    line(ax,[.8,1.2],[2.75,2.75])
    xx=np.linspace(1.2,3.65,19);yy=np.full_like(xx,2.75);yy[1:-1:2]+=.22;yy[2:-1:2]-=.22
    line(ax,xx,yy);line(ax,[3.65,4.15],[2.75,2.75])
    text(ax,2.45,3.3,r'$k$',fontsize=18)
    line(ax,[.8,2.],[1.65,1.65])
    line(ax,[2.,2.,3.1],[1.38,1.92,1.92]);line(ax,[2.,3.1],[1.38,1.38])
    line(ax,[2.65,2.65],[1.4,1.9]);line(ax,[2.65,4.15],[1.65,1.65])
    text(ax,2.55,1.02,r'$c$',fontsize=18)
    ax.add_patch(Rectangle((4.15,1.3),2.,1.8,fc='#eef2f5',ec=INK,lw=1.6))
    text(ax,5.15,2.25,r'$m$',fontsize=22)
    for x in [4.55,5.75]:ax.add_patch(Circle((x,1.15),.15,fc='white',ec=INK,lw=1.2))
    line(ax,[3.8,7.5],[1.,1.],color=GRAY,lw=1)
    arrow(ax,(6.18,2.3),(7.7,2.3),ORANGE,lw=2)
    text(ax,7.05,2.75,r'$f(t)$',fontsize=18,color=ORANGE)
    arrow(ax,(5.15,3.7),(7.15,3.7),TEAL,lw=1.7)
    line(ax,[5.15,5.15],[3.55,3.85],color=TEAL,lw=1)
    text(ax,6.18,4.07,r'$x(t)$',fontsize=18,color=TEAL)
    text(ax,5.8,.35,'Desplazamiento respecto al equilibrio',fontsize=11,color=GRAY)
    save(fig,'mecanica')


def descomposicion():
    fig,ax=setup(10,4.1,xlim=(-.3,13.8),ylim=(-.3,4.8))
    block(ax,2.7,.6,3.8,1.2,r'$G(s)$ · estado inicial nulo',fontsize=11)
    arrow(ax,(.1,1.2),(2.68,1.2),INK);text(ax,1.1,1.55,r'$u(t)$',fontsize=16)
    arrow(ax,(6.52,1.2),(9.75,1.2),INK);text(ax,8.,1.6,r'$y_{\mathrm{forzada}}(t)$',fontsize=15)
    block(ax,3.35,3.,5.1,1.1,r'Dinámica libre desde $\mathbf{z}_0$',fontsize=13)
    line(ax,[8.47,10.,10.],[3.55,3.55,1.45],color=GRAY,lw=1.4)
    arrow(ax,(10.,2.3),(10.,1.45),GRAY,lw=1.4)
    text(ax,11.42,2.75,r'$y_{\mathrm{libre}}(t)$',fontsize=15,color=GRAY)
    ax.add_patch(Circle((10.,1.2),.25,fc='white',ec=INK,lw=1.3))
    text(ax,10.,1.2,'+',fontsize=15)
    arrow(ax,(10.25,1.2),(13.1,1.2),INK)
    text(ax,12.2,1.65,r'$y(t)$',fontsize=17)
    save(fig,'descomposicion')


def respuestas():
    fig,ax=plotsetup()
    ax.plot(t,free(t),color=BLUE,label='Libre')
    ax.plot(t,F0*step(t),color=ORANGE,label='Forzada con estado inicial nulo')
    ax.plot(t,free(t)+F0*step(t),color=TEAL,lw=2.1,label='Total')
    ax.axhline(F0/k,color=GRAY,lw=1.1,ls=':',label='Equilibrio 0.20 m')
    ax.set(xlim=(0,8),ylabel='Posición (m)')
    ax.legend(loc='lower center',bbox_to_anchor=(.5,1.02),ncol=2,fontsize=9)
    save(fig,'respuestas')


def impulso():
    fig,ax=plotsetup(8.6,4.1);ax.plot(t,h(t),color=TEAL)
    ax.axhline(0,color=GRAY,lw=.7)
    ax.set(xlim=(0,8),ylabel=r'$h(t)$ [m/(N s)]')
    save(fig,'impulso')


def convolucion():
    tau=np.linspace(0,2.3,4601);ts=1.6
    u=F0*((tau>=.5)&(tau<1.5));kernel=h(ts-tau);prod=u*kernel
    fig,axes=plt.subplots(3,1,figsize=(9,7.0),sharex=True)
    axes[0].plot(tau,u,color=BLUE);axes[0].set(ylabel=r'$u(\tau)$ (N)',ylim=(-1,12))
    axes[1].plot(tau,kernel,color=TEAL);axes[1].set_ylabel(r'$h(t^*-\tau)$ [m/(N s)]')
    axes[2].plot(tau,prod,color=ORANGE,lw=1.5)
    axes[2].fill_between(tau,0,prod,where=prod>=0,color=TEAL,alpha=.22)
    axes[2].fill_between(tau,0,prod,where=prod<0,color=RED,alpha=.22)
    axes[2].set(ylabel='Producto (m/s)',xlabel=r'Instante de aplicación $\tau$ (s)',xlim=(0,2.3))
    for ax in axes:
        ax.grid(alpha=.2);ax.axvline(ts,color=GRAY,lw=1,ls=':')
    axes[0].text(ts+.03,10.2,r'$t^*=1.6$ s',fontsize=11,color=GRAY)
    fig.subplots_adjust(hspace=.15)
    save(fig,'convolucion')


def pulso():
    u=F0*((t>=.5)&(t<1.5));yp=signal.lsim(sys,u,t,interp=False)[1]
    yc=dt*np.convolve(h(t),u)[:len(t)]
    fig,ax=plotsetup()
    ax.plot(t,yp,color=TEAL,lw=2,label='Modelo continuo · entrada constante entre muestras')
    ax.plot(t,yc,color=ORANGE,lw=1.3,ls='--',label='Suma de convolución')
    ax.axvline(1.6,color=GRAY,lw=1,ls=':')
    p=F0*(step(1.6-.5)-step(1.6-1.5))
    ax.plot(1.6,p,'o',ms=4,color=INK)
    ax.annotate(r'$x(1.6)$',xy=(1.6,p),xytext=(2.5,.16),
        arrowprops={'arrowstyle':'-','color':GRAY,'lw':.8},fontsize=12)
    ax.axhline(0,color=GRAY,lw=.7);ax.set(xlim=(0,8),ylabel='Posición (m)')
    ax.legend(loc='lower center',bbox_to_anchor=(.5,1.02),fontsize=9)
    save(fig,'pulso')


def polos():
    fig,ax=plt.subplots(figsize=(8.6,5.1))
    ax.axvspan(-2,0,color=TEAL,alpha=.06);ax.axvspan(0,1.6,color=RED,alpha=.04)
    for cj,col,label in [(4,TEAL,'c = 4 N s/m · asintóticamente estable'),
                         (0,ORANGE,'c = 0 · oscilador no amortiguado'),
                         (-2,RED,'c = −2 N s/m · inestable')]:
        p=np.roots([m,cj,k]);ax.plot(p.real,p.imag,'x',ms=10,mew=2,color=col,label=label)
    ax.axvline(0,color=GRAY,ls=':',lw=1);ax.axhline(0,color=GRAY,lw=.8)
    ax.set(xlim=(-2,1.6),ylim=(-6.5,7.6),xlabel=r'Parte real $\sigma$ (s$^{-1}$)',
           ylabel=r'Parte imaginaria $\omega$ (rad/s)');ax.grid(alpha=.18)
    ax.legend(loc='upper center',fontsize=9)
    save(fig,'polos')


def resonancia():
    tr=np.arange(10001)*dt;u=np.sin(wn*tr)
    yr=signal.lsim(([1],[m,0,k]),u,tr)[1];yd=signal.lsim(sys,u,tr)[1]
    fig,ax=plotsetup(9.2,4.8)
    ax.plot(tr,yr,color=RED,lw=1.35,label='Sin amortiguamiento')
    ax.plot(tr,yd,color=TEAL,lw=1.5,label='Con c = 4 N s/m')
    env=tr/(2*m*wn)
    ax.plot(tr,env,color=GRAY,lw=1,ls=':');ax.plot(tr,-env,color=GRAY,lw=1,ls=':')
    ax.set(xlim=(0,20),ylabel='Posición (m)')
    ax.legend(loc='lower center',bbox_to_anchor=(.5,1.02),ncol=2,fontsize=10)
    save(fig,'resonancia')


def seno():
    om=3.;au=5.;u=au*np.sin(om*t)
    y=signal.lsim(sys,u,t,X0=z0)[1]
    gj=1/(k-m*om**2+1j*c*om);yss=au*abs(gj)*np.sin(om*t+np.angle(gj))
    fig,ax=plotsetup(9,4.5)
    ax.plot(t,y,color=TEAL,lw=1.9,label='Respuesta total')
    ax.plot(t,yss,color=ORANGE,lw=1.3,ls='--',label='Respuesta permanente sinusoidal')
    ax.set(xlim=(0,10),ylabel='Posición (m)')
    ax.legend(loc='lower center',bbox_to_anchor=(.5,1.02),ncol=2,fontsize=10)
    save(fig,'seno')


def motor_bloques():
    fig,ax=setup(11,4.6,xlim=(-.6,16.),ylim=(-1.5,4.3))
    # Tensión menos fuerza contraelectromotriz; par motor menos carga.
    for x in [1.,8.9]:
        ax.add_patch(Circle((x,1.5),.24,fc='white',ec=INK,lw=1.2));text(ax,x,1.5,'+',fontsize=14)
    block(ax,2.,.8,2.7,1.4,r'$\dfrac{1}{Ls+R}$',fontsize=17)
    block(ax,6.,.8,1.55,1.4,r'$K_t$',fontsize=18)
    block(ax,10.,.8,2.8,1.4,r'$\dfrac{1}{Js+b}$',fontsize=17)
    for x1,x2 in [(-.5,.76),(1.24,1.98),(4.72,5.98),(7.57,8.66),(9.14,9.98),(12.82,15.1)]:
        arrow(ax,(x1,1.5),(x2,1.5),INK,lw=1.3)
    text(ax,.1,2.05,r'$V(s)$',fontsize=16)
    text(ax,5.35,2.05,r'$I(s)$',fontsize=16)
    text(ax,8.1,2.05,r'$T_m(s)$',fontsize=16)
    text(ax,14.25,2.05,r'$\Omega(s)$',fontsize=16)
    line(ax,[8.9,8.9],[3.7,1.74],color=ORANGE,lw=1.4)
    arrow(ax,(8.9,2.7),(8.9,1.75),ORANGE,lw=1.4)
    text(ax,8.9,4.05,r'$T_L(s)$',fontsize=16,color=ORANGE)
    text(ax,9.25,2.1,'−',fontsize=15,color=ORANGE)
    block(ax,6.1,-1.05,1.5,.85,r'$K_e$',fontsize=17)
    line(ax,[13.8,13.8,7.62],[1.5,-.625,-.625],color=GRAY,lw=1.2)
    ax.add_patch(Circle((13.8,1.5),.045,fc=INK))
    line(ax,[6.08,1.,1.],[-.625,-.625,1.26],color=GRAY,lw=1.2)
    arrow(ax,(1.,.5),(1.,1.26),GRAY,lw=1.2)
    text(ax,1.4,.9,'−',fontsize=15,color=GRAY)
    save(fig,'motor-bloques')


def motor_respuesta():
    R,L,J,b,Kt,Ke=2.,.01,.002,.02,.1,.1
    am=np.array([[-R/L,-Ke/L],[Kt/J,-b/J]])
    bm=np.array([[1/L,0],[0,-1/J]])
    sm=signal.StateSpace(am,bm,[[0,1]],[[0,0]])
    tm=np.arange(2401)*.0005;u=np.column_stack((12*np.ones_like(tm),.1*(tm>=.35)))
    y=signal.lsim(sm,u,tm,interp=False)[1]
    fig,ax=plotsetup(9,4.3);ax.plot(tm,y,color=TEAL,lw=2)
    ax.axhline(24,color=GRAY,lw=1,ls=':',label='24 rad/s · sin carga')
    ax.axhline(20,color=ORANGE,lw=1,ls='--',label='20 rad/s · con carga')
    ax.axvline(.35,color=GRAY,lw=1,ls=':')
    ax.text(.365,7.,'Se aplica una carga\nde 0.1 N m',fontsize=10,color=GRAY)
    ax.set(xlim=(0,1.2),ylabel='Velocidad angular (rad/s)');ax.legend(loc='lower right',fontsize=10)
    save(fig,'motor-respuesta')


def validar():
    y0=signal.lsim(sys,np.zeros_like(t),t,X0=z0)[1]
    yz=signal.lsim(sys,np.full_like(t,F0),t)[1]
    yt=signal.lsim(sys,np.full_like(t,F0),t,X0=z0)[1]
    up=F0*((t>=.5)&(t<1.5));yp=signal.lsim(sys,up,t,interp=False)[1]
    ya=F0*(step(t-.5)-step(t-1.5));yc=dt*np.convolve(h(t),up)[:len(t)]
    errFree=float(np.max(abs(y0-free(t))));errStep=float(np.max(abs(yz-F0*step(t))))
    errSup=float(np.max(abs(yt-y0-yz)));errPulse=float(np.max(abs(yp-ya)))
    assert max(errFree,errStep,errSup,errPulse)<1e-10
    integral=quad(lambda tau:float(h(1.6-tau))*F0,.5,1.5,epsabs=1e-11)[0]
    assert abs(integral-F0*(step(1.1)-step(.1)))<1e-12
    om=3.;gj=1/(k-m*om**2+1j*c*om)
    tr=np.arange(10001)*dt;yr=signal.lsim(([1],[m,0,k]),np.sin(wn*tr),tr)[1]
    yrA=np.sin(wn*tr)/(2*m*wn**2)-tr*np.cos(wn*tr)/(2*m*wn)
    data={'error_libre':errFree,'error_escalon':errStep,'error_superposicion':errSup,
      'error_pulso_zoh':errPulse,'error_convolucion_dt_0002':float(np.max(abs(yc-yp))),
      'integral_t_16_m':float(integral),'amplitud_seno_m':float(5*abs(gj)),
      'fase_seno_grados':float(np.rad2deg(np.angle(gj))),
      'error_resonancia_interpolacion':float(np.max(abs(yr-yrA))),
      'sobreimpulso_pct':float(100*np.exp(-np.pi*.2/np.sqrt(1-.2**2))),
      'tiempo_pico_s':float(np.pi/wd),
      'polos_motor':[float(x) for x in np.roots([.00002,.0042,.05])]}
    print(json.dumps(data,indent=2))


if __name__=='__main__':
    validar()
    for draw in [mecanica,descomposicion,respuestas,impulso,convolucion,pulso,
                 polos,resonancia,seno,motor_bloques,motor_respuesta]:draw()
