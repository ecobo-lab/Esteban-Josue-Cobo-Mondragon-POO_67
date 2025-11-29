import RPi.GPIO as GPIO
import time

def configurar():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(18, GPIO.OUT)

def parpadear_led(pin):
    while True:
        GPIO.output(pin, True)
        time.sleep(1)
        GPIO.output(pin, False)
        time.sleep(1)

configurar()
parpadear_led(18)
