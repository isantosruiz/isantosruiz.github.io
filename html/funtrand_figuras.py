"""Figuras originales de funtrand.html y comprobación de las recurrencias.
Las secuencias son ejemplos calculados, no mediciones experimentales.
"""
from pathlib import Path
import io
import json
import numpy as np
from scipy.signal import lfilter
from scipy.integrate import cumulative_trapezoid
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyBboxPatch, Polygon
from matplotlib.lines import Line2D
from PIL import Image, ImageChops

OUT=Path(__file__).resolve().parent
INK,TEAL,BLUE,ORANGE,GRAY,RED='#263f50','#197b80','#426da6','#b9752c','#71808a','#b65358'
Ts=.1;bM=np.ones(3)/3;bT=Ts/2*np.ones(2)
TEXT_SIZE=12
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':TEXT_SIZE,
    'axes.labelsize':TEXT_SIZE,'axes.titlesize':TEXT_SIZE,
    'xtick.labelsize':TEXT_SIZE,'ytick.labelsize':TEXT_SIZE,
    'legend.fontsize':TEXT_SIZE,'legend.title_fontsize':TEXT_SIZE,
    'mathtext.fontset':'stix','figure.facecolor':'white',
    'axes.labelcolor':INK,'text.color':INK,'axes.edgecolor':GRAY,
    'xtick.color':GRAY,'ytick.color':GRAY,'axes.spines.top':False,
    'axes.spines.right':False,'legend.frameon':False})


def save(fig,name):
    buf=io.BytesIO();fig.savefig(buf,format='png',dpi=245,bbox_inches='tight',pad_inches=.035,facecolor='white')
    buf.seek(0);im=Image.open(buf).convert('RGB')
    d=ImageChops.difference(im,Image.new('RGB',im.size,'white'))
    box=d.convert('L').point(lambda v:255 if v>12 else 0).getbbox();assert box
    im.crop((0,max(0,box[1]-3),im.width,min(im.height,box[3]+3))).save(OUT/f'funtrand-{name}.png',optimize=True)
    plt.close(fig)


def stem(ax,k,y,color=TEAL,marker='o',label=None):
    markerline,stemlines,baseline=ax.stem(k,y,linefmt='-',markerfmt=marker,basefmt=' ')
    plt.setp(markerline,color=color,markersize=5,markerfacecolor=color if marker=='o' else 'white',label=label)
    plt.setp(stemlines,color=color,linewidth=1.3,alpha=.85)
    ax.axhline(0,color=GRAY,lw=.7);ax.grid(alpha=.17)
    return markerline


def delta(k):return (np.asarray(k)==0).astype(float)


def descomposicion():
    k=np.arange(-2,7)
    seq=[2*delta(k),-delta(k-1),3*delta(k-2)]
    fig,axs=plt.subplots(4,1,figsize=(8.5,7.3),sharex=True)
    labels=[r'$2\delta[k]$',r'$-\delta[k-1]$',r'$3\delta[k-2]$',r'$u[k]$']
    for ax,y,col,lab in zip(axs,seq+[sum(seq)],[BLUE,ORANGE,TEAL,INK],labels):
        stem(ax,k,y,col);ax.set_ylabel(lab,rotation=0,labelpad=28)
        ax.set_ylim(min(-1.5,float(min(y))-.4),3.6)
    axs[-1].set(xticks=k,xlabel='Índice entero k',xlim=(-2.5,6.5))
    fig.subplots_adjust(hspace=.14);save(fig,'descomposicion')


def superposicion():
    k=np.arange(-2,8);h=lambda n:((n>=0)&(n<=2))/3
    seq=[2*h(k),-h(k-1),3*h(k-2)]
    fig,axs=plt.subplots(4,1,figsize=(8.5,7.3),sharex=True)
    labels=[r'$2h[k]$',r'$-h[k-1]$',r'$3h[k-2]$',r'$y[k]$']
    for ax,y,col,lab in zip(axs,seq+[sum(seq)],[BLUE,ORANGE,TEAL,INK],labels):
        stem(ax,k,y,col);ax.set_ylabel(lab,rotation=0,labelpad=28)
        ax.set_ylim(-.55,1.55)
    axs[-1].set(xticks=k,xlabel='Índice entero k',xlim=(-2.5,7.5))
    fig.subplots_adjust(hspace=.14);save(fig,'superposicion')


def convolucion():
    ell=np.arange(-2,8);u=2*delta(ell)-delta(ell-1)+3*delta(ell-2)
    hh=((3-ell>=0)&(3-ell<=2))/3;prod=u*hh
    fig,axs=plt.subplots(3,1,figsize=(8.5,6.3),sharex=True)
    stem(axs[0],ell,u,BLUE);axs[0].set_ylabel(r'$u[\ell]$')
    stem(axs[1],ell,hh,TEAL);axs[1].set_ylabel(r'$h[3-\ell]$')
    stem(axs[2],ell,prod,ORANGE);axs[2].set_ylabel('Producto')
    axs[2].text(4.2,.7,r'$y[3]=-\frac{1}{3}+1=\frac{2}{3}$')
    axs[-1].set(xticks=ell,xlabel=r'Índice de suma $\ell$',xlim=(-2.5,7.5))
    fig.subplots_adjust(hspace=.18);save(fig,'convolucion')


def text(ax,x,y,s,**kw):
    kw.setdefault('ha','center');kw.setdefault('va','center');kw.setdefault('color',INK)
    return ax.text(x,y,s,**kw)


def arrow(ax,a,b,color=INK,lw=1.4,**kw):
    return ax.annotate('',xy=b,xytext=a,arrowprops={'arrowstyle':'-|>','mutation_scale':12,'color':color,'lw':lw,**kw})


def block(ax,x,y,w,h,s):
    ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle='round,pad=.015,rounding_size=.04',fc='#eef5f3',ec=TEAL,lw=1.3))
    text(ax,x+w/2,y+h/2,s)


def promediador():
    fig,ax=plt.subplots(figsize=(9.5,4.7));ax.set(xlim=(-.5,13),ylim=(.1,5.1),aspect='equal');ax.axis('off')
    # Copiar una entrada a tres caminos y sumar sus salidas en puertos separados.
    arrow(ax,(-.25,2.6),(1.,2.6));text(ax,.15,3.1,r'$u[k]$')
    ax.plot([1,1],[1.,4.2],color=INK,lw=1.3)
    ax.plot(1.,2.6,'o',color=INK,ms=3)
    arrow(ax,(1.,4.2),(6.38,4.2),shrinkA=0)
    for y,delay in [(2.6,r'$z^{-1}$'),(1.,r'$z^{-2}$')]:
        arrow(ax,(1.,y),(2.48,y),shrinkA=0);block(ax,2.5,y-.45,1.8,.9,delay)
        arrow(ax,(4.32,y),(6.38,y))
    for y,label in [(4.2,r'$u[k]$'),(2.6,r'$u[k-1]$'),(1.,r'$u[k-2]$')]:
        ax.add_patch(Polygon([(6.4,y-.6),(6.4,y+.6),(7.6,y)],
            closed=True,fc='#eef5f3',ec=TEAL,lw=1.3))
        text(ax,6.83,y,r'$1/3$')
        text(ax,5.25,y+.48,label)
    ax.add_patch(Circle((10.2,2.6),.35,fc='white',ec=INK,lw=1.3))
    ax.plot([10.06,10.34],[2.6,2.6],color=INK,lw=1.3)
    ax.plot([10.2,10.2],[2.46,2.74],color=INK,lw=1.3)
    ax.plot([7.62,10.2,10.2],[4.2,4.2,3.25],color=INK,lw=1.3)
    arrow(ax,(10.2,3.25),(10.2,2.95))
    arrow(ax,(7.62,2.6),(9.85,2.6))
    ax.plot([7.62,10.2,10.2],[1.,1.,1.95],color=INK,lw=1.3)
    arrow(ax,(10.2,1.95),(10.2,2.25))
    arrow(ax,(10.55,2.6),(12.4,2.6));text(ax,11.8,3.1,r'$y[k]$')
    save(fig,'promediador')


def ma_respuestas():
    k=np.arange(9);d=delta(k);hm=lfilter(bM,[1],d);ym=lfilter(bM,[1],np.ones(len(k)))
    fig,axs=plt.subplots(2,1,figsize=(8.5,5.1),sharex=True)
    stem(axs[0],k,hm);axs[0].set_ylabel(r'$h_M[k]$')
    stem(axs[1],k,ym,BLUE);axs[1].set_ylabel('Escalón')
    axs[1].axhline(1,color=GRAY,lw=.9,ls=':')
    axs[-1].set(xticks=k,xlabel='Índice k',xlim=(-.4,8.4))
    fig.subplots_adjust(hspace=.18);save(fig,'ma-respuestas')


def ma_memoria():
    k=np.arange(9);libre=np.r_[2/3,4/3,np.zeros(7)]
    forced=lfilter(bM,[1],6*np.ones(9));total=libre+forced
    fig,ax=plt.subplots(figsize=(8.5,4.4))
    stem(ax,k,libre,BLUE,label='Libre');stem(ax,k,forced,ORANGE,marker='s',label='Forzada')
    stem(ax,k,total,TEAL,marker='x',label='Total')
    ax.set(xticks=k,xlabel='Índice k',ylabel='Salida',xlim=(-.4,8.4))
    ax.legend(loc='lower center',bbox_to_anchor=(.5,1.02),ncol=3)
    save(fig,'ma-memoria')


def ma_frecuencia():
    om=np.linspace(0,np.pi,901);H=(1+np.exp(-1j*om)+np.exp(-2j*om))/3
    fig,ax=plt.subplots(figsize=(8.6,4.1));ax.plot(om/np.pi,abs(H),color=TEAL,lw=2)
    ax.axvline(2/3,color=GRAY,lw=1,ls=':');ax.plot(2/3,0,'o',color=ORANGE,ms=5)
    ax.annotate(r'$\Omega=2\pi/3$',xy=(2/3,0),xytext=(.73,.25),
        arrowprops={'arrowstyle':'-','color':GRAY,'lw':.8})
    ax.set(xlabel=r'Frecuencia normalizada $\Omega/\pi$',ylabel=r'$|G_M(e^{j\Omega})|$',xlim=(0,1),ylim=(-.04,1.06))
    ax.grid(alpha=.2);save(fig,'ma-frecuencia')


def sensor():
    k=np.arange(61);t=k*Ts;om=np.pi/6;v=1+.4*np.sin(om*k)
    u=v+.25*np.sin(2*np.pi*k/3);y=lfilter(bM,[1],u)
    H=(1+np.exp(-1j*om)+np.exp(-2j*om))/3
    yr=1+.4*abs(H)*np.sin(om*k+np.angle(H))
    fig,axs=plt.subplots(2,1,figsize=(9,6.1),sharex=True)
    axs[0].plot(t,u,'.',color=BLUE,ms=5,label='Entrada sintética')
    axs[0].plot(t,v,'--',color=GRAY,lw=1.2,label='Componente nominal')
    axs[1].plot(t,y,'o',color=TEAL,ms=3.5,label='Promedio causal')
    axs[1].plot(t,yr,'--',color=ORANGE,lw=1.3,label='Régimen calculado')
    for ax in axs:
        ax.grid(alpha=.2);ax.set_ylabel('Velocidad (m/s)')
        ax.legend(loc='lower center',bbox_to_anchor=(.5,1.02),ncol=2)
    axs[1].set(xlabel='Tiempo (s)',xlim=(0,6));fig.subplots_adjust(hspace=.4)
    save(fig,'sensor')


def trapecio():
    fig,ax=plt.subplots(figsize=(8.4,4.7));t=np.array([.2,.3]);v=np.array([.4,.9])
    ax.add_patch(Polygon([(.2,0),(.2,.4),(.3,.9),(.3,0)],fc=TEAL,alpha=.15))
    ax.plot(t,v,color=TEAL,lw=2,marker='o')
    ax.vlines(t,0,v,color=GRAY,lw=1,ls=':')
    ax.annotate(r'$u[k-1]=0.4$',xy=(.2,.4),xytext=(.17,.65),
        arrowprops={'arrowstyle':'-','color':GRAY,'lw':.8})
    ax.annotate(r'$u[k]=0.9$',xy=(.3,.9),xytext=(.305,.95),
        arrowprops={'arrowstyle':'-','color':GRAY,'lw':.8})
    ax.text(.25,.22,r'$\Delta y=0.065\ \mathrm{m}$',ha='center',color=TEAL)
    ax.set(xlim=(.15,.35),ylim=(0,1.1),xlabel='Tiempo (s)',ylabel='Velocidad (m/s)')
    ax.set_xticks([.2,.3],['(k−1) Ts = 0.2','k Ts = 0.3']);ax.grid(alpha=.18)
    save(fig,'trapecio')


def integrador():
    k=np.arange(21);d=delta(k);ht=lfilter(bT,[1,-1],d)
    yt=lfilter(bT,[1,-1],np.ones(len(k)));yq=k*Ts
    fig,axs=plt.subplots(2,1,figsize=(8.8,6.2),sharex=True)
    stem(axs[0],k,ht,TEAL);axs[0].set_ylabel(r'$h_T[k]$ (s)')
    stem(axs[1],k,yt,TEAL,label='Estado interno nulo')
    stem(axs[1],k,yq,ORANGE,marker='x',label=r'Cuadratura con $y[0]=0$')
    axs[1].set_ylabel('Posición (m)')
    axs[1].legend(loc='lower center',bbox_to_anchor=(.5,1.02),ncol=2)
    axs[-1].set(xlabel='Índice k',xlim=(-.5,20.5),xticks=np.arange(0,21,2))
    fig.subplots_adjust(hspace=.38);save(fig,'integrador')


def polos():
    fig,ax=plt.subplots(figsize=(7,6.4));theta=np.linspace(0,2*np.pi,501)
    ax.add_patch(Circle((0,0),1,fc=TEAL,alpha=.045))
    ax.plot(np.cos(theta),np.sin(theta),color=GRAY,lw=1,ls=':')
    zm=np.exp(1j*np.array([2*np.pi/3,-2*np.pi/3]))
    ax.plot(zm.real,zm.imag,'o',ms=10,mfc='white',mec=BLUE,mew=1.8)
    ax.plot(0,0,'x',ms=10,mew=2,color=BLUE);ax.text(.08,.08,'×2',color=BLUE)
    ax.plot(-1,0,'o',ms=10,mfc='white',mec=ORANGE,mew=1.8)
    ax.plot(1,0,'x',ms=11,mew=2,color=ORANGE)
    ax.axhline(0,color=GRAY,lw=.7);ax.axvline(0,color=GRAY,lw=.7)
    handles=[Line2D([],[],marker='o',mfc='white',mec=BLUE,color='none',label='Ceros del promediador'),
       Line2D([],[],marker='x',color=BLUE,ls='none',label='Polos del promediador'),
       Line2D([],[],marker='o',mfc='white',mec=ORANGE,color='none',label='Cero del integrador'),
       Line2D([],[],marker='x',color=ORANGE,ls='none',label='Polo del integrador')]
    ax.legend(handles=handles,loc='lower center',bbox_to_anchor=(.5,1.02),ncol=2)
    ax.set(xlim=(-1.3,1.3),ylim=(-1.25,1.25),aspect='equal',xlabel=r'Parte real de $z$',ylabel=r'Parte imaginaria de $z$')
    ax.grid(alpha=.18);save(fig,'polos')


def deriva():
    k=np.arange(101);t=k*Ts;v=.6*np.cos(1.2*t);y0=.2
    q=y0+cumulative_trapezoid(v,t,initial=0);qb=y0+cumulative_trapezoid(v+.02,t,initial=0)
    tf=np.linspace(0,10,1001);real=y0+.5*np.sin(1.2*tf)
    fig,ax=plt.subplots(figsize=(9,4.7));ax.plot(tf,real,color=GRAY,lw=1.3,label='Integral analítica')
    ax.plot(t,q,'o',ms=3,mfc='white',mec=TEAL,label='Trapecios sin sesgo')
    ax.plot(t,qb,'.',ms=4,color=ORANGE,label='Con sesgo de 0.02 m/s')
    ax.set(xlabel='Tiempo (s)',ylabel='Posición (m)',xlim=(0,10));ax.grid(alpha=.18)
    ax.legend(loc='lower center',bbox_to_anchor=(.5,1.02),ncol=2)
    save(fig,'deriva')


def fuga():
    k=np.arange(81);t=k*Ts;lam=.5
    rho=(1-lam*Ts/2)/(1+lam*Ts/2);bf=(Ts/2)/(1+lam*Ts/2)
    ideal=lfilter(bT,[1,-1],np.ones(len(k)));leak=lfilter([bf,bf],[1,-rho],np.ones(len(k)))
    fig,ax=plt.subplots(figsize=(8.8,4.6))
    ax.plot(t,ideal,'o',ms=3,mfc='white',mec=TEAL,label='Integrador ideal')
    ax.plot(t,leak,'.',ms=4,color=ORANGE,label='Integración con fuga')
    ax.axhline(2,color=GRAY,lw=1,ls=':',label='Límite con fuga = 2 m')
    ax.set(xlabel='Tiempo (s)',ylabel='Salida (m)',xlim=(0,8));ax.grid(alpha=.18)
    ax.legend(loc='lower center',bbox_to_anchor=(.5,1.02),ncol=3)
    save(fig,'fuga')


def validar():
    out=np.convolve([2,-1,3],bM);assert np.allclose(out,np.array([2,1,4,2,3])/3)
    k=np.arange(101);t=k*Ts;u=.6*np.cos(1.2*t);y0=.2;w0=y0-Ts/2*u[0]
    yf=lfilter(bT,[1,-1],u,zi=[w0])[0];yq=y0+cumulative_trapezoid(u,t,initial=0)
    assert np.max(abs(yf-yq))<1e-12
    bias=y0+cumulative_trapezoid(u+.02,t,initial=0)
    assert np.max(abs(bias-yq-.02*t))<1e-12
    om=np.pi/6;H=(1+np.exp(-1j*om)+np.exp(-2j*om))/3
    print(json.dumps({'convolucion':out.tolist(),'ganancia_MA_pi_6':abs(H),
      'fase_MA_grados':np.angle(H)*180/np.pi,'w0':w0,
      'error_cuadratura_y_estado':float(np.max(abs(yf-yq))),
      'deriva_a_10s_m':float(bias[-1]-yq[-1]),
      'polo_fuga':(1-.5*Ts/2)/(1+.5*Ts/2)},indent=2))


if __name__=='__main__':
    validar()
    for draw in [descomposicion,superposicion,convolucion,promediador,
                 ma_respuestas,ma_memoria,ma_frecuencia,sensor,trapecio,
                 integrador,polos,deriva,fuga]:draw()
