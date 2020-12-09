%% init
clear, close, clc

%% data gathering

system('synchro.bat.lnk'); % synchronizacia dat s raspberry, treba mat pripojene raspberry na sieti, nainstalovany a nakonfigurovany WinSCP
data = table2array(readtable('data/data.csv'));
confi = readtable('data/conf.csv');

sampling_time = table2array(confi(1,{'Hodnota'}));
temp = data(:,1);
input = data(:,2);

%%
t = (1:1:length(input))*sampling_time;

figure(1)
subplot(2,1,1)
plot(t,temp,'r','linewidth',2)
xlabel('time [s]')
ylabel('Temperature  °C')
grid on

subplot(2,1,2)

plot(t,input,'b','linewidth',2)
xlabel('time [s]')
ylabel('Input %')
grid on
ylim([-0.2,1.2])



