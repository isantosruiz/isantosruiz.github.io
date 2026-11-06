% Convolución, RC y mecanismo. Los modelos numéricos usan MATLAB básico.
clear

k = 0:15;
v = [1 1 1 zeros(1,13)];
h = 0.5.^k;
y = conv(v,h); y = y(1:numel(k));
assert(max(abs(y-filter(1,[1 -0.5],v))) < 1e-12);
figure; tiledlayout(3,1);
valores = {v,h,y};
titulos = {'Entrada v[k]','Respuesta al impulso h[k]', ...
           'Salida y[k] = (h * v)[k]'};
for j = 1:3
    nexttile; stem(k,valores{j},'filled');
    ylabel('Amplitud'); title(titulos{j}); grid on;
end
xlabel('Índice k');

% Circuito RC con tensión inicial no nula.
R = 1000; C = 100e-6; Ts = 0.02;
a = exp(-Ts/(R*C));
k = 0:30; t = k*Ts;
V0 = 1; Vin = 5;
vc = zeros(size(k)); vc(1) = V0;
for n = 1:numel(k)-1
    vc(n+1) = a*vc(n)+(1-a)*Vin;
end
inicial = V0*a.^k;
forzada = Vin*(1-a.^k);
assert(max(abs(vc-inicial-forzada)) < 1e-12);
residuo = diff(vc) - (1-a)*(Vin-vc(1:end-1));
assert(max(abs(residuo)) < 1e-12);
figure;
tt = linspace(0,t(end),601);
plot(tt,Vin+(V0-Vin)*exp(-tt/(R*C)), ...
     t,forzada,'--',t,inicial,':',t,vc,'o','LineWidth',1.2);
xlabel('Tiempo (s)'); ylabel('Tensión del capacitor (V)'); grid on;
legend('Evolución continua','Debida a la entrada', ...
       'Debida al estado inicial','Muestras del modelo discreto');

% Mecanismo masa-resorte-amortiguador con fuerza constante por intervalos.
m = 1; b = 2; K = 5; Ts = 0.2;
A = [0 1; -K/m -b/m]; B = [0; 1/m];
E = expm([A B; zeros(1,3)]*Ts);
Ad = E(1:2,1:2); Bd = E(1:2,3);
r = exp(-Ts); theta = 2*Ts;
den = [1 -2*r*cos(theta) r^2];
beta1 = (1-r*(cos(theta)+0.5*sin(theta)))/K;
beta2 = sum(den)/K-beta1;
disp('Ad, Bd y polos:'); disp(Ad); disp(Bd); disp(eig(Ad));
disp('Numerador y denominador en z^(-1):');
disp([0 beta1 beta2]); disp(den);
assert(all(abs(eig(Ad)) < 1));

k = 0:40; t = k*Ts; F0 = 5; N = 10;
fuerzas = {F0*ones(size(k)), F0*double(k<N)};
titulos = {'Fuerza constante de 5 N','Pulso de 5 N durante 2 s'};
figure; tiledlayout(2,1);
for j = 1:2
    fuerza = fuerzas{j};
    estado = zeros(2,numel(k));
    for n = 1:numel(k)-1
        estado(:,n+1) = Ad*estado(:,n)+Bd*fuerza(n);
    end
    y = estado(1,:);
    yFiltro = filter([0 beta1 beta2],den,fuerza);
    assert(max(abs(y-yFiltro)) < 1e-12);
    exacta = F0/K*(1-exp(-t).*(cos(2*t)+0.5*sin(2*t)));
    tt = linspace(0,t(end),1601);
    yc = F0/K*(1-exp(-tt).*(cos(2*tt)+0.5*sin(2*tt)));
    if j == 2
        activos = k>=N; tr = t(activos)-N*Ts;
        exacta(activos) = exacta(activos)- ...
            F0/K*(1-exp(-tr).*(cos(2*tr)+0.5*sin(2*tr)));
        activos = tt>=N*Ts; tr = tt(activos)-N*Ts;
        yc(activos) = yc(activos)- ...
            F0/K*(1-exp(-tr).*(cos(2*tr)+0.5*sin(2*tr)));
    end
    assert(max(abs(y-exacta)) < 1e-12);
    nexttile;
    plot(t,y,'o',tt,yc,'LineWidth',1.2);
    title(titulos{j}); ylabel('Posición (m)'); grid on;
    legend('Modelo discreto exacto','Evolución continua');
end
xlabel('Tiempo (s)');
