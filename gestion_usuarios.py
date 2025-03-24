import json
import os

DB_FILE = "usuarios.json"

def cargar_usuarios():
    if not os.path.exists(DB_FILE):
        return {}
    with open(DB_FILE, "r") as f:
        return json.load(f)

def guardar_usuario(correo, alias):
    usuarios = cargar_usuarios()
    usuarios[correo] = {"alias": alias}
    with open(DB_FILE, "w") as f:
        json.dump(usuarios, f)
