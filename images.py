import tkinter as tk
from tkinter import ttk, Scrollbar, Canvas, Frame, messagebox
from PIL import Image, ImageTk
import requests
from bs4 import BeautifulSoup
import io
import os

class ImageSearchApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Search")

        self.entry_width = 50
        self.gui_width = self.entry_width * 10  
        self.root.geometry(f"{self.gui_width}x600")  

        self.entry = ttk.Entry(root, width=self.entry_width)
        self.entry.pack(pady=10)

        self.button_frame = Frame(root)
        self.button_frame.pack(pady=5)

        self.search_button = ttk.Button(self.button_frame, text="Search", command=self.search_images)
        self.search_button.pack(side="top", padx=5, pady=5)

        self.download_button = ttk.Button(self.button_frame, text="Download Selected", command=self.download_selected)
        self.download_button.pack(side="top", padx=5, pady=5)

        self.separator = ttk.Separator(root, orient="horizontal")
        self.separator.pack(fill="x", pady=10)

        self.canvas = Canvas(root, width=self.gui_width - 20)  
        self.scrollbar = Scrollbar(root, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw", width=self.gui_width - 20)

        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.selected_images = []

    def search_images(self):
        query = self.entry.get()
        if query:
            self.clear_images()
            self.fetch_images(query)

    def clear_images(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        self.selected_images.clear()

    def fetch_images(self, query):
        url = f"https://www.bing.com/images/search?q={query}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        }
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")

        for img in soup.find_all("img", class_="mimg"):
            img_url = img["src"]
            if img_url.startswith("http"):
                self.display_image(img_url)

    def display_image(self, img_url):
        try:
            response = requests.get(img_url)
            image_data = response.content
            image = Image.open(io.BytesIO(image_data))
            image.thumbnail((200, 200))
            photo = ImageTk.PhotoImage(image)

            frame = Frame(self.scrollable_frame)
            frame.pack(pady=5, anchor="center")  

            var = tk.BooleanVar()
            checkbox = ttk.Checkbutton(frame, variable=var)
            checkbox.pack(side="top", pady=5)  

            label = tk.Label(frame, image=photo)
            label.image = photo  
            label.pack(side="top") 

            self.selected_images.append((img_url, var, image))
        except Exception as e:
            print(f"Error loading image: {e}")

    def download_selected(self):
        if not os.path.exists("Images"):
            os.makedirs("Images")

        downloaded_count = 0
        for img_url, var, image in self.selected_images:
            if var.get():  
                try:
                    image_path = os.path.join("Images", f"image_{downloaded_count + 1}.jpg")
                    image.save(image_path)
                    downloaded_count += 1
                except Exception as e:
                    print(f"Error saving image: {e}")

        messagebox.showinfo("Download Complete", f"{downloaded_count} image(s) downloaded to the 'Images' folder.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageSearchApp(root)
    root.mainloop()
