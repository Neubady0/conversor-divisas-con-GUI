import requests
import xml.etree.ElementTree as ET
import tkinter as tk
from tkinter import ttk, messagebox

# ---------------------------
# DESCARGAR XML DEL BCE
# ---------------------------
url = "https://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml"

response = requests.get(url)
xml_data = response.content

# Parseamos el XML
root = ET.fromstring(xml_data)

# Encontramos el nodo con los datos (tiene un namespace raro)
namespace = {"gesmes": "http://www.gesmes.org/xml/2002-08-01",
             "e": "http://www.ecb.int/vocabulary/2002-08-01/eurofxref"}

cube_time = root.find(".//e:Cube/e:Cube", namespace)
fecha = cube_time.attrib["time"]

# Diccionario de tasas
tasas = {"EUR": 1.0}  # Añadimos euro manualmente

for item in cube_time.findall("e:Cube", namespace):
    moneda = item.attrib["currency"]
    rate = float(item.attrib["rate"])
    tasas[moneda] = rate

# ---------------------------
# FUNCIÓN DE CONVERSIÓN
# ---------------------------
def convertir():
    try:
        cantidad = float(entry_cantidad.get())
    except:
        messagebox.showerror("Error", "Introduce un número válido.")
        return

    origen = combo_origen.get()
    destino = combo_destino.get()

    if origen == "" or destino == "":
        messagebox.showerror("Error", "Selecciona ambas monedas.")
        return

    # Conversión cruzada usando EUR como puente
    resultado = (cantidad / tasas[origen]) * tasas[destino]
    label_resultado.config(text=f"{cantidad} {origen} = {round(resultado, 4)} {destino}")

# ---------------------------
# INTERFAZ GRÁFICA TKINTER
# ---------------------------
ventana = tk.Tk()
ventana.title("Conversor de Divisas - BCE")

tk.Label(ventana, text=f"Datos del BCE (fecha: {fecha})").pack(pady=5)

tk.Label(ventana, text="Cantidad:").pack()
entry_cantidad = tk.Entry(ventana)
entry_cantidad.pack()

tk.Label(ventana, text="Moneda origen:").pack()
combo_origen = ttk.Combobox(ventana, values=list(tasas.keys()))
combo_origen.pack()

tk.Label(ventana, text="Moneda destino:").pack()
combo_destino = ttk.Combobox(ventana, values=list(tasas.keys()))
combo_destino.pack()

tk.Button(ventana, text="Convertir", command=convertir).pack(pady=10)

label_resultado = tk.Label(ventana, text="", font=("Arial", 12))
label_resultado.pack()

ventana.mainloop()