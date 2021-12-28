%% Seccion 1
clc
% input de datos canales RGB de determinada zona de interes
rgbt_d = xlsread('out2.xls');




% extracción de vectores
rt = rgbt_d (:, 3);
gt = rgbt_d (:, 2);
bt = rgbt_d (:, 1);
t = rgbt_d (:, 4);  % frames indexados

% Preprocesado de señales, zero mean y normalización de varianza unitaria
% mediante zscore(.)
r=zscore(rt);
b=zscore(bt);
g=zscore(gt);

% Calculo de los vectores ortogonales de Crominancia X e Y
X = 3*r - 2*g;
Y = 1.5*r + gt - 1.5*b;

Cx = cov(X);    % covarianza de la señal X
Cy = cov(Y);    % covarianza de la señal Y

alfa = Cx/Cy; % coeficiente 

St = X - alfa*Y ;  % Señal rPPG tentativa para la ROI

%subplot(1,2,1)
%plot(t,St); 

[pxx,w] = periodogram(St);
%subplot(1,2,2)
%plot(w,10*log10(pxx))
