from tkinter import Tk, Text, Button, LEFT
from tkinter.font import Font
from gpiozero import MCP3008
from time import sleep

def read_sensor_values():
    value0 = MCP3008(0).value * 3.3
    value1 = MCP3008(1).value * 3.3
    value2 = MCP3008(2).value * 3.3
    value3 = MCP3008(3).value * 3.3
    value4 = MCP3008(4).value * 3.3
    value5 = MCP3008(5).value * 3.3
    value6 = MCP3008(6).value * 3.3
    value7 = MCP3008(7).value * 3.3
    sensor_data = ("Voltage sensor 0: %.2f\n" % value0 +
                    "Voltage sensor 1: %.2f\n" % value1 +
                    "Voltage sensor 2: %.2f\n" % value2 +
                    "Voltage sensor 3: %.2f\n" % value3 +
                    "Voltage sensor 4: %.2f\n" % value4 +
                    "Voltage sensor 5: %.2f\n" % value5 +
                    "Voltage sensor 6: %.2f\n" % value6 +
                    "Voltage sensor 7: %.2f\n" % value7)
    text_box.insert("end", sensor_data)

def clear_sensor_data():
    text_box.delete(1.0, "end")

root = Tk()
root.title("MCP3008 Voltage  ")
root.geometry('300x300')

font = Font(family="Arial", size=15)

text_box = Text(root, font=font, height=8, width=30)
text_box.pack()

read_button = Button(root, text="Read Sensor Voltage", command=read_sensor_values)
read_button.pack()

clear_button = Button(root, text="Clear Data", command=clear_sensor_data)
clear_button.pack()

close_button = Button(root, text="Close", command=root.destroy)
close_button.pack()

root.mainloop()
