#!/usr/bin/env python3

import importlib
import subprocess
import sys
import os
import webbrowser
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.simpledialog import askstring
import tempfile

REQUIRED_LIBRARIES = ['tkinter', 'reportlab']

class AutoCloseMessageBox:
    def __init__(self, title, message, duration=3000):
        self.top = tk.Toplevel()
        self.top.title(title)
        self.top.geometry("300x100")
        self.top.resizable(False, False)
        self.top.update_idletasks()
        width = self.top.winfo_width()
        height = self.top.winfo_height()
        x = (self.top.winfo_screenwidth() // 2) - (width // 2)
        y = (self.top.winfo_screenheight() // 2) - (height // 2)
        self.top.geometry(f'{width}x{height}+{x}+{y}')
        self.top.transient(self.top.master)
        self.top.grab_set()
        label = tk.Label(self.top, text=message, wraplength=250, justify="center")
        label.pack(pady=20)
        self.top.after(duration, self.close)

    def close(self):
        self.top.grab_release()
        self.top.destroy()

def check_and_install_libraries(root):
    for lib in REQUIRED_LIBRARIES:
        try:
            importlib.import_module(lib)
            message = AutoCloseMessageBox("Info", f"Bakery Tool V1.0 - {lib} found", 2000)
            root.update()
            while message.top.winfo_exists():
                root.update()
        except ImportError:
            message = AutoCloseMessageBox("Info", f"Installing {lib}...", 3000)
            root.update()
            while message.top.winfo_exists():
                root.update()
            try:
                if lib == 'tkinter' and sys.platform.startswith('linux'):
                    try:
                        subprocess.check_call(['sudo', 'apt-get', 'install', '-y', 'python3-tk'])
                        message = AutoCloseMessageBox("Success", f"{lib} successfully installed.", 3000)
                        root.update()
                        while message.top.winfo_exists():
                            root.update()
                    except subprocess.CalledProcessError:
                        message = AutoCloseMessageBox("Error", f"Failed to install {lib}. Ensure 'apt-get' is available and you have sudo privileges.", 5000)
                        root.update()
                        while message.top.winfo_exists():
                            root.update()
                        sys.exit(1)
                elif lib == 'reportlab':
                    subprocess.check_call([sys.executable, "-m", "pip", "install", lib])
                    message = AutoCloseMessageBox("Success", f"{lib} successfully installed.", 3000)
                    root.update()
                    while message.top.winfo_exists():
                        root.update()
                elif lib == 'tkinter' and not sys.platform.startswith('linux'):
                    message = AutoCloseMessageBox("Error", f"{lib} is missing and must be installed manually on {sys.platform}.", 5000)
                    root.update()
                    while message.top.winfo_exists():
                        root.update()
                    sys.exit(1)
            except subprocess.CalledProcessError:
                message = AutoCloseMessageBox("Error", f"Failed to install {lib}. Ensure pip is configured correctly or install manually.", 5000)
                root.update()
                while message.top.winfo_exists():
                    root.update()
                sys.exit(1)

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

CONVERSIONS_FR = {
    "eau (ml)": lambda x: x,
    "lait (ml)": lambda x: x * 1.03,
    "œuf": lambda x: x * 50
}

CONVERSIONS_NL = {
    "water (ml)": lambda x: x,
    "melk (ml)": lambda x: x * 1.03,
    "ei": lambda x: x * 50
}

CONVERSIONS_EN = {
    "water (ml)": lambda x: x,
    "milk (ml)": lambda x: x * 1.03,
    "egg": lambda x: x * 50
}

INGREDIENTS_FR = [
    "farine (g)", "graine (g)", "levure (g)",
    "levain (g)", "eau (ml)", "sel (g)",
    "œuf", "lait (ml)", "lait en poudre (g)", "boter (g)", "margarine (g)",
    "améliorant (g)", "Miel (g)",
    "sucre (g)", "sucre P2 (g)", "sucre P4 (g)", "raisins secs (g)",
    "chocolat (g)", "huile (g)", "olives (g)"
]

INGREDIENTS_NL = [
    "bloem (g)", "zaad (g)", "gist (g)",
    "zuurdesem (g)", "water (ml)", "zout (g)",
    "ei", "melk (ml)", "melkpoeder (g)", "boter (g)", "margarine (g)",
    "verbeteraar (g)", "honing (g)",
    "suiker (g)", "suiker P2 (g)", "suiker P4 (g)", "rozijnen (g)",
    "chocolade (g)", "olie (g)", "olijven (g)"
]

INGREDIENTS_EN = [
    "flour (g)", "seed (g)", "yeast (g)",
    "sourdough (g)", "water (ml)", "salt (g)",
    "egg", "milk (ml)", "milk powder (g)", "butter (g)", "margarine (g)",
    "improver (g)", "honey (g)",
    "sugar (g)", "sugar P2 (g)", "sugar P4 (g)", "raisins (g)",
    "chocolate (g)", "oil (g)", "olives (g)"
]

EXTRA_INGREDIENTS = ["extra 1", "extra 2", "extra 3"]

INGREDIENTMAP_FR_TO_NL = dict(zip(INGREDIENTS_FR, INGREDIENTS_NL))
INGREDIENTMAP_NL_TO_FR = dict(zip(INGREDIENTS_NL, INGREDIENTS_FR))
INGREDIENTMAP_FR_TO_EN = dict(zip(INGREDIENTS_FR, INGREDIENTS_EN))
INGREDIENTMAP_EN_TO_FR = dict(zip(INGREDIENTS_EN, INGREDIENTS_FR))
INGREDIENTMAP_NL_TO_EN = dict(zip(INGREDIENTS_NL, INGREDIENTS_EN))
INGREDIENTMAP_EN_TO_NL = dict(zip(INGREDIENTS_EN, INGREDIENTS_NL))

RECIPES = {
    "brood met gist": {
        "bloem (g)": 1700, "gist (g)": 50, "water (ml)": 900,
        "zout (g)": 30, "verbeteraar (g)": 20
    },
    "brood met zuurdesem": {
        "bloem (g)": 4000, "zuurdesem (g)": 500, "water (ml)": 2600,
        "zout (g)": 80
    },
    "toast brood met gist": {
        "bloem (g)": 270, "gist (g)": 15, "water (ml)": 160,
        "melk (ml)": 30, "zout (g)": 5,
        "boter (g)": 20, "suiker (g)": 15
    },
    "toast brood met melk zuurdesem": {
        "bloem (g)": 247, "zuurdesem (g)": 130, "water (ml)": 100,
        "zout (g)": 5, "boter (g)": 20, "suiker (g)": 5
    },
    "cramique": {
        "bloem (g)": 1000, "gist (g)": 80, "water (ml)": 450,
        "zout (g)": 20, "ei": 1, "melkpoeder (g)": 50, "boter (g)": 150,
        "margarine (g)": 150, "verbeteraar (g)": 20, "suiker (g)": 20,
        "suiker P2 (g)": 150, "rozijnen (g)": 250
    },
    "stokbrood": {
        "bloem (g)": 2500, "gist (g)": 120, "water (ml)": 1500,
        "zout (g)": 45, "verbeteraar (g)": 50
    },
    "pistolet": {
        "bloem (g)": 1500, "gist (g)": 90, "water (ml)": 900,
        "zout (g)": 25, "verbeteraar (g)": 30
    },
    "buns": {
        "bloem (g)": 20000, "gist (g)": 1000, "water (ml)": 4000,
        "zout (g)": 400, "ei": 20, "melk (ml)": 8000, "boter (g)": 3000,
        "suiker (g)": 1000
    },
    "sandwich": {
        "bloem (g)": 1000, "gist (g)": 60, "water (ml)": 500,
        "zout (g)": 20, "ei": 1, "melkpoeder (g)": 50, "boter (g)": 150,
        "suiker (g)": 20
    },
    "pizza met gist": {
        "bloem (g)": 1000, "gist (g)": 20, "water (ml)": 500,
        "zout (g)": 17, "olie (g)": 100
    },
    "pizza met zuurdesem": {
        "bloem (g)": 500, "zuurdesem (g)": 150, "water (ml)": 300,
        "zout (g)": 12, "olie (g)": 20
    },
    "taart": {
        "bloem (g)": 1000, "gist (g)": 40, "water (ml)": 400,
        "zout (g)": 17, "melkpoeder (g)": 50, "boter (g)": 250,
        "margarine (g)": 250, "suiker (g)": 40
    }
}

RECIPE_NAMES = {
    "NL": list(RECIPES.keys()),
    "FR": [
        "pain avec levure", "pain au levain", "pain de mie avec levure",
        "pain de mie au levain de lait", "cramique", "baguette",
        "pistolet", "buns", "sandwich", "pizza avec levure", "pizza au levain",
        "tarte"
    ],
    "EN": [
        "yeast bread", "sourdough bread", "toast bread with yeast",
        "milk sourdough toast bread", "cramique", "baguette",
        "pistolet", "buns", "sandwich", "yeast pizza", "sourdough pizza",
        "pie"
    ]
}

RECIPE_MAP_FR_TO_NL = dict(zip(RECIPE_NAMES["FR"], RECIPE_NAMES["NL"]))
RECIPE_MAP_NL_TO_FR = dict(zip(RECIPE_NAMES["NL"], RECIPE_NAMES["FR"]))
RECIPE_MAP_FR_TO_EN = dict(zip(RECIPE_NAMES["FR"], RECIPE_NAMES["EN"]))
RECIPE_MAP_EN_TO_FR = dict(zip(RECIPE_NAMES["EN"], RECIPE_NAMES["FR"]))
RECIPE_MAP_NL_TO_EN = dict(zip(RECIPE_NAMES["NL"], RECIPE_NAMES["EN"]))
RECIPE_MAP_EN_TO_NL = dict(zip(RECIPE_NAMES["EN"], RECIPE_NAMES["NL"]))

TEXTS = {
    "FR": {
        "title": "Calculateur d'ingrédients",
        "calculate": "Calculer le total",
        "reset": "Réinitialiser",
        "close": "Fermer",
        "total": "Poids total :",
        "newtotal": "Nouveau poids total :",
        "rescale": "Recalculer",
        "error_title": "Erreur",
        "error_value": "Entrez un nombre positif valide pour le nouveau poids total.",
        "error_zero": "Le poids total actuel est 0. Impossible de recalculer.",
        "pdf_prompt": "Entrez le nom du fichier PDF :",
        "pdf_saved": "PDF enregistré sous :",
        "print_prompt": "Entrez le titre de la recette:",
        "print_error": "Impossible d'envoyer le document à l'imprimante. Vérifiez la configuration de l'imprimante.",
        "multiplication_window_title": "Calcul de multiplication",
        "multiplication_label": " x ",
        "value_label": " g ",
        "enter_button": "Entrer",
        "recipe_label": "Recettes de pâte de base :",
        "choose_button": "Choisir",
        "recipe_window_title": "Choisir une recette",
        "recipe_header": "Quelques recettes de base. Cliquez sur une recette pour sélectionner !"
    },
    "NL": {
        "title": "Ingrediënten Calculator",
        "calculate": "Bereken totaal",
        "reset": "Reset",
        "close": "Sluiten",
        "total": "Totaal gewicht :",
        "newtotal": "Nieuw totaalgewicht :",
        "rescale": "Herbereken",
        "error_title": "Fout",
        "error_value": "Voer een geldig positief getal in voor het nieuwe totaalgewicht.",
        "error_zero": "Het huidige totaalgewicht is 0. Kan niet herberekenen.",
        "pdf_prompt": "Geef naam voor het PDF-bestand:",
        "pdf_saved": "PDF opgeslagen als:",
        "print_prompt": "Voer de titel in van het recept:",
        "print_error": "Kan document niet naar printer verzenden. Controleer de printerinstellingen.",
        "multiplication_window_title": "Multiplicatie Berekening",
        "multiplication_label": " x ",
        "value_label": " g ",
        "enter_button": "Invoeren",
        "recipe_label": "Basis deeg recepten:",
        "choose_button": "Kies",
        "recipe_window_title": "Kies een recept",
        "recipe_header": "Enkele basis recepten. Klik op een recept om te selecteren !"
    },
    "EN": {
        "title": "Ingredient Calculator",
        "calculate": "Calculate total",
        "reset": "Reset",
        "close": "Close",
        "total": "Total weight :",
        "newtotal": "New total weight :",
        "rescale": "Rescale",
        "error_title": "Error",
        "error_value": "Enter a valid positive number for the new total weight.",
        "error_zero": "The current total weight is 0. Cannot rescale.",
        "pdf_prompt": "Enter the PDF file name:",
        "pdf_saved": "PDF saved as:",
        "print_prompt": "Enter the recipe title:",
        "print_error": "Cannot send document to printer. Check printer settings.",
        "multiplication_window_title": "Multiplication Calculation",
        "multiplication_label": " x ",
        "value_label": " g ",
        "enter_button": "Enter",
        "recipe_label": "Basic dough recipes:",
        "choose_button": "Choose",
        "recipe_window_title": "Choose a recipe",
        "recipe_header": "Some basic recipes. Click on a recipe to select !"
    }
}

class IngredientApp:
    def __init__(self, root):
        self.root = root
        self.language = "EN"
        self.entries = {}
        self.extraname_entries = {}
        self.labels = []
        self.total_var = tk.StringVar(value="0 g")
        self.newtotal_var = tk.StringVar(value="0")

        self.input_frame = ttk.Frame(self.root)
        self.input_frame.pack(padx=10, pady=10)

        self.button_frame = ttk.Frame(self.root)
        self.button_frame.pack(pady=5)

        self.total_frame = ttk.Frame(self.root)
        self.total_frame.pack(pady=5)

        self.rescale_frame = ttk.Frame(self.root)
        self.rescale_frame.pack(pady=10)

        check_and_install_libraries(self.root)

        self.create_language_buttons()
        self.create_input_fields()
        self.create_recipe_section()
        self.create_total_display()
        self.create_rescale_section()
        self.update_language()

    def create_language_buttons(self):
        main_frame = ttk.Frame(self.root)
        main_frame.pack(pady=5)

        top_buttons = ttk.Frame(main_frame)
        top_buttons.pack()

        ttk.Button(top_buttons, text="NL", command=lambda: self.set_language("NL"), width=3).pack(side="left", padx=5)
        ttk.Button(top_buttons, text="FR", command=lambda: self.set_language("FR"), width=3).pack(side="left", padx=5)
        ttk.Button(top_buttons, text="EN", command=lambda: self.set_language("EN"), width=3).pack(side="left", padx=5)
        ttk.Button(top_buttons, text="Mail", command=self.send_email).pack(side="left", padx=5)

        pdf_button = ttk.Frame(main_frame)
        pdf_button.pack(pady=(10, 0))

        ttk.Button(pdf_button, text="PDF", command=self.generate_pdf).pack(side="left", padx=5)
        ttk.Button(pdf_button, text="PRINT", command=self.print_document).pack(side="left", padx=5)
        self.close_btn = ttk.Button(pdf_button, text="", command=self.root.destroy)
        self.close_btn.pack(side="left", padx=5)

    def generate_pdf(self):
        prompt = TEXTS[self.language]["pdf_prompt"]
        filename = askstring("PDF", prompt)
        if not filename:
            return

        if not filename.lower().endswith(".pdf"):
            filename += ".pdf"

        filepath = os.path.join(os.getcwd(), filename)
        c = canvas.Canvas(filepath, pagesize=A4)
        width, height = A4
        y = height - 50

        c.setFont("Helvetica-Bold", 16)
        c.drawString(50, y, filename.replace(".pdf", ""))
        y -= 30

        c.setFont("Helvetica", 12)
        for ingredient in self.get_ingredients():
            try:
                value = float(self.entries[ingredient].get().replace(",", "."))
            except ValueError:
                value = 0

            if value > 0:
                c.drawString(50, y, f"{ingredient}: {value}")
                y -= 20
                if y < 50:
                    c.showPage()
                    y = height - 50

        for extra in EXTRA_INGREDIENTS:
            name = self.extraname_entries[extra].get().strip()
            try:
                value = float(self.entries[extra].get().replace(",", "."))
            except ValueError:
                value = 0

            if value > 0 and name:
                c.drawString(50, y, f"{name} (g): {value}")
                y -= 20
                if y < 50:
                    c.showPage()
                    y = height - 50

        y -= 10
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, y, f"{TEXTS[self.language]['total']} {self.total_var.get()}")

        c.save()
        confirmation = TEXTS[self.language]["pdf_saved"]
        messagebox.showinfo("PDF", f"{confirmation}\n{filepath}")

    def print_document(self):
        prompt = TEXTS[self.language]["print_prompt"]
        title = askstring("Print", prompt)
        if not title:
            return

        temp_file = tempfile.NamedTemporaryFile(suffix=".pdf", delete=False)
        filepath = temp_file.name
        temp_file.close()

        try:
            c = canvas.Canvas(filepath, pagesize=A4)
            width, height = A4
            y = height - 50

            c.setFont("Helvetica-Bold", 16)
            c.drawString(50, y, title)
            y -= 30

            c.setFont("Helvetica", 12)
            for ingredient in self.get_ingredients():
                try:
                    value = float(self.entries[ingredient].get().replace(",", "."))
                except ValueError:
                    value = 0

                if value > 0:
                    c.drawString(50, y, f"{ingredient}: {value}")
                    y -= 20
                    if y < 50:
                        c.showPage()
                        y = height - 50

            for extra in EXTRA_INGREDIENTS:
                name = self.extraname_entries[extra].get().strip()
                try:
                    value = float(self.entries[extra].get().replace(",", "."))
                except ValueError:
                    value = 0

                if value > 0 and name:
                    c.drawString(50, y, f"{name} (g): {value}")
                    y -= 20
                    if y < 50:
                        c.showPage()
                        y = height - 50

            y -= 10
            c.setFont("Helvetica-Bold", 12)
            c.drawString(50, y, f"{TEXTS[self.language]['total']} {self.total_var.get()}")

            c.save()

            if sys.platform.startswith('win'):
                try:
                    os.startfile(filepath, "print")
                except Exception as e:
                    messagebox.showerror(TEXTS[self.language]["error_title"], f"{TEXTS[self.language]['print_error']} {str(e)}")
                    return
            elif sys.platform.startswith('darwin') or sys.platform.startswith('linux'):
                try:
                    subprocess.run(['which', 'lp'], check=True, capture_output=True)
                    result = subprocess.run(['lp', '-o', 'fit-to-page', filepath], check=True, capture_output=True)
                    if result.returncode == 0:
                        messagebox.showinfo("Print", f"Document sent to printer queue: {filepath}")
                    else:
                        messagebox.showerror(TEXTS[self.language]["error_title"], f"{TEXTS[self.language]['print_error']} lp command failed.")
                except subprocess.CalledProcessError as e:
                    messagebox.showerror(TEXTS[self.language]["error_title"], f"{TEXTS[self.language]['print_error']} {str(e)}")
                except FileNotFoundError:
                    messagebox.showerror(TEXTS[self.language]["error_title"], f"{TEXTS[self.language]['print_error']} lp command not found.")
            else:
                messagebox.showerror(TEXTS[self.language]["error_title"], f"{TEXTS[self.language]['print_error']} Unsupported platform.")
        finally:
            try:
                os.unlink(filepath)
            except Exception:
                pass

    def send_email(self):
        if self.language == "NL":
            subject = "recept"
        elif self.language == "EN":
            subject = "recipe"
        else:
            subject = "recette"
        body_lines = []

        for ingredient in self.get_ingredients():
            try:
                value = float(self.entries[ingredient].get().replace(",", "."))
            except ValueError:
                value = 0

            if value > 0:
                body_lines.append(f"{ingredient}: {value}")

        for extra in EXTRA_INGREDIENTS:
            name = self.extraname_entries[extra].get().strip()
            try:
                value = float(self.entries[extra].get().replace(",", "."))
            except ValueError:
                value = 0

            if value > 0 and name:
                body_lines.append(f"{name} (g): {value}")

        body_lines.append(f"\n{TEXTS[self.language]['total']} {self.total_var.get()}")

        body = "\n".join(body_lines)
        body_encoded = body.replace("\n", "%0D%0A").replace(" ", "%20")
        subject_encoded = subject.replace(" ", "%20")

        mailto_link = f"mailto:?subject={subject_encoded}&body={body_encoded}"
        webbrowser.open(mailto_link)

    def set_language(self, lang):
        old_lang = self.language
        old_ingredients = self.get_ingredients()

        if old_lang == "FR" and lang == "NL":
            ingredient_mapping = INGREDIENTMAP_FR_TO_NL
            recipe_mapping = RECIPE_MAP_FR_TO_NL
        elif old_lang == "NL" and lang == "FR":
            ingredient_mapping = INGREDIENTMAP_NL_TO_FR
            recipe_mapping = RECIPE_MAP_NL_TO_FR
        elif old_lang == "FR" and lang == "EN":
            ingredient_mapping = INGREDIENTMAP_FR_TO_EN
            recipe_mapping = RECIPE_MAP_FR_TO_EN
        elif old_lang == "EN" and lang == "FR":
            ingredient_mapping = INGREDIENTMAP_EN_TO_FR
            recipe_mapping = RECIPE_MAP_EN_TO_FR
        elif old_lang == "NL" and lang == "EN":
            ingredient_mapping = INGREDIENTMAP_NL_TO_EN
            recipe_mapping = RECIPE_MAP_NL_TO_EN
        elif old_lang == "EN" and lang == "NL":
            ingredient_mapping = INGREDIENTMAP_EN_TO_NL
            recipe_mapping = RECIPE_MAP_EN_TO_NL
        else:
            ingredient_mapping = {i: i for i in old_ingredients}
            recipe_mapping = {r: r for r in RECIPE_NAMES[old_lang]}

        self.language = lang
        new_ingredients = self.get_ingredients()

        values = {}
        for old_name in old_ingredients:
            if old_name in self.entries:
                try:
                    values[ingredient_mapping[old_name]] = self.entries[old_name].get()
                except KeyError:
                    pass

        for i, ingredient in enumerate(new_ingredients):
            self.labels[i].config(text=f"{ingredient} :")
            self.entries[ingredient] = self.entries.pop(old_ingredients[i])

        for name, value in values.items():
            if name in self.entries:
                self.entries[name].delete(0, tk.END)
                self.entries[name].insert(0, value)

        for i, extra in enumerate(EXTRA_INGREDIENTS):
            self.extraname_entries[extra].delete(0, tk.END)
            self.extraname_entries[extra].insert(0, f"extra {i+1}" if lang in ["NL", "EN"] else f"supplémentaire {i+1}")

        self.update_language()

    def get_ingredients(self):
        if self.language == "FR":
            return INGREDIENTS_FR
        elif self.language == "NL":
            return INGREDIENTS_NL
        else:
            return INGREDIENTS_EN

    def get_conversions(self):
        if self.language == "FR":
            return CONVERSIONS_FR
        elif self.language == "NL":
            return CONVERSIONS_NL
        else:
            return CONVERSIONS_EN

    def get_recipe_names(self):
        return RECIPE_NAMES[self.language]

    def update_language(self):
        self.root.title(TEXTS[self.language]["title"])
        ingredients = self.get_ingredients()

        for i, ingredient in enumerate(ingredients):
            self.labels[i].config(text=f"{ingredient} :")

        self.calc_btn.config(text=TEXTS[self.language]["calculate"])
        self.reset_btn.config(text=TEXTS[self.language]["reset"])
        self.choose_btn.config(text=TEXTS[self.language]["choose_button"])
        self.recipe_label.config(text=TEXTS[self.language]["recipe_label"])
        self.close_btn.config(text=TEXTS[self.language]["close"])
        self.total_label.config(text=TEXTS[self.language]["total"])
        self.newtotal_label.config(text=TEXTS[self.language]["newtotal"])
        self.rescale_btn.config(text=TEXTS[self.language]["rescale"])

    def create_input_fields(self):
        ingredients = self.get_ingredients()
        row = 0
        for i, ingredient in enumerate(ingredients):
            label = ttk.Label(self.input_frame, text=f"{ingredient} :")
            label.grid(row=row, column=0, sticky="w")
            self.labels.append(label)

            entry = ttk.Entry(self.input_frame, width=10)
            entry.grid(row=row, column=1)
            entry.insert(0, "0")
            self.entries[ingredient] = entry
            row += 1

        for i, extra in enumerate(EXTRA_INGREDIENTS):
            name_entry = ttk.Entry(self.input_frame, width=15)
            name_entry.grid(row=row, column=0, sticky="w")
            name_entry.insert(0, f"supplémentaire {i+1}" if self.language == "FR" else f"extra {i+1}")
            self.extraname_entries[extra] = name_entry

            label = ttk.Label(self.input_frame, text="(g) :")
            label.grid(row=row, column=1, sticky="w")
            self.labels.append(label)

            value_entry = ttk.Entry(self.input_frame, width=10)
            value_entry.grid(row=row, column=2)
            value_entry.insert(0, "0")
            self.entries[extra] = value_entry
            row += 1

    def create_recipe_section(self):
        # Frame for recipe label and choose button
        recipe_frame = ttk.Frame(self.button_frame)
        recipe_frame.pack(pady=5)

        self.recipe_label = ttk.Label(recipe_frame, text="")
        self.recipe_label.pack(side="left", padx=5)

        self.choose_btn = ttk.Button(recipe_frame, text="", command=self.open_recipe_window)
        self.choose_btn.pack(side="left", padx=5)

        # New frame for calculate and reset buttons
        action_frame = ttk.Frame(self.button_frame)
        action_frame.pack(pady=5)

        self.calc_btn = ttk.Button(action_frame, text="", command=self.calculate_total)
        self.calc_btn.pack(side="left", padx=5)

        self.reset_btn = ttk.Button(action_frame, text="", command=self.reset_values)
        self.reset_btn.pack(side="left", padx=5)

    def open_recipe_window(self):
        recipe_window = tk.Toplevel(self.root)
        recipe_window.title(TEXTS[self.language]["recipe_window_title"])
        recipe_window.geometry("300x500")
        recipe_window.resizable(False, False)

        header_label = ttk.Label(recipe_window, text=TEXTS[self.language]["recipe_header"], wraplength=250, justify="center")
        header_label.pack(pady=10)

        listbox = tk.Listbox(recipe_window, height=14, width=30)
        listbox.pack(pady=10)

        for recipe in self.get_recipe_names():
            listbox.insert(tk.END, recipe)

        def on_select(event):
            selection = listbox.curselection()
            if selection:
                selected_recipe = listbox.get(selection[0])
                self.load_recipe(selected_recipe)
                recipe_window.destroy()

        listbox.bind('<<ListboxSelect>>', on_select)

    def load_recipe(self, selected_recipe):
        # Map the selected recipe to the NL key (since RECIPES uses NL keys)
        if self.language == "FR":
            recipe_key = RECIPE_MAP_FR_TO_NL.get(selected_recipe, selected_recipe)
        elif self.language == "EN":
            recipe_key = RECIPE_MAP_EN_TO_NL.get(selected_recipe, selected_recipe)
        else:
            recipe_key = selected_recipe

        # Reset all fields to 0
        self.reset_values()

        # Get the recipe data
        recipe_data = RECIPES.get(recipe_key, {})

        # Map NL ingredients to current language
        ingredients = self.get_ingredients()
        if self.language == "FR":
            ingredient_mapping = INGREDIENTMAP_NL_TO_FR
        elif self.language == "EN":
            ingredient_mapping = INGREDIENTMAP_NL_TO_EN
        else:
            ingredient_mapping = {i: i for i in INGREDIENTS_NL}

        # Populate fields
        for nl_ingredient, value in recipe_data.items():
            ingredient = ingredient_mapping.get(nl_ingredient, nl_ingredient)
            if ingredient in self.entries:
                self.entries[ingredient].delete(0, tk.END)
                self.entries[ingredient].insert(0, f"{value:.2f}")
            elif nl_ingredient == "extra 1":
                self.extraname_entries["extra 1"].delete(0, tk.END)
                self.extraname_entries["extra 1"].insert(0, "room (g)" if self.language == "NL" else "crème (g)" if self.language == "FR" else "cream (g)")
                self.entries["extra 1"].delete(0, tk.END)
                self.entries["extra 1"].insert(0, f"{value:.2f}")
            elif nl_ingredient == "extra 2":
                self.extraname_entries["extra 2"].delete(0, tk.END)
                self.extraname_entries["extra 2"].insert(0, "extra 2")
                self.entries["extra 2"].delete(0, tk.END)
                self.entries["extra 2"].insert(0, f"{value:.2f}")
            elif nl_ingredient == "extra 3":
                self.extraname_entries["extra 3"].delete(0, tk.END)
                self.extraname_entries["extra 3"].insert(0, "extra 3")
                self.entries["extra 3"].delete(0, tk.END)
                self.entries["extra 3"].insert(0, f"{value:.2f}")

        self.calculate_total()

    def create_total_display(self):
        self.total_label = ttk.Label(self.total_frame, text="")
        self.total_label.grid(row=0, column=0, sticky="w")

        self.total_entry = ttk.Entry(self.total_frame, textvariable=self.total_var, font=("Arial", 12), width=20, state="readonly")
        self.total_entry.grid(row=0, column=1)

    def create_rescale_section(self):
        self.newtotal_label = ttk.Label(self.rescale_frame, text="")
        self.newtotal_label.grid(row=0, column=0)

        self.newtotal_entry = ttk.Entry(self.rescale_frame, textvariable=self.newtotal_var, width=10, state="readonly")
        self.newtotal_entry.grid(row=0, column=1)

        self.rescale_btn = ttk.Button(self.rescale_frame, text="", command=self.open_multiplication_window)
        self.rescale_btn.grid(row=0, column=2, padx=5)

    def open_multiplication_window(self):
        mult_window = tk.Toplevel(self.root)
        mult_window.title(TEXTS[self.language]["multiplication_window_title"])
        mult_window.geometry("350x280")

        mult_frame = ttk.Frame(mult_window)
        mult_frame.pack(padx=10, pady=10)

        self.left_entries = []
        self.right_entries = []

        for i in range(7):
            left_entry = ttk.Entry(mult_frame, width=10)
            left_entry.grid(row=i, column=0, pady=5)
            left_entry.insert(0, "0")
            self.left_entries.append(left_entry)

            ttk.Label(mult_frame, text=TEXTS[self.language]["multiplication_label"]).grid(row=i, column=1, padx=5)

            right_entry = ttk.Entry(mult_frame, width=10)
            right_entry.grid(row=i, column=2, pady=5)
            right_entry.insert(0, "0")
            self.right_entries.append(right_entry)

            ttk.Label(mult_frame, text=TEXTS[self.language]["value_label"]).grid(row=i, column=3, padx=5)

        enter_btn = ttk.Button(mult_frame, text=TEXTS[self.language]["enter_button"], command=lambda: self.process_multiplication(mult_window))
        enter_btn.grid(row=7, column=0, columnspan=4, pady=10)

    def process_multiplication(self, mult_window):
        total = 0
        for left_entry, right_entry in zip(self.left_entries, self.right_entries):
            try:
                left_value = float(left_entry.get().replace(",", "."))
                right_value = float(right_entry.get().replace(",", "."))
                if left_value < 0 or right_value < 0:
                    raise ValueError
                total += left_value * right_value
            except ValueError:
                continue

        if total <= 0:
            messagebox.showerror(TEXTS[self.language]["error_title"], TEXTS[self.language]["error_value"])
            return

        self.newtotal_var.set(f"{round(total, 2)}")
        self.rescale_values(total)
        mult_window.destroy()

    def reset_values(self):
        for entry in self.entries.values():
            entry.delete(0, tk.END)
            entry.insert(0, "0")
        for i, extra in enumerate(EXTRA_INGREDIENTS):
            self.extraname_entries[extra].delete(0, tk.END)
            self.extraname_entries[extra].insert(0, f"supplémentaire {i+1}" if self.language == "FR" else f"extra {i+1}")
        self.total_var.set("0 g")
        self.newtotal_var.set("0")

    def calculate_total(self):
        total = 0
        conversions = self.get_conversions()

        for ingredient, entry in self.entries.items():
            try:
                value = float(entry.get().replace(",", "."))
                if value < 0:
                    value = 0
            except ValueError:
                value = 0

            if ingredient in conversions:
                total += conversions[ingredient](value)
            else:
                total += value

        self.total_var.set(f"{round(total, 2)} g")

    def rescale_values(self, new_total):
        current_total = 0
        values = {}
        conversions = self.get_conversions()

        for ingredient, entry in self.entries.items():
            try:
                value = float(entry.get().replace(",", "."))
                if value < 0:
                    value = 0
            except ValueError:
                value = 0

            if ingredient in conversions:
                weight = conversions[ingredient](value)
            else:
                weight = value

            values[ingredient] = (value, weight)
            current_total += weight

        if current_total == 0:
            messagebox.showerror(TEXTS[self.language]["error_title"], TEXTS[self.language]["error_zero"])
            return

        factor = new_total / current_total

        for ingredient, (original_input, weight) in values.items():
            new_input = original_input * factor
            self.entries[ingredient].delete(0, tk.END)
            self.entries[ingredient].insert(0, round(new_input, 2))

        self.calculate_total()

if __name__ == "__main__":
    root = tk.Tk()
    app = IngredientApp(root)
    root.mainloop()

