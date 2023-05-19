import openai
import tkinter as tk
import subprocess

openai.api_key = "  "


def get_response(prompt):
    response = openai.Completion.create(
      engine="text-davinci-003",
      prompt=prompt,
      max_tokens=250,
      n=1,
      stop=None,
      temperature=0.4,
    )

    message = response.get('choices')[0].get('text')
    return message

def send_message():
    message = entry_box.get("1.0",'end-1c').strip()
    entry_box.delete("0.0", tk.END)

    if message != '':
        chat_box.config(state=tk.NORMAL)
        chat_box.insert(tk.END, "Vous: " + message + '\n\n')
        chat_box.config(foreground="#446665", font=("Verdana", 12 ))

        response = get_response(prompt=message)

        chat_box.insert(tk.END, "GPT: " + response + '\n\n')

        chat_box.config(state=tk.DISABLED)
        chat_box.yview(tk.END)
        espeak_output = subprocess.check_output(['espeak-ng', '-v', 'en+f2', '-m', '-s', '127', '-z', '--stdout', response])
        subprocess.Popen(['paplay'], stdin=subprocess.PIPE).communicate(input=espeak_output)

def enter_pressed(event):
    send_message()

root = tk.Tk()
root.title("ChatGPT")
root.geometry("750x500")

# Chat display
chat_box = tk.Text(root, bd=0, bg="white", height="8", width="50", font="Arial",)
chat_box.config(state=tk.DISABLED)

# Scrollbar
scrollbar = tk.Scrollbar(root, command=chat_box.yview, cursor="heart")
chat_box['yscrollcommand'] = scrollbar.set

# Input box
entry_box = tk.Text(root, bd=0, bg="white", width="28", height="5", font="Arial")

entry_box.bind("<Return>", enter_pressed)

# Send button
send_button = tk.Button(root, font="Arial", text="Send", width="10", height=5,
                        bd=0, bg="blue", activebackground="#ffffff",
                        command=send_message)

# Widgets
scrollbar.place(x=726,y=6, height=386)
chat_box.place(x=6,y=6, height=386, width=720)
entry_box.place(x=128, y=401, height=90, width=615)
send_button.place(x=6, y=401, height=90)

root.mainloop()
