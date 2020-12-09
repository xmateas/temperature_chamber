import time
import RPi.GPIO as GPIO
import regulators
import os

if __name__ == '__main__':

    try:
        os.remove('data/data.csv')
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(23, GPIO.OUT) # ventilator
        GPIO.setup(18, GPIO.OUT) # vyhrevne teleso
        ####
        ### Configuration ###
        ####
        reference = int(input('Napis pozadovanu teplotu [25°C - 65°C]: '))
        sampling_period = int(input('Napis periodu vzorkovania [s]: '))
        regulators.confi_writer(sampling_period,reference)
        regulator = regulators.switch(reference)
        ####


        while True:

            temperature = regulators.read_temp()

            print(temperature)

            if regulator.regulation(temperature):
                GPIO.output(18,GPIO.HIGH)
                vstup = 1
            else:
                GPIO.output(18, GPIO.LOW)
                vstup = 0
            regulators.data_writer(temperature,vstup)
            time.sleep(sampling_period)
    except KeyboardInterrupt:
        GPIO.output(18, GPIO.LOW)
        print('Proces je ukonceny prebehne vetranie komory')

    finally:
        time.sleep(2)
        ans = input('Chces vetrat? [Y/N]: ')
        if ans == 'Y' or ans == 'y':
            air_time = int(input('Kolko sekund? [s]: '))
            GPIO.output(23, GPIO.HIGH)
            time.sleep(air_time)
            GPIO.output(23, GPIO.LOW)
        else:
            pass

        final_temp = regulators.read_temp()
        print('Teplota v komore: {}'.format(final_temp))
        GPIO.cleanup()
