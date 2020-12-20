import csv
import os
import glob
import time
# import termios
# import tty
# import sys
# import sys, termios, tty, os, time

### ON/OFF regulator ###
class switch:
    def __init__(self,ref):
        self.ref = ref

    def regulation(self,state):
        if self.ref - state > 0:
            print('Zapnut')
            return 100
        else:
            print('Vypnut')
            return 0
###
### P regulator ###

class P_regulator:
    def __init__(self,ref,Kp):
        self.ref = ref
        self.Kp = Kp
        self.error_list = []
        self.error = float

    def regulation(self,state):
        self.error = self.ref - state
        u_p = self.error*self.Kp

        u = u_p
        norm_u = max(min(100, u), 0)

        return norm_u

### PI regulator ###

class PI_regulator:
    def __init__(self, ref, Kp,Ki):
        self.ref = ref
        self.Kp = Kp
        self.Ki = Ki
        self.error_list = []
        self.error = float

    def regulation(self, state):
        self.error = self.ref - state
        self.error_list.append(self.error)

        u_i = sum(self.error_list)*self.Ki
        u_p = self.error * self.Kp

        u = u_p + u_i
        norm_u = max(min(100, u), 0)

        return norm_u,u_p,u_i

### PD regulator ###

class PD_regulator:
    def __init__(self, ref, Kp, Kd):
        self.ref = ref
        self.Kp = Kp
        self.Kd = Kd
        self.error_list = [0]
        self.error = float

    def regulation(self, state):
        self.error = self.ref - state
        self.error_list.append(self.error)

        u_d = (self.error_list[-1] - self.error_list[-2]) * self.Kd
        u_p = self.error * self.Kp

        u = u_p + u_d
        norm_u = max(min(100, u), 0)

        return norm_u, u_p, u_d

### PID regulator ###

class PID_regulator:
    def __init__(self, ref, Kp, Ki, Kd):
        self.ref = ref
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.error_list = [0]
        self.error = float

    def regulation(self, state):
        self.error = self.ref - state
        self.error_list.append(self.error)

        u_d = (self.error_list[-2] - self.error_list[-1]) * self.Kd
        u_i = sum(self.error_list)*self.Ki
        u_p = self.error * self.Kp

        u = u_p + u_i + u_d
        norm_u = max(min(100, u), 0)

        return norm_u, u_p, u_d, u_i





### functions for temperature reading ###
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'  #### konfiguracia teplomera

def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines


def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos + 2:]
        temp_c = float(temp_string) / 1000.0

        return temp_c



### Data logging
def data_writer(temperature, vstup=None,referencia=None):
    dir = 'data/'
    with open((dir + ('data.csv')), 'a', newline='') as csvfile:
        spamwriter = csv.writer(csvfile)
        spamwriter.writerow([temperature, vstup,referencia])


def confi_writer(conf1,conf2,conf3=None,conf4=None,conf5=None):
    dir = 'data/'
    with open((dir + ('conf.csv')), 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile)
        spamwriter.writerow(['Konfiguracny parameter', 'Hodnota'])
        spamwriter.writerow(['Perioda vzorkovania', conf1])
        spamwriter.writerow(['Referencia', conf2])

        if conf3:
            spamwriter.writerow(['Kp', conf3])
        if conf4:
            spamwriter.writerow(['Ki', conf4])
        if conf5:
            spamwriter.writerow(['Kd', conf5])
# def key_input():
#     ch = None
#     fd = sys.stdin.fileno()
#     old_settings = termios.tcgetattr(fd)
#
#     tty.setraw(sys.stdin.fileno())
#     ch = sys.stdin.read(1)
#     termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
#
#     if ch:
#         return ch
#     else:
#         return False









