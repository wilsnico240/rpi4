import tkinter as tk
import serial
import threading

root = tk.Tk()
root.title("3D-Scanner")
root.geometry("1150x813")

textbox = tk.Text(root, width=113, height=37, font=("Arial", 14, "bold"), wrap=tk.NONE)
textbox.pack()
textbox.config(borderwidth=2, relief="solid")

button_frame = tk.Frame(root)
button_frame.pack()

ser = serial.Serial('/dev/ttyACM0', 9600)

def ontvang_data():
    while True:
        data = ser.readline().decode().strip()
        data = data.replace(" ", ",")
        modified_data = []
        for item in data.split(","):
            modified_data.append("99" if int(item) > 99 else item)
        textbox.insert(tk.END, ",".join(modified_data) + '\n')

def reset_textbox():
    textbox.delete("1.0", tk.END)

def opslaan():
    bestand = open("3D-Scan.txt", "w")
    bestand.write(textbox.get("1.0", tk.END))
    bestand.close()

def close_window():
    ser.close()
    root.quit()
    root.destroy()

def calculate():
    input_data = textbox.get("1.0", tk.END)
    lines = input_data.split("\n")
    output_data = []

    for line in lines:
        line_data = line.split(",")
        new_line_data = []
        for datum in line_data:
            try:
                new_data = 100 - float(datum)
                new_line_data.append("{:.0f}".format(new_data))
            except ValueError:
                new_line_data.append(datum)
        output_data.append(",".join(new_line_data))

    output_text = "\n".join(output_data)
    textbox.delete("1.0", tk.END)
    textbox.insert(tk.END, output_text)

sluitknop = tk.Button(button_frame, text="Close", command=close_window)
sluitknop.pack(side=tk.LEFT)

reset_knop = tk.Button(button_frame, text="Reset", command=reset_textbox)
reset_knop.pack(side=tk.LEFT)

opslaan_knop = tk.Button(button_frame, text="Save", command=opslaan)
opslaan_knop.pack(side=tk.LEFT)

calculate_knop = tk.Button(button_frame, text="Calculate", command=calculate)
calculate_knop.pack(side=tk.LEFT)

receive_thread = threading.Thread(target=ontvang_data)
receive_thread.start()

root.mainloop()
