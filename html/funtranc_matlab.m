%% 1. Modelo físico y representación de estados
% Función de transferencia, convolución y estabilidad.
% Modelos de tiempo continuo.
% Requiere MATLAB y Control System Toolbox. No requiere Simulink.
clear; close all; clc;
m = 2;                 % kg
c = 4;                 % N*s/m
k = 50;                % N/m
F0 = 10;               % N
z0 = [0.08; -0.10];     % [posición en m; velocidad en m/s]
dt = 0.002;            % Paso de observación, no del modelo continuo
t = (0:dt:10)';

Am = [0 1; -k/m -c/m];
Bm = [0; 1/m];
Cm = [1 0];
Dm = 0;
sys = ss(Am,Bm,Cm,Dm);
G = tf(1,[m c k]);
alpha = c/(2*m);
wn = sqrt(k/m);
zeta = alpha/wn;
wd = sqrt(wn^2-alpha^2);
disp('Polos de G:'); disp(pole(G));
fprintf('Ganancia estática: %.6f m/N\n',dcgain(G));
fprintf('Estabilidad estricta: %d\n',isstable(sys));

%% 2. Respuesta libre, forzada y total
fStep = F0*ones(size(t));
xLibre = initial(sys,z0,t);
xForzada = lsim(sys,fStep,t,zeros(2,1));
xTotal = lsim(sys,fStep,t,z0);
xLibreAn = exp(-alpha*t).*(z0(1)*cos(wd*t) + ...
    (z0(2)+alpha*z0(1))/wd*sin(wd*t));
xForzadaAn = F0/k*(1-exp(-alpha*t).* ...
    (cos(wd*t)+alpha/wd*sin(wd*t)));
errSuperposicion = max(abs(xTotal-xLibre-xForzada));
errAnalitico = max(abs(xTotal-xLibreAn-xForzadaAn));
fprintf('Error de superposición: %.3e m\n',errSuperposicion);
fprintf('Error frente a la solución analítica: %.3e m\n', ...
    errAnalitico);

figure('Name','Libre, forzada y total');
plot(t,xLibre,'LineWidth',1.4); hold on;
plot(t,xForzada,'LineWidth',1.4);
plot(t,xTotal,'LineWidth',1.7);
yline(F0/k,'k:','Equilibrio'); grid on;
xlabel('Tiempo (s)'); ylabel('Posición (m)');
legend('Libre','Forzada con estado inicial nulo','Total', ...
    'Location','best');
xlim([0 8]);

%% 3. Respuesta al impulso
h = squeeze(impulse(G,t));
h = h(:);
hAn = exp(-alpha*t).*sin(wd*t)/(m*wd);
fprintf('Error de h(t): %.3e m/(N*s)\n',max(abs(h-hAn)));
figure('Name','Respuesta al impulso');
plot(t,h,'LineWidth',1.6); grid on;
xlabel('Tiempo (s)'); ylabel('h(t) [m/(N s)]'); xlim([0 8]);

%% 4. Pulso de fuerza y convolución numérica
uPulso = F0*double(t>=0.5 & t<1.5);
% Cada muestra de la fuerza se mantiene hasta la siguiente (ZOH).
xPulso = lsim(sys,uPulso,t,zeros(2,1),'zoh');
aux = dt*conv(h,uPulso);
xConv = aux(1:numel(t));

% Solución exacta como diferencia de dos respuestas al escalón.
escalon = @(r) (1/k)*(1-exp(-alpha*r).* ...
    (cos(wd*r)+alpha/wd*sin(wd*r)));
xPulsoAn = F0*(escalon(max(t-0.5,0))-escalon(max(t-1.5,0)));
fprintf('Error ZOH frente al pulso analítico: %.3e m\n', ...
    max(abs(xPulso-xPulsoAn)));
fprintf('Error de la suma de convolución: %.3e m\n', ...
    max(abs(xConv-xPulso)));

figure('Name','Respuesta al pulso');
plot(t,xPulso,'LineWidth',1.8); hold on;
plot(t,xConv,'--','LineWidth',1.3); grid on;
xlabel('Tiempo (s)'); ylabel('Posición (m)');
legend('Modelo continuo con entrada ZOH','Convolución aproximada');
xlim([0 8]);

% Una instantánea del integrando para t*=1.6 s.
tEstrella = 1.6;
tau = t(t<=2.3);
uTau = F0*double(tau>=0.5 & tau<1.5);
retardo = tEstrella-tau;
hInvertida = zeros(size(tau));
causal = retardo>=0;
hInvertida(causal) = exp(-alpha*retardo(causal)).* ...
    sin(wd*retardo(causal))/(m*wd);
producto = uTau.*hInvertida;
figure('Name','Construcción de la convolución');
tiledlayout(3,1);
nexttile; stairs(tau,uTau,'LineWidth',1.4); grid on;
ylabel('u(\tau) (N)');
nexttile; plot(tau,hInvertida,'LineWidth',1.4); grid on;
ylabel('h(t^*-\tau)');
nexttile; area(tau,producto); grid on;
xlabel('\tau (s)'); ylabel('Producto (m/s)');

%% 5. Estabilidad y criterio de Routh-Hurwitz
fprintf('\nEstabilidad al cambiar el amortiguamiento:\n');
valoresC = [4 0 -2];
figure('Name','Polos y estabilidad'); hold on;
for j = 1:numel(valoresC)
    Gj = tf(1,[m valoresC(j) k]);
    pj = pole(Gj);
    plot(real(pj),imag(pj),'x','MarkerSize',10,'LineWidth',1.7, ...
        'DisplayName',sprintf('c = %g N s/m',valoresC(j)));
    fprintf('c=%g: isstable=%d\n',valoresC(j),isstable(Gj));
end
xline(0,'k:'); yline(0,'k:'); grid on;
xlabel('Parte real (1/s)'); ylabel('Parte imaginaria (rad/s)');
legend('Location','best');

% p(s)=s^3+3s^2+2s+K es Hurwitz exactamente para 0<K<6.
for K = [1 6 8]
    fprintf('\nK=%g, raíces del polinomio:\n',K);
    disp(roots([1 3 2 K]));
end

%% 6. Valor final y respuesta sinusoidal permanente
xInf = F0*dcgain(G);
zEq = -Am\(Bm*F0);
info = stepinfo(G);    % Escalón unitario, estado inicial nulo
fprintf('\nx(infinito) = %.4f m\n',xInf);
fprintf('Equilibrio [posición; velocidad]:\n'); disp(zEq);
fprintf('Sobreimpulso: %.2f %%\n',info.Overshoot);
fprintf('Establecimiento al 2 %%: %.3f s\n',info.SettlingTime);

Au = 5;               % Amplitud de fuerza, N
Omega = 3;            % rad/s
uSen = Au*sin(Omega*t);
Gj = squeeze(freqresp(G,Omega));
amplitud = Au*abs(Gj);
fase = angle(Gj);
xPermanente = amplitud*sin(Omega*t+fase);
xSen = lsim(sys,uSen,t,z0,'foh');
fprintf('Amplitud permanente: %.6f m\n',amplitud);
fprintf('Fase: %.4f grados\n',rad2deg(fase));
figure('Name','Estado estable sinusoidal');
plot(t,xSen,'LineWidth',1.6); hold on;
plot(t,xPermanente,'--','LineWidth',1.4); grid on;
xlabel('Tiempo (s)'); ylabel('Posición (m)');
legend('Respuesta total','Respuesta permanente sinusoidal');

% Una rampa no tiene por qué producir un valor final constante.
aRampa = 2;           % N/s
xRampa = lsim(sys,aRampa*t,t,zeros(2,1),'foh');
xRampaAsintotica = aRampa/k*t-aRampa*c/k^2;
figure('Name','Régimen de una rampa');
plot(t,xRampa,'LineWidth',1.5); hold on;
plot(t,xRampaAsintotica,'--','LineWidth',1.4); grid on;
xlabel('Tiempo (s)'); ylabel('Posición (m)');
legend('Respuesta desde reposo','Régimen asintótico');

%% 7. Resonancia y estabilidad BIBO
tr = (0:dt:20)';
ur = sin(wn*tr);       % Fuerza de amplitud 1 N, acotada
GsinAmort = tf(1,[m 0 k]);
xResonante = lsim(GsinAmort,ur,tr,'foh');
xAmortiguada = lsim(G,ur,tr,'foh');
xResonanteAn = sin(wn*tr)/(2*m*wn^2) ...
    - tr.*cos(wn*tr)/(2*m*wn);
fprintf('Error en resonancia por interpolación: %.3e m\n', ...
    max(abs(xResonante-xResonanteAn)));
figure('Name','Una entrada acotada puede producir resonancia');
plot(tr,xResonante,'LineWidth',1.4); hold on;
plot(tr,xAmortiguada,'LineWidth',1.4); grid on;
xlabel('Tiempo (s)'); ylabel('Posición (m)');
legend('Sin amortiguamiento','Con c = 4 N s/m');

%% 8. Un modo interno que no aparece en la transferencia reducida
Ah = [1 0; 0 -2]; Bh = [0; 1]; Ch = [1 1]; Dh = 0;
sysOculto = ss(Ah,Bh,Ch,Dh);
Gred = minreal(tf(sysOculto),1e-9);
disp('Transferencia reducida:'); disp(Gred);
fprintf('Transferencia reducida estable: %d\n',isstable(Gred));
disp('Autovalores internos:'); disp(eig(Ah));
% Con entrada cero y estado inicial [1;0], la salida es exp(t).
% minreal no debe usarse como prueba de estabilidad interna.

%% 9. Motor de CD con tensión y par de carga como entradas
R = 2; L = 0.01; J = 0.002; b = 0.02; Kt = 0.1; Ke = 0.1;
denMotor = [L*J L*b+R*J R*b+Ke*Kt];
Gomega = tf(Kt,denMotor);
Gtau = tf([-L -R],denMotor);
Gmotor = [Gomega Gtau];
tm = (0:0.0005:1.2)';
Vm = 12; tau0 = 0.1;
entradas = [Vm*ones(size(tm)), tau0*double(tm>=0.35)];
omega = lsim(Gmotor,entradas,tm,'zoh');
omegaSinCarga = Vm*dcgain(Gomega);
omegaConCarga = Vm*dcgain(Gomega)+tau0*dcgain(Gtau);
fprintf('\nVelocidad sin carga: %.3f rad/s\n',omegaSinCarga);
fprintf('Velocidad con carga: %.3f rad/s\n',omegaConCarga);
disp('Polos de velocidad:'); disp(pole(Gomega));

figure('Name','Motor de CD');
plot(tm,omega,'LineWidth',1.7); hold on;
yline(omegaSinCarga,':','Sin carga');
yline(omegaConCarga,'--','Con carga');
xline(0.35,':','Se aplica la carga'); grid on;
xlabel('Tiempo (s)'); ylabel('Velocidad angular (rad/s)');

% Para posición angular aparece un integrador adicional.
Gtheta = Gomega*tf(1,[1 0]);
fprintf('Transferencia tensión-posición BIBO estable: %d\n', ...
    isstable(Gtheta));
