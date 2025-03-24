from kivymd.app import MDApp
from kivymd.uix.screen import Screen
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.dialog import MDDialog
from kivy.uix.image import Image
import json, os, re, cv2
from pyzbar.pyzbar import decode

from gestion_usuarios import cargar_usuarios, guardar_usuario
from gestion_historial import guardar_historial
from utils_qr import generar_qr

def es_correo_valido(correo):
    return re.match(r"[^@\s]+@[^@\s]+\.[^@\s]+", correo)

def alias_valido(alias):
    return alias.isalnum() and len(alias) <= 15

class MiAppEscolar(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Blue"
        self.pantalla = Screen()
        self.etiqueta = MDLabel(text="Ingresa tu correo:", halign="center", pos_hint={"center_y": 0.8})
        self.entrada = MDTextField(hint_text="correo@ejemplo.com", pos_hint={"center_x": 0.5, "center_y": 0.7}, size_hint_x=0.8)
        self.boton = MDRaisedButton(text="Continuar", pos_hint={"center_x": 0.5, "center_y": 0.6}, on_release=self.validar_correo)
        self.boton_qr = MDRaisedButton(text="Ingresar con QR", pos_hint={"center_x": 0.5, "center_y": 0.5}, on_release=self.login_con_qr)
        self.pantalla.add_widget(self.etiqueta)
        self.pantalla.add_widget(self.entrada)
        self.pantalla.add_widget(self.boton)
        self.pantalla.add_widget(self.boton_qr)
        return self.pantalla

    def validar_correo(self, obj):
        self.correo = self.entrada.text.strip()
        if es_correo_valido(self.correo):
            usuarios = cargar_usuarios()
            if self.correo in usuarios:
                self.mostrar_bienvenida(usuarios[self.correo]["alias"])
            else:
                self.pedir_alias()
        else:
            self.etiqueta.text = "Correo inválido. Intenta nuevamente."

    def pedir_alias(self):
        self.pantalla.clear_widgets()
        self.etiqueta = MDLabel(text="Crea tu alias (sin símbolos, máx. 15):", halign="center", pos_hint={"center_y": 0.8})
        self.entrada_alias = MDTextField(hint_text="Tu alias", pos_hint={"center_x": 0.5, "center_y": 0.7}, size_hint_x=0.8)
        self.boton_alias = MDRaisedButton(text="Registrar", pos_hint={"center_x": 0.5, "center_y": 0.6}, on_release=self.registrar_alias)
        self.pantalla.add_widget(self.etiqueta)
        self.pantalla.add_widget(self.entrada_alias)
        self.pantalla.add_widget(self.boton_alias)

    def registrar_alias(self, obj):
        alias = self.entrada_alias.text.strip()
        if alias_valido(alias):
            guardar_usuario(self.correo, alias)
            guardar_historial(self.correo, alias)
            self.mostrar_bienvenida(alias)
        else:
            self.etiqueta.text = "Alias inválido. Solo letras/números, máx. 15."

    def mostrar_bienvenida(self, alias):
        guardar_historial(self.correo, alias)
        self.pantalla.clear_widgets()
        saludo = MDLabel(text=f"¡Hola, {alias}!", halign="center", pos_hint={"center_y": 0.8})
        btn_qr = MDRaisedButton(text="Ver mi QR", pos_hint={"center_x": 0.5, "center_y": 0.6}, on_release=self.mostrar_qr)
        self.pantalla.add_widget(saludo)
        self.pantalla.add_widget(btn_qr)

    def mostrar_qr(self, obj):
        self.pantalla.clear_widgets()
        ruta_qr = f"qr/qr_{self.correo.replace('@','_at_')}.png"
        if os.path.exists(ruta_qr):
            img = Image(source=ruta_qr, size_hint=(None, None), size=(200, 200), pos_hint={"center_x": 0.5, "center_y": 0.6})
            lbl = MDLabel(text="Escanea este código para ingresar fácilmente", halign="center", pos_hint={"center_y": 0.85})
            self.pantalla.add_widget(lbl)
            self.pantalla.add_widget(img)

    def login_con_qr(self, obj):
        cap = cv2.VideoCapture(0)
        encontrado = False
        while not encontrado:
            ret, frame = cap.read()
            for codigo in decode(frame):
                datos = codigo.data.decode("utf-8")
                try:
                    data = json.loads(datos)
                    correo = data["correo"]
                    alias = data["alias"]
                    usuarios = cargar_usuarios()
                    if correo in usuarios and usuarios[correo]["alias"] == alias:
                        encontrado = True
                        cap.release()
                        cv2.destroyAllWindows()
                        guardar_historial(correo, alias)
                        self.correo = correo
                        self.mostrar_bienvenida(alias)
                        return
                    else:
                        self.mostrar_dialogo("QR no válido", "Usuario no registrado.")
                        encontrado = True
                except:
                    self.mostrar_dialogo("Error", "El QR no contiene datos válidos.")
                    encontrado = True
            cv2.imshow("Escanea tu QR", frame)
            if cv2.waitKey(1) == 27:  # Presiona ESC para salir
                break
        cap.release()
        cv2.destroyAllWindows()

    def mostrar_dialogo(self, titulo, mensaje):
        dialogo = MDDialog(
            title=titulo,
            text=mensaje,
            buttons=[MDFlatButton(text="OK", on_release=lambda x: dialogo.dismiss())]
        )
        dialogo.open()

MiAppEscolar().run()
