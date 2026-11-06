% Transformadas e inversas. Requiere Symbolic Math Toolbox.
clear
syms k integer
assumeAlso(k >= 0)
syms z

a = sym(1)/2;
b = sym(4)/5;
funciones = [a^k, k*a^k];
for f = funciones
    disp('Secuencia y transformada:');
    disp(f);
    disp(simplify(ztrans(f,k,z)));
end

X = z/((z-a)*(z-b));
x = simplify(iztrans(X,z,k));
xEsperada = (b^k-a^k)/(b-a);
disp('Fracciones parciales de X(z)/z:');
disp(partfrac(X/z,z));
disp('Inversa causal para k >= 0:'); disp(x);
assert(isAlways(simplify(x-xEsperada) == 0));
assert(isAlways(simplify(ztrans(x,k,z)-X) == 0));

X2 = z/(z-a)^2;
x2 = simplify(iztrans(X2,z,k));
assert(isAlways(simplify(x2-k*a^(k-1)) == 0));
disp('Inversa con polo repetido:'); disp(x2);

% El impulso de Kronecker no se confunde con la delta de Dirac.
disp('Inversa de z^(-3):'); disp(iztrans(z^(-3),z,k));

syms Y V y0 c
Ysol = simplify(solve(z*(Y-y0) == a*Y+c*V,Y));
disp('Solución con condición inicial:'); disp(Ysol);
disp('Valor inicial:'); disp(limit(Ysol,z,Inf));
