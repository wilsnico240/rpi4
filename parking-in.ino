import RPi.GPIO as GPIO
import time

green_pin = 11
orange_pin = 13
red_pin = 15
lamp_pin = 22
servo_pin = 19
LDR_PIN = 29

GPIO.setmode(GPIO.BOARD)
GPIO.setup(green_pin, GPIO.OUT)
GPIO.setup(orange_pin, GPIO.OUT)
GPIO.setup(red_pin, GPIO.OUT)
GPIO.setup(lamp_pin, GPIO.OUT)
GPIO.setup(servo_pin, GPIO.OUT)
GPIO.setup(LDR_PIN, GPIO.IN)

lamp_pwm = GPIO.PWM(lamp_pin, 100)
lamp_pwm.start(0)

def read_ldr():
    ldr_value = 0
    for i in range(10):
        ldr_value += GPIO.input(LDR_PIN)
    return ldr_value / 10

def lamp_light(intensity):
    lamp_pwm.ChangeDutyCycle(intensity)

def open_barrier():
    pwm = GPIO.PWM(servo_pin, 50)
    pwm.start(7.5)
    time.sleep(1)

def close_barrier():
    pwm = GPIO.PWM(servo_pin, 50)
    pwm.start(3.2)
    time.sleep(1)

def traffic_light(color):
    if color == "green":
        GPIO.output(green_pin, GPIO.HIGH)
        GPIO.output(orange_pin, GPIO.LOW)
        GPIO.output(red_pin, GPIO.LOW)
        open_barrier()
        time.sleep(30)
    elif color == "orange":
        GPIO.output(green_pin, GPIO.LOW)
        GPIO.output(orange_pin, GPIO.HIGH)
        GPIO.output(red_pin, GPIO.LOW)
        time.sleep(3)
    elif color == "red":
        GPIO.output(green_pin, GPIO.LOW)
        GPIO.output(orange_pin, GPIO.LOW)
        GPIO.output(red_pin, GPIO.HIGH)
        close_barrier()
        time.sleep(10)

try:
    while True:
        ldr_intensity = read_ldr()
        lamp_light(ldr_intensity * 10)
        traffic_light("green")
        traffic_light("orange")
        traffic_light("red")
except KeyboardInterrupt:
    pass

lamp_pwm.stop()
GPIO.cleanup()
