import time
import RPi.GPIO as GPIO
import regulators

if __name__ == 'reg_process':

    try:
        # os.system('modprobe w1-gpio')
        # os.system('modprobe w1-therm')
        #
        # base_dir = '/sys/bus/w1/devices/'
        # device_folder = glob.glob(base_dir + '28*')[0]
        # device_file = device_folder + '/w1_slave'  #### konfiguracia teplomera

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(23, GPIO.OUT) # ventilator
        GPIO.setup(18, GPIO.OUT) # vyhrevne teleso

        reference = int(input('Napis pozadovanu teplotu [25°C - 65°C]: '))

        regulator = regulators.switch(reference)

        while True:

            temperature = regulators.read_temp()
            regulators.data_writer(temperature)
            print(temperature)

            if regulator.regulation(temperature):
                GPIO.output(18,GPIO.HIGH)
            else:
                GPIO.output(18, GPIO.LOW)

            time.sleep(2)
    except KeyboardInterrupt:
        GPIO.output(18, GPIO.LOW)
        print('Proces je ukonceny prebehne vetranie komory')

    finally:
        time.sleep(2)
        GPIO.output(23, GPIO.HIGH)
        time.sleep(60)
        GPIO.output(23, GPIO.LOW)
        GPIO.cleanup()

        final_temp = regulators.read_temp()
        print('Teplota po vetrani: {}'.format(final_temp))
        GPIO.cleanup()
