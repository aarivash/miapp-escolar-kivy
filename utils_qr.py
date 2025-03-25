import qrcode
import os
import json
import cv2
from pyzbar.pyzbar import decode

QR_FOLDER = "qr"

def generar_qr(correo, alias):
    if not os.path.exists(QR_FOLDER):
        os.makedirs(QR_FOLDER)
    data = json.dumps({"correo": correo, "alias": alias})
    img = qrcode.make(data)
    img.save(f"{QR_FOLDER}/qr_{correo.replace('@','_at_')}.png")

def leer_qr():
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        for codigo in decode(frame):
            try:
                datos = json.loads(codigo.data.decode("utf-8"))
                cap.release()
                cv2.destroyAllWindows()
                return datos
            except:
                cap.release()
                cv2.destroyAllWindows()
                return None
        cv2.imshow("Escanea tu código QR", frame)
        if cv2.waitKey(1) == 27:  # ESC para salir
            break
    cap.release()
    cv2.destroyAllWindows()
    return None
