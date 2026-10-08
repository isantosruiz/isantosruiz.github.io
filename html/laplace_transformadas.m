% Transformadas y fracciones parciales. Requiere Symbolic Math Toolbox.
clear;
syms t positive
syms s

funciones = [exp(-2*t), t, exp(-t)*sin(2*t)];
for f = funciones
    disp('Función y transformada:');
    disp(f);
    disp(simplify(laplace(f,t,s)));
end

ejemplos = [2/(s*(s+1)*(s+2)), ...
            (s+3)/(s+2)^2, ...
            (s+3)/(s^2+2*s+5)];
for F = ejemplos
    f = simplify(ilaplace(F,s,t));
    disp('Fracciones parciales e inversa para t > 0:');
    disp(partfrac(F,s));
    disp(f);
    assert(isAlways(simplify(laplace(f,t,s)-F) == 0));
end

syms tr real
disp('Escalón retardado:');
disp(ilaplace(exp(-2*s)/s,s,tr));
