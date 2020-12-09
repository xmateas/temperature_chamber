import csv
import os
import glob
import time

### ON/OFF regulator ###
class switch:
    def __init__(self,ref):
        self.ref = ref

    def regulation(self,input):
        if self.ref - input > 0:
            print('Zapnut')
            return True
        else:
            print('Vypnut')
            return False
###



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


def data_writer(temperature, vstup=None):
    dir = 'data/'
    with open((dir + ('data.csv')), 'a', newline='') as csvfile:
        spamwriter = csv.writer(csvfile)
        spamwriter.writerow([temperature, vstup])


def confi_writer(conf1):
    dir = 'data/'
    with open((dir + ('conf.csv')), 'a', newline='') as csvfile:
        spamwriter = csv.writer(csvfile)
        spamwriter.writerow(['Perioda vzorkovania', conf1])