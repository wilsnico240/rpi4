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
         textbox.insert(tk.END, data + '\n')

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

sluitknop = tk.Button(button_frame, text="Close", command=close_window)
sluitknop.pack(side=tk.LEFT)

reset_knop = tk.Button(button_frame, text="Reset", command=reset_textbox)
reset_knop.pack(side=tk.LEFT)

opslaan_knop = tk.Button(button_frame, text="Save", command=opslaan)
opslaan_knop.pack(side=tk.LEFT)

receive_thread = threading.Thread(target=ontvang_data)
receive_thread.start()

root.mainloop()
