#!/usr/bin/env python3

import importlib
import os
import subprocess
import sys
import tempfile
import urllib.parse
import webbrowser
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.simpledialog import askstring
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import xml.etree.ElementTree as ET
import re

REQUIRED_LIBRARIES = ['tkinter', 'reportlab']

EXTRA_INGREDIENTS = ["extra 1", "extra 2", "extra 3"]

LANGUAGES = ["NL", "FR", "EN", "DE", "ES", "IT"]

TEXTS = {
    "FR": {
        "title": "Calculateur d'ingrédients",
        "calculate": "Calculer le total",
        "reset": "Réinitialiser",
        "close": "Fermer",
        "cancel": "Annuler",
        "total": "Poids total :",
        "newtotal": "Nouveau poids total :",
        "rescale": "Recalculer",
        "error_title": "Erreur",
        "error_value": "Entrez un nombre positif valide pour le nouveau poids total.",
        "error_zero": "Le poids total actuel est 0. Impossible de recalculer.",
        "error_combination": "Impossible de combiner les calculs par pièce avec la multiplication ou la division.",
        "error_multiply_divide": "Impossible d'utiliser à la fois la multiplication et la division.",
        "pdf_prompt": "Entrez le nom du fichier PDF :",
        "pdf_saved": "PDF enregistré sous :",
        "print_prompt": "Entrez le titre de la recette :",
        "print_error": "Impossible d'envoyer le document à l'imprimante. Vérifiez la configuration de l'imprimante.",
        "multiplication_window_title": "Calcul de multiplication",
        "multiplication_label": " x ",
        "value_label": " g ",
        "multiply_by": "Multiplier par :",
        "divide_by": "Diviser par :",
        "enter_button": "Entrer",
        "recipe_label": "Recettes de pâte de base :",
        "choose_button": "Choisir",
        "recipe_window_title": "Choisir une recette",
        "recipe_header": "Quelques recettes de base. Cliquez sur une recette pour sélectionner !",
        "language_label": "Choix de langue :",
        "xml_error": "Erreur lors du chargement de {file} : {error}"
    },
    "NL": {
        "title": "Ingrediënten Calculator",
        "calculate": "Bereken totaal",
        "reset": "Reset",
        "close": "Sluiten",
        "cancel": "Annuleren",
        "total": "Totaal gewicht :",
        "newtotal": "Nieuw totaalgewicht :",
        "rescale": "Herberekenen",
        "error_title": "Fout",
        "error_value": "Voer een geldig positief getal in voor het nieuwe totaalgewicht.",
        "error_zero": "Het huidige totaalgewicht is 0. Kan niet herberekenen.",
        "error_combination": "Kan per-stuk berekeningen niet combineren met vermenigvuldigen of delen.",
        "error_multiply_divide": "Kan niet zowel vermenigvuldigen als delen gebruiken.",
        "pdf_prompt": "Geef naam voor het PDF-bestand :",
        "pdf_saved": "PDF opgeslagen als :",
        "print_prompt": "Voer de titel in van het recept :",
        "print_error": "Kan document niet naar printer verzenden. Controleer de printerinstellingen.",
        "multiplication_window_title": "Multiplicatie Berekening",
        "multiplication_label": " x ",
        "value_label": " g ",
        "multiply_by": "Vermenigvuldigen met :",
        "divide_by": "Delen door :",
        "enter_button": "Invoeren",
        "recipe_label": "Basis deeg recepten :",
        "choose_button": "Kies",
        "recipe_window_title": "Kies een recept",
        "recipe_header": "Enkele basis recepten. Klik op een recept om te selecteren !",
        "language_label": "Taalkeuze :",
        "xml_error": "Fout bij het laden van {file} : {error}"
    },
    "EN": {
        "title": "Ingredient Calculator",
        "calculate": "Calculate total",
        "reset": "Reset",
        "close": "Close",
        "cancel": "Cancel",
        "total": "Total weight :",
        "newtotal": "New total weight :",
        "rescale": "Rescale",
        "error_title": "Error",
        "error_value": "Enter a valid positive number for the new total weight.",
        "error_zero": "The current total weight is 0. Cannot rescale.",
        "error_combination": "Cannot combine per-piece calculations with multiplication or division.",
        "error_multiply_divide": "Cannot use both multiply and divide operations.",
        "pdf_prompt": "Enter the PDF file name :",
        "pdf_saved": "PDF saved as :",
        "print_prompt": "Enter the recipe title :",
        "print_error": "Cannot send document to printer. Check printer settings.",
        "multiplication_window_title": "Multiplication Calculation",
        "multiplication_label": " x ",
        "value_label": " g ",
        "multiply_by": "Multiply by :",
        "divide_by": "Divide by :",
        "enter_button": "Enter",
        "recipe_label": "Basic dough recipes :",
        "choose_button": "Choose",
        "recipe_window_title": "Choose a recipe",
        "recipe_header": "Some basic recipes. Click on a recipe to select !",
        "language_label": "Language choice :",
        "xml_error": "Error loading {file}: {error}"
    },
    "DE": {
        "title": "Zutatenrechner",
        "calculate": "Gesamtgewicht berechnen",
        "reset": "Zurücksetzen",
        "close": "Schließen",
        "cancel": "Abbrechen",
        "total": "Gesamtgewicht :",
        "newtotal": "Neues Gesamtgewicht :",
        "rescale": "Neu berechnen",
        "error_title": "Fehler",
        "error_value": "Geben Sie eine gültige positive Zahl für das neue Gesamtgewicht ein.",
        "error_zero": "Das aktuelle Gesamtgewicht ist 0. Kann nicht neu berechnet werden.",
        "error_combination": "Kann Stückberechnungen nicht mit Multiplikation oder Division kombinieren.",
        "error_multiply_divide": "Kann nicht sowohl Multiplikation als auch Division verwenden.",
        "pdf_prompt": "Geben Sie den Namen der PDF-Datei ein :",
        "pdf_saved": "PDF gespeichert als :",
        "print_prompt": "Geben Sie den Titel des Rezepts ein :",
        "print_error": "Dokument kann nicht an den Drucker gesendet werden. Überprüfen Sie die Druckereinstellungen.",
        "multiplication_window_title": "Multiplikationsberechnung",
        "multiplication_label": " x ",
        "value_label": " g ",
        "multiply_by": "Multiplizieren mit :",
        "divide_by": "Dividieren durch :",
        "enter_button": "Eingeben",
        "recipe_label": "Grundteigrezepturen :",
        "choose_button": "Auswählen",
        "recipe_window_title": "Rezept auswählen",
        "recipe_header": "Einige Grundrezepte. Klicken Sie auf ein Rezept, um es auszuwählen !",
        "language_label": "Sprachauswahl :",
        "xml_error": "Fehler beim Laden von {file}: {error}"
    },
    "ES": {
        "title": "Calculadora de ingredientes",
        "calculate": "Calcular el total",
        "reset": "Restablecer",
        "close": "Cerrar",
        "cancel": "Cancelar",
        "total": "Peso total :",
        "newtotal": "Nuevo peso total :",
        "rescale": "Recalcular",
        "error_title": "Error",
        "error_value": "Introduzca un número positivo válido para el nuevo peso total.",
        "error_zero": "El peso total actual es 0. No se puede recalcular.",
        "error_combination": "No se pueden combinar cálculos por pieza con multiplicación o división.",
        "error_multiply_divide": "No se pueden usar operaciones de multiplicación y división juntas.",
        "pdf_prompt": "Introduzca el nombre del archivo PDF :",
        "pdf_saved": "PDF guardado como :",
        "print_prompt": "Introduzca el título de la receta :",
        "print_error": "No se puede enviar el documento a la impresora. Verifique la configuración de la impresora.",
        "multiplication_window_title": "Cálculo de multiplicación",
        "multiplication_label": " x ",
        "value_label": " g ",
        "multiply_by": "Multiplicar por :",
        "divide_by": "Dividir por :",
        "enter_button": "Ingresar",
        "recipe_label": "Recetas de masa básica :",
        "choose_button": "Elegir",
        "recipe_window_title": "Elegir una receta",
        "recipe_header": "Algunas recetas básicas. ¡Haga clic en una receta para seleccionarla !",
        "language_label": "Elección de idioma :",
        "xml_error": "Error al cargar {file}: {error}"
    },
    "IT": {
        "title": "Calcolatore di ingredienti",
        "calculate": "Calcola il totale",
        "reset": "Ripristina",
        "close": "Chiudi",
        "cancel": "Annulla",
        "total": "Peso totale :",
        "newtotal": "Nuovo peso totale :",
        "rescale": "Ricalcola",
        "error_title": "Errore",
        "error_value": "Inserisci un numero positivo valido per il nuovo peso totale.",
        "error_zero": "Il peso totale attuale è 0. Impossibile ricalcolare.",
        "error_combination": "Impossibile combinare calcoli per pezzo con moltiplicazione o divisione.",
        "error_multiply_divide": "Impossibile utilizzare sia la moltiplicazione che la divisione.",
        "pdf_prompt": "Inserisci il nome del file PDF :",
        "pdf_saved": "PDF salvato come :",
        "print_prompt": "Inserisci il titolo della ricetta :",
        "print_error": "Impossibile inviare il documento alla stampante. Controlla le impostazioni della stampante.",
        "multiplication_window_title": "Calcolo di moltiplicazione",
        "multiplication_label": " x ",
        "value_label": " g ",
        "multiply_by": "Moltiplicare per :",
        "divide_by": "Dividere per :",
        "enter_button": "Inserisci",
        "recipe_label": "Ricette di impasto base :",
        "choose_button": "Scegli",
        "recipe_window_title": "Scegli una ricetta",
        "recipe_header": "Alcune ricette base. Clicca su una ricetta per selezionarla !",
        "language_label": "Scelta della lingua :",
        "xml_error": "Errore durante il caricamento di {file}: {error}"
    }
}

def normalize_ingredient_name(name):
    """Normalize ingredient names by removing units and converting to lowercase."""
    return re.sub(r'\s*\(g\)\s*|\s*\(ml\)\s*', '', name, flags=re.IGNORECASE).lower()

def load_ingredients():
    """Load ingredients and their translations from BakeryTool1.xml."""
    file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "BakeryTool1.xml"))
    print(f"Attempting to load BakeryTool1.xml from: {file_path}")
    if not os.path.exists(file_path):
        messagebox.showerror(TEXTS["EN"]["error_title"], TEXTS["EN"]["xml_error"].format(file="BakeryTool1.xml", error=f"File not found at {file_path}"))
        sys.exit(1)
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        ingredients = {lang: [] for lang in LANGUAGES}

        for ingredient_elem in root.findall("ingredient"):
            nl_name = ingredient_elem.get("name")
            if nl_name and (ingredient_elem.get("lang") == "NL" or not ingredient_elem.get("lang")):
                normalized_name = normalize_ingredient_name(nl_name)
                ingredients["NL"].append(nl_name)
                for trans_elem in ingredient_elem.findall("translations/translation"):
                    lang = trans_elem.get("lang")
                    if lang in ingredients:
                        ingredients[lang].append(trans_elem.text)

        return ingredients
    except ET.ParseError as e:
        messagebox.showerror(TEXTS["EN"]["error_title"], TEXTS["EN"]["xml_error"].format(file="BakeryTool1.xml", error=f"Parse error: {str(e)}"))
        sys.exit(1)
    except PermissionError:
        messagebox.showerror(TEXTS["EN"]["error_title"], TEXTS["EN"]["xml_error"].format(file="BakeryTool1.xml", error="Permission denied"))
        sys.exit(1)

def load_conversions():
    """Load conversion factors from BakeryTool3.xml."""
    file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "BakeryTool3.xml"))
    print(f"Attempting to load BakeryTool3.xml from: {file_path}")
    if not os.path.exists(file_path):
        messagebox.showerror(TEXTS["EN"]["error_title"], TEXTS["EN"]["xml_error"].format(file="BakeryTool3.xml", error=f"File not found at {file_path}"))
        sys.exit(1)
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        conversions = {lang: {} for lang in LANGUAGES}

        for ingredient_elem in root.findall("ingredient"):
            nl_name = ingredient_elem.get("name")
            if nl_name:
                normalized_name = normalize_ingredient_name(nl_name)
                conversion_elem = ingredient_elem.find("conversion")
                factor = float(conversion_elem.get("factor")) if conversion_elem is not None else 1.0
                for lang in LANGUAGES:
                    if lang == "NL":
                        conversions[lang][nl_name] = lambda x, f=factor: x * f
                    else:
                        translated_name = None
                        for orig_name, trans_name in INGREDIENT_MAPS.get(("NL", lang), {}).items():
                            if normalize_ingredient_name(orig_name) == normalized_name:
                                translated_name = trans_name
                                break
                        if translated_name:
                            conversions[lang][translated_name] = lambda x, f=factor: x * f
                        else:
                            conversions[lang][nl_name] = lambda x, f=factor: x * f

        return conversions
    except ET.ParseError as e:
        messagebox.showerror(TEXTS["EN"]["error_title"], TEXTS["EN"]["xml_error"].format(file="BakeryTool3.xml", error=f"Parse error: {str(e)}"))
        sys.exit(1)
    except PermissionError:
        messagebox.showerror(TEXTS["EN"]["error_title"], TEXTS["EN"]["xml_error"].format(file="BakeryTool3.xml", error="Permission denied"))
        sys.exit(1)

def load_recipes():
    """Load recipes and their translations from BakeryTool2.xml."""
    file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "BakeryTool2.xml"))
    print(f"Attempting to load BakeryTool2.xml from: {file_path}")
    if not os.path.exists(file_path):
        messagebox.showerror(TEXTS["EN"]["error_title"], TEXTS["EN"]["xml_error"].format(file="BakeryTool2.xml", error=f"File not found at {file_path}"))
        sys.exit(1)
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        recipes = {}
        recipe_names = {lang: [] for lang in LANGUAGES}

        for recipe_elem in root.findall("recipe"):
            nl_name = recipe_elem.get("name")
            if nl_name:
                recipe_names["NL"].append(nl_name)
                recipes[nl_name] = {}

                for trans_elem in recipe_elem.findall("translations/translation"):
                    lang = trans_elem.get("lang")
                    if lang in recipe_names:
                        recipe_names[lang].append(trans_elem.text)

                for ing_elem in recipe_elem.findall("ingredients/ingredient"):
                    ing_name = ing_elem.get("name")
                    normalized_ing_name = normalize_ingredient_name(ing_name)
                    amount = float(ing_elem.get("amount"))
                    recipes[nl_name][ing_name] = amount

        return recipes, recipe_names
    except ET.ParseError as e:
        messagebox.showerror(TEXTS["EN"]["error_title"], TEXTS["EN"]["xml_error"].format(file="BakeryTool2.xml", error=f"Parse error: {str(e)}"))
        sys.exit(1)
    except PermissionError:
        messagebox.showerror(TEXTS["EN"]["error_title"], TEXTS["EN"]["xml_error"].format(file="BakeryTool2.xml", error="Permission denied"))
        sys.exit(1)

INGREDIENTS = load_ingredients()

INGREDIENT_MAPS = {}
for source_lang in LANGUAGES:
    for target_lang in LANGUAGES:
        if source_lang != target_lang:
            INGREDIENT_MAPS[(source_lang, target_lang)] = dict(zip(INGREDIENTS[source_lang], INGREDIENTS[target_lang]))
            INGREDIENT_MAPS[(target_lang, source_lang)] = dict(zip(INGREDIENTS[target_lang], INGREDIENTS[source_lang]))

CONVERSIONS = load_conversions()
RECIPES, RECIPE_NAMES = load_recipes()

RECIPE_MAPS = {}
for source_lang in LANGUAGES:
    for target_lang in LANGUAGES:
        if source_lang != target_lang:
            RECIPE_MAPS[(source_lang, target_lang)] = dict(zip(RECIPE_NAMES[source_lang], RECIPE_NAMES[target_lang]))
            RECIPE_MAPS[(target_lang, source_lang)] = dict(zip(RECIPE_NAMES[target_lang], RECIPE_NAMES[source_lang]))

class AutoCloseMessageBox:
    """A message box that automatically closes after a specified duration."""
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
    """Check for required libraries and install them if missing on Linux."""
    for lib in REQUIRED_LIBRARIES:
        try:
            importlib.import_module(lib)
            message = AutoCloseMessageBox("Info", f"Bakery Tool - {lib} found", 2000)
            root.update()
            while message.top.winfo_exists():
                root.update()
        except ImportError:
            message = AutoCloseMessageBox("Info", f"Installing {lib}...", 3000)
            root.update()
            while message.top.winfo_exists():
                root.update()
            try:
                if lib == 'tkinter':
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
            except subprocess.CalledProcessError:
                message = AutoCloseMessageBox("Error", f"Failed to install {lib}. Ensure pip is configured correctly or install manually.", 5000)
                root.update()
                while message.top.winfo_exists():
                    root.update()
                sys.exit(1)

class IngredientApp:
    """Main application class for the ingredient calculator GUI."""
    def __init__(self, root):
        self.root = root
        self.language = "FR"
        self.entries = {}
        self.extraname_entries = {}
        self.labels = []
        self.total_var = tk.StringVar(value="0 g")
        self.newtotal_var = tk.StringVar(value="0")
        self.recipe_window = None
        self.mult_window = None
        self.buttons = []  
        self.language_menu = None  

        self.input_frame = ttk.Frame(self.root)
        self.input_frame.pack(padx=10, pady=10)
        self.button_frame = ttk.Frame(self.root)
        self.button_frame.pack(pady=5)
        self.total_frame = ttk.Frame(self.root)
        self.total_frame.pack(pady=5)
        self.rescale_frame = ttk.Frame(self.root)
        self.rescale_frame.pack(pady=10)

        check_and_install_libraries(self.root)

        self.create_language_menu()
        self.create_input_fields()
        self.create_recipe_section()
        self.create_total_display()
        self.create_rescale_section()
        self.update_language()

    def disable_ui_elements(self):
        """Disable all buttons (except close), language combobox, and input fields."""
        for button in self.buttons:
            button.config(state="disabled")
        if self.language_menu:
            self.language_menu.config(state="disabled")
        for entry in self.entries.values():
            entry.config(state="disabled")
        for entry in self.extraname_entries.values():
            entry.config(state="disabled")

    def enable_ui_elements(self):
        """Enable all buttons (except close), language combobox, and input fields."""
        for button in self.buttons:
            button.config(state="normal")
        if self.language_menu:
            self.language_menu.config(state="readonly")
        for entry in self.entries.values():
            entry.config(state="normal")
        for entry in self.extraname_entries.values():
            entry.config(state="normal")

    def create_language_menu(self):
        """Create the language selection menu and related buttons."""
        main_frame = ttk.Frame(self.root)
        main_frame.pack(pady=5)

        self.top_frame = ttk.Frame(main_frame)
        self.top_frame.pack()

        self.language_label = ttk.Label(self.top_frame, text=TEXTS[self.language]["language_label"])
        self.language_label.pack(side="left", padx=5)

        language_var = tk.StringVar(value="English")
        self.language_menu = ttk.Combobox(self.top_frame, textvariable=language_var,
                                         values=["English", "Français", "Nederlands", "Deutsch", "Español", "Italiano"],
                                         state="readonly", width=10)
        self.language_menu.pack(side="left", padx=5)
        self.language_menu.current(0)
        self.language_menu.bind("<<ComboboxSelected>>", self.on_language_select)

        mail_btn = ttk.Button(self.top_frame, text="Mail", command=self.send_email)
        mail_btn.pack(side="left", padx=5)
        self.buttons.append(mail_btn)

        pdf_button = ttk.Frame(main_frame)
        pdf_button.pack(pady=(10, 0))

        pdf_btn = ttk.Button(pdf_button, text="PDF", command=self.generate_pdf)
        pdf_btn.pack(side="left", padx=5)
        self.buttons.append(pdf_btn)

        print_btn = ttk.Button(pdf_button, text="PRINT", command=self.print_document)
        print_btn.pack(side="left", padx=5)
        self.buttons.append(print_btn)

        self.close_btn = ttk.Button(pdf_button, text="", command=self.root.destroy)
        self.close_btn.pack(side="left", padx=5)

    def on_language_select(self, event):
        """Handle language selection change."""
        language_map = {
            "English": "EN",
            "Français": "FR",
            "Nederlands": "NL",
            "Deutsch": "DE",
            "Español": "ES",
            "Italiano": "IT"
        }
        selected_language = event.widget.get()
        self.set_language(language_map[selected_language])

    def generate_pdf(self):
        """Generate a PDF file with the current ingredient values."""
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
        """Print the current ingredient values to a PDF and send to printer on Linux."""
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
                messagebox.showerror(TEXTS["EN"]["error_title"], f"{TEXTS[self.language]['print_error']} lp command not found.")
        finally:
            try:
                os.unlink(filepath)
            except Exception:
                pass

    def send_email(self):
        """Send the current ingredient values via email."""
        subject = {
            "NL": "recept",
            "EN": "recipe",
            "FR": "recette",
            "DE": "Rezept",
            "ES": "receta",
            "IT": "ricetta"
        }.get(self.language, "recipe")

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
        subject_encoded = urllib.parse.quote(subject)
        body_encoded = urllib.parse.quote(body)
        mailto_link = f"mailto:?subject={subject_encoded}&body={body_encoded}"
        webbrowser.open(mailto_link)

    def set_language(self, lang):
        """Switch the application language and update UI elements."""
        old_lang = self.language
        old_ingredients = self.get_ingredients()

        ingredient_mapping = INGREDIENT_MAPS.get((old_lang, lang), {i: i for i in old_ingredients})
        recipe_mapping = RECIPE_MAPS.get((old_lang, lang), {r: r for r in RECIPE_NAMES[old_lang]})

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
                self.entries[name].config(state="normal")  
                self.entries[name].delete(0, tk.END)
                self.entries[name].insert(0, value)
                self.entries[name].config(state="disabled" if self.recipe_window or self.mult_window else "normal")  

        for i, extra in enumerate(EXTRA_INGREDIENTS):
            self.extraname_entries[extra].config(state="normal")  
            self.extraname_entries[extra].delete(0, tk.END)
            extra_name = {
                "FR": f"supplémentaire {i+1}",
                "DE": f"zusätzlich {i+1}",
                "ES": f"extra {i+1}",
                "IT": f"extra {i+1}",
                "NL": f"extra {i+1}",
                "EN": f"extra {i+1}"
            }.get(self.language, f"extra {i+1}")
            self.extraname_entries[extra].insert(0, extra_name)
            self.extraname_entries[extra].config(state="disabled" if self.recipe_window or self.mult_window else "normal")  

        self.update_language()

    def get_ingredients(self):
        """Return the ingredient list for the current language."""
        return INGREDIENTS.get(self.language, INGREDIENTS["EN"])

    def get_conversions(self):
        """Return the conversion dictionary for the current language."""
        return CONVERSIONS.get(self.language, CONVERSIONS["EN"])

    def get_recipe_names(self):
        """Return the recipe names for the current language."""
        return RECIPE_NAMES[self.language]

    def update_language(self):
        """Update UI text to reflect the current language."""
        self.root.title(TEXTS[self.language]["title"])
        self.calc_btn.config(text=TEXTS[self.language]["calculate"])
        self.reset_btn.config(text=TEXTS[self.language]["reset"])
        self.choose_btn.config(text=TEXTS[self.language]["choose_button"])
        self.recipe_label.config(text=TEXTS[self.language]["recipe_label"])
        self.close_btn.config(text=TEXTS[self.language]["close"])
        self.total_label.config(text=TEXTS[self.language]["total"])
        self.newtotal_label.config(text=TEXTS[self.language]["newtotal"])
        self.rescale_btn.config(text=TEXTS[self.language]["rescale"])
        self.language_label.config(text=TEXTS[self.language]["language_label"])

    def create_input_fields(self):
        """Create input fields for ingredients and extra ingredients."""
        ingredients = self.get_ingredients()
        row = 0
        for ingredient in ingredients:
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
            extra_name = {
                "FR": f"supplémentaire {i+1}",
                "DE": f"zusätzlich {i+1}",
                "ES": f"extra {i+1}",
                "IT": f"extra {i+1}",
                "NL": f"extra {i+1}",
                "EN": f"extra {i+1}"
            }.get(self.language, f"extra {i+1}")
            name_entry.insert(0, extra_name)
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
        """Create the recipe selection and action buttons."""
        recipe_frame = ttk.Frame(self.button_frame)
        recipe_frame.pack(pady=5)

        self.recipe_label = ttk.Label(recipe_frame, text="")
        self.recipe_label.pack(side="left", padx=5)

        self.choose_btn = ttk.Button(recipe_frame, text="", command=self.open_recipe_window)
        self.choose_btn.pack(side="left", padx=5)
        self.buttons.append(self.choose_btn)

        action_frame = ttk.Frame(self.button_frame)
        action_frame.pack(pady=5)

        self.calc_btn = ttk.Button(action_frame, text="", command=self.calculate_total)
        self.calc_btn.pack(side="left", padx=5)
        self.buttons.append(self.calc_btn)

        self.reset_btn = ttk.Button(action_frame, text="", command=self.reset_values)
        self.reset_btn.pack(side="left", padx=5)
        self.buttons.append(self.reset_btn)

    def open_recipe_window(self):
        """Open a recipe selection window or focus the existing one if already open."""
        if self.recipe_window and self.recipe_window.winfo_exists():
            self.recipe_window.lift()
            return

        self.disable_ui_elements()  

        self.recipe_window = tk.Toplevel(self.root)
        self.recipe_window.title(TEXTS[self.language]["recipe_window_title"])
        self.recipe_window.resizable(False, False)

        self.recipe_window.protocol("WM_DELETE_WINDOW", self.on_recipe_window_close)

        recipe_frame = ttk.Frame(self.recipe_window)
        recipe_frame.pack(padx=10, pady=10)

        header_label = ttk.Label(recipe_frame, text=TEXTS[self.language]["recipe_header"],
                                 wraplength=450, justify="center")
        header_label.pack(pady=10)

        listbox = tk.Listbox(recipe_frame, height=27, width=60)
        listbox.pack(pady=10)

        for recipe in self.get_recipe_names():
            listbox.insert(tk.END, recipe)

        def on_select(event):
            selection = listbox.curselection()
            if selection:
                selected_recipe = listbox.get(selection[0])
                self.load_recipe(selected_recipe)
                self.on_recipe_window_close()

        listbox.bind('<<ListboxSelect>>', on_select)

        cancel_btn = ttk.Button(recipe_frame, text=TEXTS[self.language]["cancel"], command=self.on_recipe_window_close)
        cancel_btn.pack(pady=10)

        self.recipe_window.update_idletasks()
        width = recipe_frame.winfo_reqwidth() + 20
        height = recipe_frame.winfo_reqheight() + 20
        self.recipe_window.geometry(f"{width}x{height}")

    def on_recipe_window_close(self):
        """Handle the recipe window closing."""
        if self.recipe_window:
            self.recipe_window.destroy()
            self.recipe_window = None
            self.enable_ui_elements()  

    def load_recipe(self, selected_recipe):
        """Load a selected recipe into the input fields."""
        recipe_key = RECIPE_MAPS.get((self.language, "NL"), {r: r for r in RECIPE_NAMES[self.language]}).get(selected_recipe, selected_recipe)
        self.reset_values()

        recipe_data = RECIPES.get(recipe_key, {})
        ingredient_mapping = INGREDIENT_MAPS.get(("NL", self.language), {i: i for i in INGREDIENTS["NL"]})

        for nl_ingredient, value in recipe_data.items():
            ingredient = ingredient_mapping.get(nl_ingredient, nl_ingredient) if nl_ingredient not in EXTRA_INGREDIENTS else nl_ingredient
            if ingredient in self.entries:
                self.entries[ingredient].config(state="normal")  
                self.entries[ingredient].delete(0, tk.END)
                self.entries[ingredient].insert(0, f"{value:.2f}")
                self.entries[ingredient].config(state="disabled")  
            if ingredient == "extra 1":
                self.extraname_entries["extra 1"].config(state="normal")  
                self.extraname_entries["extra 1"].delete(0, tk.END)
                extra_name = {
                    "NL": "Room (g)",
                    "FR": "Crème (g)",
                    "DE": "Sahne (g)",
                    "ES": "Nata (g)",
                    "IT": "Panna (g)",
                    "EN": "Cream (g)"
                }.get(self.language, "Cream (g)")
                self.extraname_entries["extra 1"].insert(0, extra_name)
                self.extraname_entries["extra 1"].config(state="disabled")  
                self.entries["extra 1"].config(state="normal")  
                self.entries["extra 1"].delete(0, tk.END)
                self.entries["extra 1"].insert(0, f"{value:.2f}")
                self.entries["extra 1"].config(state="disabled")  
            elif ingredient in ["extra 2", "extra 3"]:
                self.extraname_entries[ingredient].config(state="normal")  
                self.extraname_entries[ingredient].delete(0, tk.END)
                self.extraname_entries[ingredient].insert(0, ingredient)
                self.extraname_entries[ingredient].config(state="disabled")  
                self.entries[ingredient].config(state="normal")  
                self.entries[ingredient].delete(0, tk.END)
                self.entries[ingredient].insert(0, f"{value:.2f}")
                self.entries[ingredient].config(state="disabled")  

        self.calculate_total()

    def create_total_display(self):
        """Create the display for the total weight."""
        self.total_label = ttk.Label(self.total_frame, text="")
        self.total_label.grid(row=0, column=0, sticky="w")

        self.total_entry = ttk.Entry(self.total_frame, textvariable=self.total_var,
                                     font=("Arial", 12), width=20, state="readonly")
        self.total_entry.grid(row=0, column=1)

    def create_rescale_section(self):
        """Create the rescale section for adjusting total weight."""
        self.newtotal_label = ttk.Label(self.rescale_frame, text="")
        self.newtotal_label.grid(row=0, column=0)

        self.newtotal_entry = ttk.Entry(self.rescale_frame, textvariable=self.newtotal_var,
                                        width=10, state="readonly")
        self.newtotal_entry.grid(row=0, column=1)

        self.rescale_btn = ttk.Button(self.rescale_frame, text="", command=self.open_multiplication_window)
        self.rescale_btn.grid(row=0, column=2, padx=5)
        self.buttons.append(self.rescale_btn)

    def open_multiplication_window(self):
        """Open a multiplication window or focus the existing one if already open."""
        if self.mult_window and self.mult_window.winfo_exists():
            self.mult_window.lift()
            return

        self.disable_ui_elements()  

        self.mult_window = tk.Toplevel(self.root)
        self.mult_window.title(TEXTS[self.language]["multiplication_window_title"])
        self.mult_window.resizable(False, False)

        self.mult_window.protocol("WM_DELETE_WINDOW", self.on_mult_window_close)

        mult_frame = ttk.Frame(self.mult_window)
        mult_frame.pack(padx=10, pady=10)

        self.left_entries = []
        self.right_entries = []
        for i in range(7):
            left_entry = ttk.Entry(mult_frame, width=10)
            left_entry.grid(row=i, column=0, pady=5)
            left_entry.insert(0, "0")
            self.left_entries.append(left_entry)

            label = ttk.Label(mult_frame, text=TEXTS[self.language]["multiplication_label"])
            label.grid(row=i, column=1, padx=5)

            right_entry = ttk.Entry(mult_frame, width=10)
            right_entry.grid(row=i, column=2, pady=5)
            right_entry.insert(0, "0")
            self.right_entries.append(right_entry)

            label = ttk.Label(mult_frame, text=TEXTS[self.language]["value_label"])
            label.grid(row=i, column=3, padx=5)

        ttk.Label(mult_frame, text=TEXTS[self.language]["multiply_by"]).grid(row=7, column=0, pady=5)
        self.multiply_entry = ttk.Entry(mult_frame, width=10)
        self.multiply_entry.grid(row=7, column=1, pady=5)

        ttk.Label(mult_frame, text=TEXTS[self.language]["divide_by"]).grid(row=8, column=0, pady=5)
        self.divide_entry = ttk.Entry(mult_frame, width=10)
        self.divide_entry.grid(row=8, column=1, pady=5)

        button_frame = ttk.Frame(mult_frame)
        button_frame.grid(row=9, column=0, columnspan=4, pady=10)

        enter_btn = ttk.Button(button_frame, text=TEXTS[self.language]["enter_button"],
                               command=lambda: self.process_multiplication(self.mult_window))
        enter_btn.pack(side="left", padx=5)

        cancel_btn = ttk.Button(button_frame, text=TEXTS[self.language]["cancel"],
                                command=self.on_mult_window_close)
        cancel_btn.pack(side="left", padx=5)

        self.mult_window.update_idletasks()
        width = mult_frame.winfo_reqwidth() + 20
        height = mult_frame.winfo_reqheight() + 40
        self.mult_window.geometry(f"{width}x{height}")

    def on_mult_window_close(self):
        """Handle the multiplication window closing."""
        if self.mult_window:
            self.mult_window.destroy()
            self.mult_window = None
            self.enable_ui_elements()  

    def process_multiplication(self, mult_window):
        """Process multiplication and division factors or per-piece calculations."""
        has_per_piece = False
        total = 0
        for left_entry, right_entry in zip(self.left_entries, self.right_entries):
            try:
                left_value = float(left_entry.get().replace(",", "."))
                right_value = float(right_entry.get().replace(",", "."))
                if left_value < 0 or right_value < 0:
                    raise ValueError
                if left_value != 0 or right_value != 0:
                    has_per_piece = True
                total += left_value * right_value
            except ValueError:
                continue

        has_multiply = False
        has_divide = False
        try:
            multiply_factor = float(self.multiply_entry.get().replace(",", "."))
            if multiply_factor <= 0:
                raise ValueError
            has_multiply = True
        except ValueError:
            multiply_factor = 1

        try:
            divide_factor = float(self.divide_entry.get().replace(",", "."))
            if divide_factor <= 0:
                raise ValueError
            has_divide = True
        except ValueError:
            divide_factor = 1

        if has_per_piece and (has_multiply or has_divide):
            messagebox.showerror(TEXTS[self.language]["error_title"], TEXTS["EN"]["error_combination"])
            mult_window.destroy()
            self.mult_window = None
            self.enable_ui_elements()
            return

        if has_multiply and has_divide:
            messagebox.showerror(TEXTS[self.language]["error_title"], TEXTS[self.language]["error_multiply_divide"])
            mult_window.destroy()
            self.mult_window = None
            self.enable_ui_elements()
            return

        if has_per_piece:
            if total <= 0:
                messagebox.showerror(TEXTS[self.language]["error_title"], TEXTS[self.language]["error_value"])
                mult_window.destroy()
                self.mult_window = None
                self.enable_ui_elements()
                return
            self.newtotal_var.set(f"{round(total, 2)}")
            self.rescale_values(total)
            mult_window.destroy()
            self.mult_window = None
            self.enable_ui_elements()
            return

        try:
            current_total = float(self.total_var.get().replace(" g", "").replace(",", "."))
        except ValueError:
            current_total = 0

        if current_total <= 0:
            messagebox.showerror(TEXTS[self.language]["error_title"], TEXTS[self.language]["error_zero"])
            mult_window.destroy()
            self.mult_window = None
            self.enable_ui_elements()
            return

        new_total = current_total * multiply_factor / divide_factor

        if new_total <= 0:
            messagebox.showerror(TEXTS[self.language]["error_title"], TEXTS[self.language]["error_value"])
            mult_window.destroy()
            self.mult_window = None
            self.enable_ui_elements()
            return

        self.newtotal_var.set(f"{round(new_total, 2)}")
        self.rescale_values(new_total)
        mult_window.destroy()
        self.mult_window = None
        self.enable_ui_elements()

    def reset_values(self):
        """Reset all input fields to zero."""
        for entry in self.entries.values():
            entry.config(state="normal")  
            entry.delete(0, tk.END)
            entry.insert(0, "0")
            entry.config(state="disabled" if self.recipe_window or self.mult_window else "normal")  
        for i, extra in enumerate(EXTRA_INGREDIENTS):
            self.extraname_entries[extra].config(state="normal")  
            self.extraname_entries[extra].delete(0, tk.END)
            extra_name = {
                "FR": f"supplémentaire {i+1}",
                "DE": f"zusätzlich {i+1}",
                "ES": f"extra {i+1}",
                "IT": f"extra {i+1}",
                "NL": f"extra {i+1}",
                "EN": f"extra {i+1}"
            }.get(self.language, f"extra {i+1}")
            self.extraname_entries[extra].insert(0, extra_name)
            self.extraname_entries[extra].config(state="disabled" if self.recipe_window or self.mult_window else "normal")  
        self.total_var.set("0 g")
        self.newtotal_var.set("0")

    def calculate_total(self):
        """Calculate the total weight of ingredients."""
        total = 0
        conversions = self.get_conversions()

        for ingredient, entry in self.entries.items():
            try:
                value = float(entry.get().replace(",", "."))
                if value < 0:
                    value = 0
            except ValueError:
                value = 0

            total += conversions.get(ingredient, lambda x: x)(value)

        formatted_total = f"{round(total, 2)} g"
        self.total_var.set(formatted_total)
        self.newtotal_var.set(formatted_total.replace(" g", ""))

    def rescale_values(self, new_total):
        """Rescale ingredient values based on a new total weight."""
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

            weight = conversions.get(ingredient, lambda x: x)(value)
            values[ingredient] = (value, weight)
            current_total += weight

        if current_total == 0:
            messagebox.showerror(TEXTS[self.language]["error_title"], TEXTS[self.language]["error_zero"])
            return

        factor = new_total / current_total

        for ingredient, (original_input, _) in values.items():
            new_input = original_input * factor
            self.entries[ingredient].config(state="normal")  
            self.entries[ingredient].delete(0, tk.END)
            self.entries[ingredient].insert(0, round(new_input, 2))
            self.entries[ingredient].config(state="disabled")  

        self.calculate_total()

if __name__ == "__main__":
    root = tk.Tk()
    app = IngredientApp(root)
    root.mainloop()
