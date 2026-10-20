% Ubicación de una fábrica sin restricciones
syms x y real
P = [0 0; 4 2; 2 3];
J = sqrt(x^2 + y^2) ...
    + sqrt((x-4)^2 + (y-2)^2) ...
    + sqrt((x-2)^2 + (y-3)^2);
gradJ = gradient(J, [x, y]);
HJ = hessian(J, [x, y]);

[xs, ys] = vpasolve(gradJ == 0, [x, y], [2, 2]);
if isempty(xs) || isempty(ys)
    error('No se encontró un punto estacionario.');
end
p = double([xs; ys]);
assert(isreal(p) && all(isfinite(p)), 'La solución debe ser real y finita.');
costo = double(subs(J, [x, y], p.'));
residuo = double(subs(gradJ, [x, y], p.'));
Hopt = double(subs(HJ, [x, y], p.'));
assert(norm(residuo) < 1e-8, 'El gradiente no es suficientemente pequeño.');
assert(all(eig(Hopt) > 0), 'No se confirmó la curvatura positiva.');

fprintf('Ubicación óptima: (%.6f, %.6f)\n', p(1), p(2));
fprintf('Suma mínima de distancias: %.6f\n', costo);
disp('Eigenvalores de la hessiana en la solución:');
disp(eig(Hopt));

figure('Color', 'w');
hold on
hCentros = plot(P(:,1), P(:,2), 'ko', 'MarkerFaceColor', 'k');
hFabrica = plot(p(1), p(2), 'rp', 'MarkerSize', 12, 'MarkerFaceColor', 'r');
for k = 1:size(P, 1)
    plot([p(1), P(k,1)], [p(2), P(k,2)], '--', 'Color', [0.2 0.5 0.5]);
end
xlabel('$x$', 'Interpreter', 'latex');
ylabel('$y$', 'Interpreter', 'latex');
title('Ubicación óptima de la fábrica');
legend([hCentros, hFabrica], {'Centros de distribución', 'Fábrica óptima'}, ...
    'Location', 'best');
axis equal
xlim([-0.3 4.3]); ylim([-0.3 3.3]);
grid on
