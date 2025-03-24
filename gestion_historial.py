import json
import os
from datetime import datetime

HISTORIAL_FILE = "historial.json"

def guardar_historial(correo, alias):
    nuevo_registro = {
        "correo": correo,
        "alias": alias,
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    historial = []
    if os.path.exists(HISTORIAL_FILE):
        with open(HISTORIAL_FILE, "r") as f:
            historial = json.load(f)

    historial.append(nuevo_registro)

    with open(HISTORIAL_FILE, "w") as f:
        json.dump(historial, f, indent=4)
