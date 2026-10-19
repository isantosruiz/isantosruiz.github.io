% Asignación estática de corriente a dos actuadores
H = diag([2, 4]);
c = [-6; -8];
A = [1, 1];
b = 4;
lb = [0; 0];
ub = [2.5; 3];

opciones = optimoptions('quadprog', 'Display', 'off');
[x, valor_qp, exitflag, salida] = quadprog( ...
    H, c, A, b, [], [], lb, ub, [], opciones);

if exitflag <= 0
    error('No se confirmó la convergencia: %s', salida.message);
end

tol = 1e-7;
assert(all(A*x <= b + tol), 'Se excede la corriente total.');
assert(all(x >= lb - tol) && all(x <= ub + tol), ...
    'Una corriente está fuera de sus límites.');

costo = (x(1)-3)^2 + 2*(x(2)-2)^2;
holguras = [b-A*x; ub-x; x-lb];
assert(abs(costo-(valor_qp+17)) < tol);
assert(norm(x-[7/3; 5/3]) < 1e-5);

fprintf('Corrientes [A]: %.6f, %.6f\n', x(1), x(2));
fprintf('Costo de seguimiento: %.6f\n', costo);
disp('Holguras [suma; cota superior 1; cota superior 2; inferiores]:');
disp(holguras);

% Visualización del objetivo y del conjunto factible
[X1, X2] = meshgrid(linspace(0, 3.5, 250), linspace(0, 3.5, 250));
F = (X1-3).^2 + 2*(X2-2).^2;
vertices = [0 0; 2.5 0; 2.5 1.5; 1 3; 0 3];

figure('Color', 'w');
hold on
patch(vertices(:,1), vertices(:,2), [0.84 0.94 0.91], ...
    'FaceAlpha', 0.5, 'EdgeColor', [0.1 0.4 0.35]);
contour(X1, X2, F, [2/3 1 2 4 8 12], 'LineWidth', 1);
plot(3, 2, 'kx', 'MarkerSize', 10, 'LineWidth', 2);
plot(x(1), x(2), 'ro', 'MarkerFaceColor', 'r', 'MarkerSize', 7);
xlabel('$x_1=I_1/I_0$', 'Interpreter', 'latex');
ylabel('$x_2=I_2/I_0$', 'Interpreter', 'latex');
title('Reparto de corriente con restricciones');
axis equal
xlim([0 3.5]); ylim([0 3.5]);
grid on
