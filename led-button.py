import RPi.GPIO as GPIO
import time

led_pin = 26
button_pin = 23

GPIO.setmode(GPIO.BCM)
GPIO.setup(led_pin, GPIO.OUT)
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

button_pressed_time = 0
button_press_count = 0

def button_callback(channel):
    global button_pressed_time
    global button_press_count
    
    if (time.time() - button_pressed_time) < 0.3:
        button_press_count += 1
    else:
        button_press_count = 1
    
    button_pressed_time = time.time()
    
    if button_press_count == 1:
        GPIO.output(led_pin, GPIO.HIGH)
    elif button_press_count == 2:
        GPIO.output(led_pin, GPIO.LOW)
        button_press_count = 0

GPIO.add_event_detect(button_pin, GPIO.FALLING, callback=button_callback, bouncetime=200)

try:
    while True:
        time.sleep(1)

finally:
    GPIO.cleanup()
