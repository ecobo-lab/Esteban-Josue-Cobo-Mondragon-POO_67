import RPi.GPIO as GPIO
import time

def configurar():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(18, GPIO.OUT)
    GPIO.setup(25, GPIO.IN)

def controlar_led(pin1, pin2):
    while True:
        if GPIO.input(pin2):
            GPIO.output(pin1, False)
        else:
            GPIO.output(pin1, True)
        time.sleep(0.1)

configurar()
controlar_led(18, 25)
