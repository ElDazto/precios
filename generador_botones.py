import tkinter as tk
from tkinter import messagebox, simpledialog
from tkinter import ttk
import json
import pyperclip
import sys
import os

# Crear la ventana principal
root = tk.Tk()
root.title("Generador de Botones")
root.geometry("770x600")

# Variable para mantener los datos de los botones cargados
button_data = []

def resource_path(relative_path):
    """Obtener el recurso correcto cuando el programa está empaquetado."""
    try:
        # PyInstaller crea una carpeta temporal y almacena el archivo ahí
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def load_buttons():
    global button_data
    try:
        with open(resource_path('buttons.json'), 'r') as file:
            data = json.load(file)
            button_data = data["buttons"]
    except FileNotFoundError:
        button_data = []
    except json.JSONDecodeError:
        button_data = []

    update_buttons()

def update_buttons():
    """Actualizar la interfaz con los botones actuales."""
    # Limpiar los botones actuales en ambas secciones
    for widget in offer_frame.winfo_children():
        if isinstance(widget, tk.Frame):
            widget.destroy()

    for widget in price_frame.winfo_children():
        if isinstance(widget, tk.Frame):
            widget.destroy()

    # Crear filas dinámicas para distribuir botones
    offer_row = None
    price_row = None
    offer_count = 0
    price_count = 0

    for button_info in button_data:
        if button_info["type"] == "offer":
            if offer_count % 6 == 0:
                offer_row = tk.Frame(offer_frame)
                offer_row.pack(fill="x", pady=5)
            create_button(button_info["label"], button_info["text"], offer_row)
            offer_count += 1

        elif button_info["type"] == "price":
            if price_count % 6 == 0:
                price_row = tk.Frame(price_frame)
                price_row.pack(fill="x", pady=5)
            create_button(button_info["label"], button_info["text"], price_row)
            price_count += 1

    # Actualizar los ComboBox
    update_comboboxes()

def update_comboboxes():
    """Actualizar las opciones de los ComboBox según el tipo de botón."""
    offer_labels = [button["label"] for button in button_data if button["type"] == "offer"]
    price_labels = [button["label"] for button in button_data if button["type"] == "price"]

    offer_combobox['values'] = offer_labels
    price_combobox['values'] = price_labels

    offer_combobox.set("")  # Limpiar selección actual
    price_combobox.set("")  # Limpiar selección actual

def create_button(label, text, parent_frame):
    """Crear un botón en el contenedor especificado."""
    def copy_to_clipboard():
        pyperclip.copy(text)

    button = tk.Button(parent_frame, text=label, command=copy_to_clipboard, width=15, height=2)
    button.pack(side="left", padx=5, pady=5)

def save_buttons():
    """Guardar la lista actual de botones en el archivo JSON."""
    with open(resource_path('buttons.json'), 'r') as file:
        json.dump({"buttons": button_data}, file, indent=4)

def add_button(type_):
    """Agregar un botón con el tipo especificado."""
    global button_data
    label = simpledialog.askstring("Etiqueta del botón", "Ingrese el texto del botón:")
    text = simpledialog.askstring("Texto a copiar", "Ingrese el texto que se copiará:")

    if label and text:
        new_button = {"label": label, "text": text, "type": type_}
        button_data.append(new_button)
        save_buttons()
        update_buttons()
    else:
        messagebox.showerror("Error", "Debe ingresar todos los datos.")

def remove_button(type_):
    """Eliminar un botón según el tipo especificado."""
    global button_data
    if type_ == "offer":
        selected_label = offer_combobox.get()
    elif type_ == "price":
        selected_label = price_combobox.get()

    if not selected_label:
        messagebox.showinfo("Seleccionar botón", "Por favor, seleccione un botón para eliminar.")
        return

    confirm = messagebox.askyesno("Confirmar eliminación", f"¿Está seguro de que desea eliminar el botón '{selected_label}'?")
    if confirm:
        button_data = [button for button in button_data if button["label"] != selected_label]
        save_buttons()
        update_buttons()
        messagebox.showinfo("Eliminado", f"El botón '{selected_label}' ha sido eliminado.")

# Contenedor principal para Offer Buttons y sus controles
offer_frame = tk.LabelFrame(root, text="Oferta", font=("Arial", 14, "bold"), bd=2, relief="sunken", padx=10, pady=10)
offer_frame.pack(pady=(10, 0), padx=10, fill="x")

# Controles para Offer
offer_controls = tk.Frame(root)
offer_controls.pack(pady=(5, 10), padx=10, fill="x")

add_offer_button = tk.Button(offer_controls, text="Agregar", command=lambda: add_button("offer"))
add_offer_button.pack(side="left", padx=10)

offer_combobox = ttk.Combobox(offer_controls, state="readonly", width=30)
offer_combobox.pack(side="left", padx=10)

remove_offer_button = tk.Button(offer_controls, text="Eliminar", command=lambda: remove_button("offer"))
remove_offer_button.pack(side="left", padx=10)

# Contenedor principal para Price Buttons y sus controles
price_frame = tk.LabelFrame(root, text="Precios", font=("Arial", 14, "bold"), bd=2, relief="sunken", padx=10, pady=10)
price_frame.pack(pady=(10, 0), padx=10, fill="x")

# Controles para Price
price_controls = tk.Frame(root)
price_controls.pack(pady=(5, 10), padx=10, fill="x")

add_price_button = tk.Button(price_controls, text="Agregar", command=lambda: add_button("price"))
add_price_button.pack(side="left", padx=10)

price_combobox = ttk.Combobox(price_controls, state="readonly", width=30)
price_combobox.pack(side="left", padx=10)

remove_price_button = tk.Button(price_controls, text="Eliminar", command=lambda: remove_button("price"))
remove_price_button.pack(side="left", padx=10)

# Cargar los botones iniciales
load_buttons()

root.mainloop()
