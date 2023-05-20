import openai
import tkinter as tk
import subprocess

openai.api_key = "  "

def get_response(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=500,
        n=1,
        stop=None,
        temperature=0.4,
    )
    message = response.get('choices')[0].get('text')
    return message

def say_response(message):
    subprocess.Popen(['espeak-ng', '-v', voice.get(), '-m', '-s', speed.get(), '-z', message], stdout=subprocess.PIPE)

def send_message():
    message = entry_box.get("1.0",'end-1c')
    response = get_response(message)
    chat_history.config(state=tk.NORMAL)
    chat_history.insert(tk.END, "You: " + message + "\n\n")
    chat_history.config(foreground="#442265", font=("Verdana", 12 ))
    chat_history.insert(tk.END, "Assistant: " + response + "\n\n")
    chat_history.config(state=tk.DISABLED)
    chat_history.yview(tk.END)
    say_response(response)
    entry_box.delete('1.0', tk.END)

app = tk.Tk()
app.title("ChatGPT")
app.geometry("750x500")

voice_label = tk.Label(app, text="Select the voice:")
voice_label.pack()

voice_options = ["none", "fr+f2", "fr+m7", "en+f2", "en+m7", "nl+f4", "nl+m7", "de+f2", "de+m7"]
voice = tk.StringVar(app)
voice.set(voice_options[0])

voice_dropdown = tk.OptionMenu(app, voice, *voice_options)
voice_dropdown.pack()

speed_label = tk.Label(app, text="Select speed:")
speed_label.pack()

speed = tk.StringVar(app)
speed.set("127")

speed_scale = tk.Scale(app, variable=speed, from_=80, to=400, orient=tk.HORIZONTAL)
speed_scale.pack()

chat_history = tk.Text(app, bd=1, bg='white', height=15, width=50)
chat_history.pack()

scrollbar = tk.Scrollbar(app)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

chat_history.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=chat_history.yview, cursor="heart")

entry_box = tk.Text(app, bd=0, bg="white", width="28", height="5", font="Arial")
entry_box.pack()

send_button = tk.Button(app, font="Arial", text="Send", width="10", height=5,
                        bd=0, bg="blue", activebackground="#ffffff",
                        command=send_message)
send_button.pack()

voice_label.place(x=166,y=10)
voice_dropdown.place(x=277,y=5)
speed_label.place(x=375,y=10)
speed_scale.place(x=465,y=2)
chat_history.place(x=6,y=50, height=352, width=724)
scrollbar.place(x=730,y=50, height=353)
entry_box.place(x=128, y=401, height=90, width=615)
send_button.place(x=6, y=401, height=90)

app.mainloop()
