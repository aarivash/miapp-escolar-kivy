import qrcode
import os
import json

QR_FOLDER = "qr"

def generar_qr(correo, alias):
    if not os.path.exists(QR_FOLDER):
        os.makedirs(QR_FOLDER)
    data = json.dumps({"correo": correo, "alias": alias})
    img = qrcode.make(data)
    img.save(f"{QR_FOLDER}/qr_{correo.replace('@','_at_')}.png")
