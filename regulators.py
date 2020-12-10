import csv
import os
import glob
import time

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

    def regulation(self,state):

        error = self.ref - state
        u = error*self.Kp

        norm_u = max(min(100, u), 0)

        return norm_u





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
def data_writer(temperature, vstup=None):
    dir = 'data/'
    with open((dir + ('data.csv')), 'a', newline='') as csvfile:
        spamwriter = csv.writer(csvfile)
        spamwriter.writerow([temperature, vstup])


def confi_writer(conf1,conf2,conf3=None,conf4=None,conf5=None):
    dir = 'data/'
    with open((dir + ('conf.csv')), 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile)
        spamwriter.writerow(['Konfiguracny parameter', 'Hodnota'])
        spamwriter.writerow(['Perioda vzorkovania', conf1])
        spamwriter.writerow(['Referencia', conf2])

        if conf3:
            spamwriter.writerow(['Kp', conf3])









