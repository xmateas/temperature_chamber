%% init
clear, close,clc

%% indetifikacia
%data1 = load('data/data_identifikacia/ident1.mat').t; % tieto data sa
%neberu v uvahu
%data2 = load('data/data_identifikacia/ident2.mat').t;
data3 = load('data/data_identifikacia/ident3.mat').t;
data4 = load('data/data_identifikacia/ident4.mat').t;



%% normovanie
ident = ((data3 + data4)*0.5)/100;
ident_min = min(ident);
ident = ident - ident_min;
%% cas 2sekundove vzorkovanie
t = (0:1:length(ident))*2;
t(end) = [];
t = t';
%% inflex. bod
K = ident(end)

dy = diff(ident);
dt = diff(t);
yd = dy./dt;

i = find(yd == max(yd));
t1 = t(i);
t2 = t(i+1);
y1 = ident(i);
y2 = ident(i+1);

tif = (t1 + t2)/2;
yif = (y1 + y2)/2;
a = (y1 - y2)/(t1 - t2);
b = y1 - a*t1;
tz = -b*0.5/a;
tk = (K-b*2.4)/a;

% figure
% plot(t,ident,tif,yif,'ro',[tz,tk],[0,K])

i = find(ident > 0,1);
D = t(i-1)

Tu = tz - D;
Tn = tk - tz;
f1 = Tn/Tu;
k = 0.9607;
f2 = 2.6647;
T1 = Tn/f2;
T2 = k*T1;
G = tf(K, conv([T1 1], [T2 1]), 'IODELAY',3)
[yi,ti] = step(G,t);
figure(6)
% plot(t,ident,ti,yi)

%% identifikovanie
num = cell2mat(G.numerator)
den= cell2mat(G.denominator)
%% urcenie T a Z


function G_ident = identification(y,t) % navrhujem ze je to system 2. radu

baropt = baronset('maxtime',15);

p0 = [10,10,10];
obj = @(p) sum((y' - model(p)).^2);
[p_hat,value] = baron(obj,[],[],[],[],[],[],[],[],[],p0,baropt)

G_ident = tf(p_hat(1),conv([p_hat(2) 1],[p_hat(3) 1]));

    function y_m = model(p)
        y_m = p(1) + ((p(1)*p(2))/(p(3)-p(2))).*exp(-t./p(2)) - ((p(1)*p(3))/(p(3)-p(2))).*exp(-t./p(3)) 

    end
end




