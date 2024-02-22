from gpiozero import MCP3008, PWMLED, Button
import time
import tkinter as tk

analog_input = MCP3008(0)
led = PWMLED(27)
led2 = PWMLED(26)
button = Button(23)

def update_light_intensity():
    sensor_value = analog_input.value
    light_intensity = sensor_value * 100
    led.value = light_intensity / 100
    window.after(50, update_light_intensity)

def button_pressed():
    start_time = time.time()
    while button.is_pressed:
        if time.time() - start_time >= 3:
            led2.value = 0
            time.sleep(1)
            return
    led2.value = 1

def stop_program():
    window.destroy()
    led.close()
    led2.close()
    analog_input.close()
    button.close()

window = tk.Tk()
window.title("Licht")
window.geometry("250x35")

stop_button = tk.Button(window, text="Stop script", command=stop_program)
stop_button.pack()

button.when_pressed = button_pressed

update_light_intensity()

window.mainloop()
