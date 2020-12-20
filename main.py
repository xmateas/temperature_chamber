import time
import RPi.GPIO as GPIO
import regulators
import os

if __name__ == '__main__':

    try:
        try:
            os.remove('data/data.csv')
        except IOError:
            print('Neboli najdene predchadzajuce data')
            pass
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(23, GPIO.OUT) # ventilator
        GPIO.setup(18, GPIO.OUT) # vyhrevne teleso
        p = GPIO.PWM(18,100) # pracujeme s PWM
        p.start(0)
        ###
        ## Configuration ###
        ###
        option = input('Napis typ regulator [S/P/PI/PD/PID]: ')

        if option == 'S' or option =='s':
            reference = int(input('Napis pozadovanu teplotu [25°C - 65°C]: '))
            sampling_period = int(input('Napis periodu vzorkovania [s]: '))
            regulators.confi_writer(sampling_period,reference)
            regulator = regulators.switch(reference)

        elif option == 'P' or option =='p':
            reference = int(input('Napis pozadovanu teplotu [25°C - 65°C]: '))
            sampling_period = int(input('Napis periodu vzorkovania [s]: '))
            Kp = int(input('Napis hodnotu zosilnenia Kp: '))
            regulators.confi_writer(sampling_period, reference,Kp)
            regulator = regulators.P_regulator(reference,Kp)

        elif option == 'PI' or option == 'pi':
            reference = int(input('Napis pozadovanu teplotu [25°C - 65°C]: '))
            sampling_period = int(input('Napis periodu vzorkovania [s]: '))
            Kp = float(input('Napis hodnotu zosilnenia Kp: '))
            Ki = float(input('Napis hodnotu zosilnenia Ki: '))
            regulators.confi_writer(sampling_period, reference, Kp, Ki)
            regulator = regulators.PI_regulator(reference, Kp, Ki)

        elif option == 'PD' or option == 'pd':
            reference = int(input('Napis pozadovanu teplotu [25°C - 65°C]: '))
            sampling_period = int(input('Napis periodu vzorkovania [s]: '))
            Kp = float(input('Napis hodnotu zosilnenia Kp: '))
            Kd = float(input('Napis hodnotu zosilnenia Kd: '))
            regulators.confi_writer(sampling_period, reference, Kp,None, Kd)
            regulator = regulators.PD_regulator(reference, Kp, Kd)

        elif option == 'PID' or option == 'pid':
            reference = int(input('Napis pozadovanu teplotu [25°C - 65°C]: '))
            sampling_period = int(input('Napis periodu vzorkovania [s]: '))
            Kp = float(input('Napis hodnotu zosilnenia Kp: '))
            Ki = float(input('Napis hodnotu zosilnenia Ki: '))
            Kd = float(input('Napis hodnotu zosilnenia Kd: '))
            regulators.confi_writer(sampling_period, reference, Kp,Ki, Kd)
            regulator = regulators.PID_regulator(reference, Kp,Ki, Kd)
        while True:

            temperature = regulators.read_temp()  # citanie teploty
            # print(str(temperature) + '°C')  # vypisovanie teploty do command window

            vstup,p_zlozka,d_zlozka,i_zlozka = regulator.regulation(temperature)  # vypocitanie akcneho zasahu
            print(str(temperature) + '°C' + ' P zlozka:' + str(round(p_zlozka,2)) + ' I_zlozka:' + str(round(i_zlozka,2)) + ' D_zlozka:' + str(round(d_zlozka,2))+ ' Suma: ' + str(round(i_zlozka + p_zlozka, 2)))  #iba pre debugovanie
            p.ChangeDutyCycle(vstup)  # aplikovanie akcneho zasahu

            regulators.data_writer(temperature, vstup, reference)  # logovanie udajov
            time.sleep(sampling_period)  # perioda vzorkovania





    except KeyboardInterrupt:
        p.stop()
        GPIO.output(18, GPIO.LOW)
        print('Proces je ukonceny prebehne vetranie komory')


    finally:
        p.stop()
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
