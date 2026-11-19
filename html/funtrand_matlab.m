%% 1. Muestras e impulsos desplazados
% Función de transferencia y respuesta en tiempo discreto.
% Los modelos requieren Control System Toolbox.
% No requiere Signal Processing Toolbox ni Simulink.
clear; close all; clc;
Ts = 0.1;                    % s
k = (-2:7)';
delta = @(n) double(n==0);
uEjemplo = 2*delta(k)-delta(k-1)+3*delta(k-2);
componentes = [2*delta(k), -delta(k-1), 3*delta(k-2)];
assert(max(abs(uEjemplo-sum(componentes,2)))<1e-14);
figure('Name','Una secuencia como suma de impulsos');
tiledlayout(4,1);
for j = 1:3
    nexttile; stem(k,componentes(:,j),'filled'); grid on;
    ylabel(sprintf('Componente %d',j));
end
nexttile; stem(k,uEjemplo,'filled'); grid on;
xlabel('Índice k'); ylabel('u[k]');
%% 2. Convolución, recurrencia y filtro causal
bM = [1 1 1]/3; aM = 1;
uCorto = [2; -1; 3];
hM = bM(:);
yConv = conv(uCorto,hM);
% Añadir dos ceros permite observar la cola completa del FIR.
uExtendida = [uCorto; zeros(2,1)];
yFilter = filter(bM,aM,uExtendida);
yRec = zeros(size(uExtendida));
uPrev1 = 0; uPrev2 = 0;
for j = 1:numel(uExtendida)
    actual = uExtendida(j);
    yRec(j) = (actual+uPrev1+uPrev2)/3;
    uPrev2 = uPrev1; uPrev1 = actual;
end
yEsperada = [2;1;4;2;3]/3;
assert(max(abs(yConv-yEsperada))<1e-14);
assert(max(abs(yConv-yFilter))<1e-14);
assert(max(abs(yConv-yRec))<1e-14);
disp('Convolución completa:'); disp(yConv.');
figure('Name','Salida del promediador');
stem((0:numel(yConv)-1)',yConv,'filled'); grid on;
xlabel('Índice k'); ylabel('y[k]');

% Las respuestas a impulsos desplazados también se superponen.
hIndice = @(n) double(n>=0 & n<=2)/3;
respuestas = [2*hIndice(k),-hIndice(k-1),3*hIndice(k-2)];
figure('Name','Superposición de las respuestas');
tiledlayout(4,1);
for j = 1:3
    nexttile; stem(k,respuestas(:,j),'filled'); grid on;
    ylabel(sprintf('Aportación %d',j));
end
nexttile; stem(k,sum(respuestas,2),'filled'); grid on;
xlabel('Índice k'); ylabel('y[k]');

% Invertir y desplazar h como función del índice de suma.
ell = k; indiceSalida = 3;
uEll = 2*delta(ell)-delta(ell-1)+3*delta(ell-2);
hDesplazada = hIndice(indiceSalida-ell);
productos = uEll.*hDesplazada;
assert(abs(sum(productos)-2/3)<1e-14);
figure('Name','Construcción de y[3] por convolución');
tiledlayout(3,1);
nexttile; stem(ell,uEll,'filled'); grid on; ylabel('u[l]');
nexttile; stem(ell,hDesplazada,'filled'); grid on;
ylabel('h[3-l]');
nexttile; stem(ell,productos,'filled'); grid on;
xlabel('Índice de suma l'); ylabel('Producto');
%% 3. Modelos en z y normalización del impulso
% tf usa aquí potencias descendentes de z.
GM = tf([1 1 1],[3 0 0],Ts);
beta = Ts/2;
bT = beta*[1 1]; aT = [1 -1];
GT = tf(bT,aT,Ts);
AM = [0 0; 1 0]; BM = [1;0];
CM = [1 1]/3; DM = 1/3;
sysM = ss(AM,BM,CM,DM,Ts);
sysT = ss(1,Ts,1,beta,Ts);
kd = (0:12)'; td = kd*Ts;
delta0 = double(kd==0);
hMFiltro = filter(bM,aM,delta0);
hTFiltro = filter(bT,aT,delta0);
hMImp = Ts*squeeze(impulse(GM,td));
hTImp = Ts*squeeze(impulse(GT,td));
assert(max(abs(hMImp(:)-hMFiltro))<1e-12);
assert(max(abs(hTImp(:)-hTFiltro))<1e-12);
assert(max(abs(lsim(sysM,delta0,td)-hMFiltro))<1e-12);
assert(max(abs(lsim(sysT,delta0,td)-hTFiltro))<1e-12);
fprintf('Ganancia estática del promediador: %.6f\n',dcgain(GM));
fprintf('Promediador estable: %d\n',isstable(GM));
fprintf('Integrador ideal BIBO estable: %d\n',isstable(GT));
figure('Name','Impulso y escalón del promediador');
tiledlayout(2,1);
nexttile; stem(kd,hMFiltro,'filled'); grid on; ylabel('h_M[k]');
nexttile; stem(kd,filter(bM,aM,ones(size(kd))),'filled');
grid on; xlabel('Índice k'); ylabel('Escalón');
%% 4. Estado inicial y superposición en el promediador
km = (0:8)'; tm = km*Ts;
memoria0 = [4;-2];             % [u[-1]; u[-2]]
entradaM = 6*ones(size(km));
yLibreM = initial(sysM,memoria0,tm);
yForzadaM = lsim(sysM,entradaM,tm,zeros(2,1));
yTotalM = lsim(sysM,entradaM,tm,memoria0);
assert(max(abs(yTotalM-yLibreM-yForzadaM))<1e-12);
assert(max(abs(yLibreM-[2/3;4/3;zeros(7,1)]))<1e-12);
figure('Name','Memoria inicial del promediador');
stem(km,yLibreM,'filled'); hold on;
stem(km,yForzadaM,'o'); stem(km,yTotalM,'x'); grid on;
xlabel('Índice k'); ylabel('Salida');
legend('Libre','Forzada','Total','Location','best');
%% 5. Integrador trapezoidal y condición inicial física
ki = (0:100)'; ti = ki*Ts;
velocidad = 0.6*cos(1.2*ti);   % m/s
posicion0 = 0.2;              % m
w0 = posicion0-beta*velocidad(1);
yCeroEstado = filter(bT,aT,velocidad);
yCuadratura = posicion0+cumtrapz(ti,velocidad);
yEstado = lsim(sysT,velocidad,ti,w0);
yFilterInicial = filter(bT,aT,velocidad,w0);
yLibreT = initial(sysT,w0,ti);
assert(max(abs(yCuadratura-yEstado))<1e-12);
assert(max(abs(yCuadratura-yFilterInicial))<1e-12);
assert(max(abs(yCuadratura-yCeroEstado-yLibreT))<1e-12);
fprintf('Estado inicial interno w[0]: %.6f m\n',w0);
fprintf('Posición inicial física y[0]: %.6f m\n',yEstado(1));

% Recurrencia de cuadratura: y[0] está fijada antes del primer paso.
yRecT = zeros(size(ti)); yRecT(1) = posicion0;
for j = 2:numel(ti)
    yRecT(j) = yRecT(j-1) ...
        + beta*(velocidad(j)+velocidad(j-1));
end
assert(max(abs(yRecT-yCuadratura))<1e-12);
figure('Name','Respuesta del integrador a un escalón');
kiCorto = (0:20)'; tiCorto = kiCorto*Ts;
escalon = ones(size(kiCorto));
yEscalonT = filter(bT,aT,escalon);
yDesdeCero = cumtrapz(tiCorto,escalon);
stem(kiCorto,yEscalonT,'o'); hold on;
stem(kiCorto,yDesdeCero,'x'); grid on;
xlabel('Índice k'); ylabel('Posición (m)');
legend('Estado interno nulo','Cuadratura con y[0]=0');
%% 6. Respuesta en frecuencia y mediciones sintéticas
Omega = linspace(0,pi,501)';    % rad/muestra
HM = (1+exp(-1i*Omega)+exp(-2i*Omega))/3;
figure('Name','Ganancia del promediador');
plot(Omega/pi,abs(HM),'LineWidth',1.6); grid on;
xlabel('Frecuencia normalizada, Omega/pi'); ylabel('|G_M|');
xline(2/3,':','Cero en 2pi/3');

ks = (0:60)'; ts = ks*Ts;
Omega0 = pi/6;
nominal = 1+0.4*sin(Omega0*ks);
perturbacion = 0.25*sin(2*pi*ks/3);
medicion = nominal+perturbacion;
salidaM = filter(bM,aM,medicion);
H0 = (1+exp(-1i*Omega0)+exp(-2i*Omega0))/3;
regimenM = 1+0.4*abs(H0)*sin(Omega0*ks+angle(H0));
% evalfr recibe z; freqresp recibe frecuencia física en rad/s.
assert(abs(evalfr(GM,exp(1i*Omega0))-H0)<1e-12);
assert(abs(squeeze(freqresp(GM,Omega0/Ts))-H0)<1e-12);
assert(max(abs(salidaM(3:end)-regimenM(3:end)))<1e-12);
fprintf('Ganancia a pi/6: %.9f\n',abs(H0));
fprintf('Fase a pi/6: %.6f grados\n',rad2deg(angle(H0)));
figure('Name','Promediado de una señal sintética');
tiledlayout(2,1);
nexttile; plot(ts,medicion,'.',ts,nominal,'--'); grid on;
ylabel('Velocidad (m/s)'); legend('Entrada','Componente nominal');
nexttile; plot(ts,salidaM,'o',ts,regimenM,'--'); grid on;
xlabel('Tiempo (s)'); ylabel('Velocidad (m/s)');
legend('Promedio causal','Régimen calculado');
%% 7. Sesgo de velocidad y deriva de posición
sesgo = 0.02;                 % m/s
posicionAnalitica = posicion0+0.5*sin(1.2*ti);
estimacion = posicion0+cumtrapz(ti,velocidad+sesgo);
deriva = estimacion-yCuadratura;
assert(max(abs(deriva-sesgo*ti))<1e-12);
figure('Name','Deriva por sesgo en la medición');
plot(ti,posicionAnalitica,'k-',ti,yCuadratura,'o', ...
    ti,estimacion,'.'); grid on;
xlabel('Tiempo (s)'); ylabel('Posición (m)');
legend('Integral analítica','Trapecios sin sesgo','Con sesgo');
fprintf('Deriva por sesgo a 10 s: %.6f m\n',deriva(end));
%% 8. Estabilidad, criterio de Jury e integración con fuga
disp('Polos del promediador:'); disp(pole(GM));
disp('Ceros del promediador:'); disp(zero(GM));
disp('Polos del integrador:'); disp(pole(GT));
a1 = -1.2; a2 = 0.5;
condicionesJury = [1+a1+a2, 1-a1+a2, 1-a2];
assert(all(condicionesJury>0));
disp('Raíces del ejemplo cuadrático:'); disp(roots([1 a1 a2]));

lambda = 0.5;                % 1/s
rho = (1-lambda*Ts/2)/(1+lambda*Ts/2);
betaF = (Ts/2)/(1+lambda*Ts/2);
bF = betaF*[1 1]; aF = [1 -rho];
GF = tf(bF,aF,Ts);
assert(isstable(GF));
assert(abs(dcgain(GF)-1/lambda)<1e-12);
% Las transferencias coinciden con la discretización de Tustin.
GTdesdeS = c2d(tf(1,[1 0]),Ts,'tustin');
GFdesdeS = c2d(tf(1,[1 lambda]),Ts,'tustin');
assert(norm(minreal(GT-GTdesdeS,1e-10),inf)<1e-10);
assert(norm(minreal(GF-GFdesdeS,1e-10),inf)<1e-10);
kf = (0:80)'; tfis = kf*Ts;
uConstante = ones(size(kf));
yIdeal = filter(bT,aT,uConstante);
yFuga = filter(bF,aF,uConstante);
figure('Name','Acumulación ideal e integración con fuga');
plot(tfis,yIdeal,'o',tfis,yFuga,'.'); hold on;
yline(1/lambda,':','Límite con fuga'); grid on;
xlabel('Tiempo (s)'); ylabel('Salida (m)');
legend('Integrador ideal','Integración con fuga','Location','best');
fprintf('Polo con fuga: %.9f\n',rho);
fprintf('Ganancia estática con fuga: %.6f s\n',dcgain(GF));
%% 9. Procesamiento por bloques sin perder la memoria
corte = 25;
entradaBloques = medicion;
[primera,zFinal] = filter(bM,aM,entradaBloques(1:corte));
segunda = filter(bM,aM,entradaBloques(corte+1:end),zFinal);
salidaBloques = [primera; segunda];
assert(max(abs(salidaBloques-salidaM))<1e-12);
% zFinal es la memoria interna de filter, no el par de muestras.
fprintf('Error al procesar por bloques: %.3e\n', ...
    max(abs(salidaBloques-salidaM)));
disp('VALIDACION_FUNTRAND_COMPLETA');
