%% init
clear, close, clc

%% data gathering

system('synchro.bat.lnk'); % synchronizacia dat s raspberry, treba mat pripojene raspberry na sieti, nainstalovany a nakonfigurovany WinSCP
data = table2array(readtable('data/data.csv'));

temp = data(:,1);
input = data(:,2);

%%



