from gpiozero import MCP3008, Motor, Button
import tkinter as tk
from gpiozero import AngularServo
import time

servo = AngularServo(17, min_angle=-180, max_angle=180, initial_angle=60)

motor = Motor(16, 12)
analog_input = MCP3008(channel=7)
analog_input2 = MCP3008(channel=6)
button = Button(22)

motor_on = False

def update_motor_intensity():
    global motor_on
    if motor_on:
        sensor_value = analog_input.value * 2 - 1
        if sensor_value < -0.5:
            motor.backward(speed=-sensor_value)
        elif sensor_value > 0.5:
            motor.forward(speed=sensor_value)
        else:
            motor.stop()
    if motor_on:
        window.after(50, update_motor_intensity)

def update_servo_motor():
    if motor_on:
        sensor_value2 = analog_input2.value * 2 - 1
        angle = sensor_value2 * 180
        servo.angle = angle
    if motor_on:
        window.after(50, update_servo_motor)

def start_motor():
    global motor_on
    if not motor_on:
        motor_on = True
        update_motor_intensity()
        update_servo_motor()

def stop_motor():
    global motor_on
    if motor_on:
        motor.stop()
        motor_on = False

def on_button_pressed():
    start_motor()

def on_button_released():
    stop_motor()

def stop_program():
    window.destroy()
    analog_input.close()
    analog_input2.close()
    button.close()
    if motor_on:
        motor.stop()

window = tk.Tk()
window.title("Motor")
window.geometry("250x35")

stop_button = tk.Button(window, text="Stop script", command=stop_program)
stop_button.pack()

button.when_pressed = on_button_pressed
button.when_released = on_button_released

window.mainloop()
