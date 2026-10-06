%% Estimación de fuerza y potencia
% Ejemplo hipotético; los parámetros no describen un vehículo comercial.
% MATLAB R2020a o posterior. No requiere toolboxes adicionales.
m = 1200;                    % Masa total, kg
g = 9.81;                    % Aceleración de la gravedad, m/s^2
p = 15;                      % Pendiente porcentual: 15 significa 15 %
v_kmh = 20;
v = v_kmh/3.6;               % Velocidad sobre el camino, m/s
a = 0;                       % Aceleración longitudinal, m/s^2
rho = 1.2;                   % Densidad del aire, kg/m^3
Cd = 0.32;
Af = 2.2;                    % Área frontal, m^2
eta = 0.85;                  % Eficiencia de bornes de batería a ruedas
eta_t = 0.95;                % Eficiencia mecánica de la transmisión
Crr = [0.015; 0.050; 0.080]; % Escenarios ilustrativos de rodadura

q = p/100;
sinTheta = q/sqrt(1+q^2);
cosTheta = 1/sqrt(1+q^2);
theta = atan(q);
N = m*g*cosTheta;
Fpendiente = m*g*sinTheta;
Frodadura = Crr*N;
Faire = 0.5*rho*Cd*Af*v^2;    % Sin viento
Ftraccion = Fpendiente + Frodadura + Faire + m*a;
Pruedas = Ftraccion*v;
Peje = Pruedas/eta_t;
Ptraccion = Pruedas/eta;      % Potencia eléctrica, sin auxiliares

escenario = {'Pavimento de referencia'; ...
    'Rodadura media'; 'Rodadura alta'};
resultados = table(escenario,Crr,Ftraccion,Pruedas/1000, ...
    Ptraccion/1000,'VariableNames', ...
    {'Escenario','Crr','Fuerza_N','Ruedas_kW','Traccion_kW'});
disp(resultados)
fprintf('Ángulo de la pendiente: %.4f grados\n',theta*180/pi)
fprintf('Potencia en el eje, caso de referencia: %.3f kW\n',Peje(1)/1000)

%% Potencia a distintas velocidades
% Cada punto es un ascenso estacionario, no una maniobra de aceleración.
vel_kmh = (5:0.5:60)';
vel = vel_kmh/3.6;
Pcurvas = zeros(numel(vel),numel(Crr));
for j = 1:numel(Crr)
    fuerza = Fpendiente + Crr(j)*N + 0.5*rho*Cd*Af*vel.^2;
    Pcurvas(:,j) = fuerza.*vel/eta/1000;
end

outDir = fileparts(mfilename('fullpath'));
colores = [0.05 0.42 0.43; 0.65 0.32 0.08; 0.64 0.18 0.31];
fPotencia = figure('Color','w','Position',[100 100 1000 660]);
ax = axes(fPotencia);
hold(ax,'on')
for j = 1:numel(Crr)
    plot(ax,vel_kmh,Pcurvas(:,j),'Color',colores(j,:), ...
        'LineWidth',2)
    plot(ax,v_kmh,Ptraccion(j)/1000,'o','Color',colores(j,:), ...
        'MarkerFaceColor',colores(j,:),'MarkerSize',6, ...
        'HandleVisibility','off')
end
xline(ax,v_kmh,':','Color',[0.45 0.45 0.45],'HandleVisibility','off')
xlim(ax,[5 60])
ylim(ax,[0 60])
grid(ax,'on')
box(ax,'off')
xlabel(ax,'Velocidad sobre el camino (km/h)')
ylabel(ax,'Potencia eléctrica de tracción (kW)')
legend(ax,{'$C_{rr} = 0.015$','$C_{rr} = 0.050$','$C_{rr} = 0.080$'}, ...
    'Interpreter','latex','Location','northwest','Box','off')
set(ax,'FontSize',13,'TickLabelInterpreter','latex')
exportgraphics(fPotencia,fullfile(outDir,'pendientes-potencia.png'), ...
    'Resolution',160)

%% Esquema de fuerzas
% El ángulo se amplía para facilitar la lectura. Flechas no a escala.
fFuerzas = figure('Color','w','Position',[100 100 1000 640]);
ax = axes(fFuerzas);
hold(ax,'on')
angle = 24*pi/180;
t = [cos(angle);sin(angle)];
n = [-sin(angle);cos(angle)];
R = [t n];
base = 4*t;
road = [0 8.6];
plot(ax,t(1)*road,t(2)*road,'Color',[0.55 0.57 0.57],'LineWidth',2)
plot(ax,[0 2.5],[0 0],'--','Color',[0.65 0.65 0.65])
arc = linspace(0,angle,70);
plot(ax,1.7*cos(arc),1.7*sin(arc),'Color',colores(1,:),'LineWidth',1.4)
text(ax,1.9*cos(angle/2),1.9*sin(angle/2),'$\theta$', ...
    'Interpreter','latex','FontSize',17,'Color',colores(1,:))

body = [-1.55 0.36;1.55 0.36;1.55 0.8;0.75 0.95; ...
    0.2 1.4;-0.8 1.4;-1.13 0.88;-1.55 0.78]';
body = redondearContorno(body,0.08);
body = R*body + base;
patch(ax,body(1,:),body(2,:),[0.91 0.94 0.94], ...
    'EdgeColor',[0.20 0.24 0.24],'LineWidth',1.5)
phi = linspace(0,2*pi,90);
for axle = [-1 1]
    center = base + R*[axle;0.24];
    patch(ax,center(1)+0.24*cos(phi),center(2)+0.24*sin(phi), ...
        [0.28 0.30 0.30],'EdgeColor','none')
end
c = base + 0.84*n;
flecha(ax,c,2.55*t,colores(1,:),'F_t',[0.05 0.17])
flecha(ax,c,-2.65*t,colores(2,:),'F_{rr}+F_a',[-0.4 0.38])
flecha(ax,c,1.7*n,[0.28 0.36 0.42],'N',[-0.1 0.16])
flecha(ax,c,[0;-2.55],colores(3,:),'mg',[0.18 0])
plot(ax,c(1),c(2),'o','MarkerFaceColor',[0.15 0.19 0.19], ...
    'MarkerEdgeColor','w','MarkerSize',6)
axis(ax,'equal')
xlim(ax,[-0.4 8.3])
ylim(ax,[-0.9 5.0])
axis(ax,'off')
exportgraphics(fFuerzas,fullfile(outDir,'pendientes-fuerzas.png'), ...
    'Resolution',160)

function flecha(ax,origin,vector,color,label,offset)
quiver(ax,origin(1),origin(2),vector(1),vector(2),0, ...
    'Color',color,'LineWidth',2,'MaxHeadSize',0.22)
endpoint = origin+vector;
text(ax,endpoint(1)+offset(1),endpoint(2)+offset(2),['$' label '$'], ...
    'Interpreter','latex','FontSize',18,'Color',color, ...
    'VerticalAlignment','middle')
end

function outline = redondearContorno(vertices,recorte)
% Curvas cuadráticas suavizan las esquinas y conservan los lados rectos.
count = size(vertices,2);
samples = 12;
u = linspace(0,1,samples);
outline = zeros(2,count*samples);
for j = 1:count
    corner = vertices(:,j);
    incoming = vertices(:,mod(j-2,count)+1)-corner;
    outgoing = vertices(:,mod(j,count)+1)-corner;
    distance = min(recorte,min(norm(incoming),norm(outgoing))/3);
    entry = corner+distance*incoming/norm(incoming);
    departure = corner+distance*outgoing/norm(outgoing);
    segment = entry*(1-u).^2+2*corner*(u.*(1-u))+departure*u.^2;
    outline(:,(j-1)*samples+(1:samples)) = segment;
end
end
