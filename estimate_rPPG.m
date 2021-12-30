%% Seccion 1
clc
% input de datos canales RGB de determinada zona de interes
rgbt_d = xlsread('mzuniga.xls');

% extracci�n de vectores
rt = rgbt_d (:, 3);
gt = rgbt_d (:, 2);
bt = rgbt_d (:, 1);
f = rgbt_d (:, 4);  % frames indexados
fps = 60;
tof = f/fps;

% Preprocesado de se�ales, zero mean y normalizaci�n de varianza unitaria
% mediante zscore(.)
r=zscore(rt);
b=zscore(bt);
g=zscore(gt);
subplot(4,1,1)
plot(tof,r,'MarkerIndices',1:5:length(r),'Color',[1,0,0])
hold on
plot(tof,g,'MarkerIndices',1:5:length(g),'Color',[0,1,0])
hold on 
plot(tof,b,'MarkerIndices',1:5:length(b),'Color',[0,0,1])
hold off 
title('TSPs RGB traces in time')
xlabel('time(s)')
ylabel('Normalized Intensity')

% Calculo de los vectores ortogonales de Crominancia X e Y
X = 3*r - 2*g;
Y = 1.5*r + g - 1.5*b;

Cx = cov(X);    % covarianza de la se�al X
Cy = cov(Y);    % covarianza de la se�al Y

alfa = Cx/Cy; % coeficiente 

st = X - alfa*Y ;  % Se�al rPPG tentativa para la ROI

subplot(4,1,2)
plot(tof,st);
title('Tentative rPPG signal S_i(t)')
xlabel('time(s)')
ylabel('S_i(t)')
%% Obtenci�n de la Transformada de Fourier para la se�al rPPG tentativa en la regi�n dada.

X = st.';
Fs = 4000;            % Sampling frequency                    
T = 1/Fs;             % Sampling period       
L = length(X);             % Length of signal
t = (0:L-1)*T;        % Time vector

Y = fft(X);

P2 = abs(Y/L);
P1 = P2(1:L/2+1);
P1(2:end-1) = 2*P1(2:end-1);

f = Fs*(0:(L/2))/L;

subplot(4,1,3)
plot(f,P1) 
title('Amplitud del Espectro de S_i(t) (Single-Sided)')
xlabel('f (Hz)')
ylabel('|.|')

[pxx,w] = periodogram(X);
%subplot(4,1,4)
%plot(w,10*log10(pxx))
