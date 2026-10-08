% Modelos RC y mecánico. Requiere Symbolic Math Toolbox.
clear;
syms t positive
syms s X

R = sym(1000); C = sym(1)/10000;
V0 = sym(1); Vin = sym(5);
Vc = (Vin/s + R*C*V0)/(R*C*s + 1);
vc = simplify(ilaplace(Vc,s,t));
assert(isAlways(simplify(R*C*diff(vc,t) + vc - Vin) == 0));
assert(isAlways(limit(vc,t,0,'right') == V0));
disp('Tensión del capacitor:'); disp(vc);

m = sym(1); b = sym(2); k = sym(5); F0 = sym(5);
x0 = sym(1)/5; v0 = sym(0);
ecuacion = m*(s^2*X-s*x0-v0) + b*(s*X-x0) + k*X == F0/s;
Xs = simplify(solve(ecuacion,X));
H = 1/(m*s^2+b*s+k);
Xentrada = H*F0/s;
Xinicial = H*((m*s+b)*x0+m*v0);
x = simplify(ilaplace(Xs,s,t));
xe = simplify(ilaplace(Xentrada,s,t));
xi = simplify(ilaplace(Xinicial,s,t));
assert(isAlways(simplify(m*diff(x,t,2)+b*diff(x,t)+k*x-F0) == 0));
assert(isAlways(limit(x,t,0,'right') == x0));
assert(isAlways(limit(diff(x,t),t,0,'right') == v0));
assert(isAlways(simplify(x-xe-xi) == 0));
disp('X(s) y x(t):'); disp(Xs); disp(x);
disp('Polos:'); disp(solve(m*s^2+b*s+k == 0,s));
disp('Posición final:'); disp(limit(s*Xs,s,0));

tt = linspace(0,8,1601);
fx = matlabFunction(x,'Vars',t);
fe = matlabFunction(xe,'Vars',t);
fi = matlabFunction(xi,'Vars',t);
figure;
plot(tt,fx(tt),tt,fe(tt),'--',tt,fi(tt),':','LineWidth',1.5);
xlabel('Tiempo (s)'); ylabel('Posición (m)'); grid on;
legend('Respuesta total','Debida a la fuerza', ...
       'Debida al estado inicial','Location','best');

% Segundo experimento: pulso de 5 N durante 2 s, desde el reposo.
T = 2;
xp = fe(tt);
activos = tt >= T;
xp(activos) = xp(activos) - fe(tt(activos)-T);
figure;
tiledlayout(2,1);
nexttile;
stairs(tt,double(F0)*(tt<T),'LineWidth',1.5);
ylabel('Fuerza (N)'); grid on;
nexttile;
plot(tt,xp,'LineWidth',1.5);
xlabel('Tiempo (s)'); ylabel('Posición (m)'); grid on;
