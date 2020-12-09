%% init
clear, close, clc

%% data gathering

system('synchro.bat.lnk'); % synchronizacia dat s raspberry, treba mat pripojene raspberry na sieti, nainstalovany a nakonfigurovany WinSCP
data = table2array(readtable('data/data.csv'));
confi = readtable('data/conf.csv');

sampling_time = table2array(confi(1,{'Hodnota'}));
ref = table2array(confi(2,{'Hodnota'}));
temp = data(:,1);
input = data(:,2);

input(1) = [];
temp(1) = [];
%%
t = (2:1:length(input)+1)*sampling_time;

figure(1)
subplot(2,1,1)
plot(t,temp,'r','linewidth',2),hold on
plot([t(1),t(end)],[ref,ref],'k--','linewidth',1.5)
xlabel('time [s]')
ylabel('Temperature  °C')
grid on
ylim([20,ref*1.1])
legend('Temperature °C','Reference','location','southeast')


subplot(2,1,2)

stairs(t,input*100,'b--','linewidth',2)
xlabel('time [s]')
ylabel('Input %')
grid on
ylim([-20,120])



