%% init
clear,close,clc

%%
load('data/switch_onff_30.mat')
load('data/switch_onff_40.mat')
load('data/switch_onff_50.mat')

t1 = (0:1:length(data1)-1)*2;
t2 = (0:1:length(data2)-1)*2;
t3 = (0:1:length(data3)-1)*2;
%%
% 30 stupnov
figure(1)
subplot(2,1,1)
plot(t1,data1(:,2),'r','linewidth',2),hold on
plot([0,2000],[30,30],'--k','linewidth',1.5)
grid on
xlim([0,2000])

subplot(2,1,2)
plot(t1,data1(:,1),':b','linewidth',1.5),hold on
grid on
ylim([-0.2,1.2])
xlim([0,2000])
% 40 stupnov
%%
figure(2)
subplot(2,1,1)
plot(t2,data2(:,2),'r','linewidth',2),hold on
plot([0,2000],[40,40],'--k','linewidth',1.5)
grid on
xlim([0,2000])

subplot(2,1,2)
plot(t2,data2(:,1),':b','linewidth',1.5),hold on
grid on
ylim([-0.2,1.2])
xlim([0,2000])

%% 50 stupnov
figure(3)
subplot(2,1,1)
plot(t3,data3(:,2),'r','linewidth',2),hold on
plot([0,2000],[50,50],'--k','linewidth',1.5)
grid on
xlim([0,2000])

subplot(2,1,2)
plot(t3,data3(:,1),':b','linewidth',1.5),hold on
grid on
ylim([-0.2,1.2])
xlim([0,2000])

%% porovnanie 
figure(4)
plot(data1(:,2),'r','linewidth',2),hold on
plot(data2(:,2),'b','linewidth',2)
plot(data3(:,2),'g','linewidth',2)


plot([0,1000],[30,30],'--k','linewidth',1.5)
plot([0,1000],[40,40],'--k','linewidth',1.5)
plot([0,1000],[50,50],'--k','linewidth',1.5)

legend('Referencia: 30 stupnov','Referencia: 40 stupnov','Referencia: 50 stupnov')
grid on
xlim([0,900])






