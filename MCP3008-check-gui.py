from gpiozero import MCP3008
import time
import tkinter as tk

analog_inputs = [MCP3008(i) for i in range(8)]

def update_sensor_values():
    try:
        for i, analog_input in enumerate(analog_inputs):
            sensor_value = analog_input.value
            sensor_label_list[i].config(text="Sensor waarde {}: {}".format(i + 1, sensor_value))
        root.after(2000, update_sensor_values)
    except Exception as e:
        print("Fout bij het updaten van de sensorwaarde:", e)

def close_program():
    root.destroy()

root = tk.Tk()
root.title("MCP3008")

sensor_label_list = []
for i in range(8):
    label = tk.Label(root, text="Sensor waarde {}: ".format(i + 1), font=("Arial", 16), justify="left")
    label.pack(pady=10)
    sensor_label_list.append(label)

close_button = tk.Button(root, text="Sluiten", command=close_program)
close_button.pack()

update_sensor_values()

root.mainloop()
