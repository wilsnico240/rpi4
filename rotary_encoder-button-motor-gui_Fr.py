import RPi.GPIO as GPIO
from gpiozero import Motor
from time import sleep
import tkinter as tk

CLK = 17
DT = 27
SW = 25

GPIO.setmode(GPIO.BCM)
GPIO.setup(CLK, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(DT, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(SW, GPIO.IN, pull_up_down=GPIO.PUD_UP)

motor = Motor(forward=16, backward=12)

counter = 0

def update_motor_status():
    if counter < 0:
        direction = "En arrière"
    elif counter > 0:
        direction = "En avant"
    else:
        direction = "Arrêté"

    motor_speed = max(0, min(1, map_range(abs(counter), 0, 40, 0, 1)))
    status_label.config(text=f"Direction: {direction}\nVitesse: {motor_speed:.2f}")

def map_range(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def rotary_callback(channel):
    global counter
    CLK_state = GPIO.input(CLK)
    DT_state = GPIO.input(DT)
    if CLK_state != DT_state:
        counter += 1
    else:
        counter -= 1

    motor_speed = map_range(abs(counter), 0, 50, 0, 1)
    motor_speed = max(0, min(1, motor_speed))

    if counter < 0:
        motor.backward(speed=motor_speed)
    elif counter > 0:
        motor.forward(speed=motor_speed)
    else:
        motor.stop()

    update_motor_status()

def switch_callback(channel):
    global counter
    motor.stop()
    counter = 0
    update_motor_status()

def stop_program():
    GPIO.cleanup()
    window.quit()
    window.destroy()

window = tk.Tk()
window.title("Rotary Motor  ")
window.geometry("300x100")

status_label = tk.Label(window, text="Direction: Arrêté\nVitesse: 0.00", anchor='w', font=("Arial", 16))
status_label.pack()

stop_button = tk.Button(window, text="Arrêter le script", command=stop_program, font=("Arial", 16))
stop_button.pack()

GPIO.add_event_detect(CLK, GPIO.BOTH, callback=rotary_callback, bouncetime=5)
GPIO.add_event_detect(SW, GPIO.FALLING, callback=switch_callback, bouncetime=200)

window.mainloop()
