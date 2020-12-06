import os
import glob
import time
import csv
import RPi.GPIO as GPIO


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


def data_writer(temperature):
    dir = 'data/'
    with open((dir + ('data.csv')), 'a', newline='') as csvfile:
        spamwriter = csv.writer(csvfile)
        spamwriter.writerow([temperature])


if __name__ == '__main__':

    try:
        os.system('modprobe w1-gpio')
        os.system('modprobe w1-therm')

        base_dir = '/sys/bus/w1/devices/'
        device_folder = glob.glob(base_dir + '28*')[0]
        device_file = device_folder + '/w1_slave'  #### konfiguracia teplomera

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(23, GPIO.OUT)
        GPIO.setup(18, GPIO.OUT)

        desired_time = None
        desired_time = int(input('Napis dlzku vyhrievania[s]:'))

        time_stamp = time.time()
        time_of_process = desired_time + time_stamp
        GPIO.output(18, GPIO.HIGH)

        while True:

            teplota = read_temp()
            data_writer(teplota)
            print(teplota)

            time.sleep(1.8)
            if time.time() > time_of_process:
                break

    except KeyboardInterrupt:
        print('Proces je ukonceny prebehne vetranie komory')
        desired_time = time.time() - time_stamp
        if not desired_time:
            desired_time = 0


    finally:
        GPIO.output(18, GPIO.LOW)
        print('Proces je ukonceny prebehne vetranie komory')
        time.sleep(2)
        GPIO.output(23, GPIO.HIGH)

        time.sleep(desired_time / 2)
        GPIO.output(23, GPIO.LOW)
        GPIO.cleanup()

        final_temp = read_temp()
        print('Teplota po vetrani: {}'.format(final_temp))
        GPIO.cleanup()

