from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivy.app import App
from kivy.metrics import dp
from kivy.uix.image import Image
from gestion_historial import guardar_historial
from estilos import COLORES, TAMAÑOS
from kivymd.uix.screen import MDScreen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.textfield import MDTextField
import json, os

HISTORIAL_FILE = "historial.json"

class PantallaPrincipal(BoxLayout):
    def __init__(self, nombre_usuario, cerrar_sesion_callback, **kwargs):
        super().__init__(orientation='vertical', padding=dp(10), spacing=dp(10), **kwargs)
        self.nombre_usuario = nombre_usuario
        self.cerrar_sesion_callback = cerrar_sesion_callback
        self.md_bg_color = COLORES["fondo"]

        self.label_usuario = MDLabel(
            text=f"👤 {self.nombre_usuario}",
            halign='left',
            theme_text_color="Custom",
            text_color=COLORES["texto"],
            font_style="H6",
            size_hint=(1, 0.1)
        )
        self.add_widget(self.label_usuario)

        self.imagen = Image(
            source="imagenes/bienvenida.png",
            size_hint=(1, 0.4),
            mipmap=True
        )
        self.add_widget(self.imagen)

        self.boton_historial = MDRaisedButton(
            text="📜 Ver historial",
            md_bg_color=COLORES["boton"],
            text_color=COLORES["boton_texto"],
            size_hint=TAMAÑOS["boton"],
            pos_hint={"center_x": 0.5},
            on_release=self.mostrar_historial
        )
        self.add_widget(self.boton_historial)

        self.boton_cerrar = MDRaisedButton(
            text="🚪 Cerrar sesión",
            md_bg_color=COLORES["secundario"],
            text_color=COLORES["texto"],
            size_hint=TAMAÑOS["boton"],
            pos_hint={"center_x": 0.5},
            on_release=self.cerrar_sesion
        )
        self.add_widget(self.boton_cerrar)

    def mostrar_historial(self, instance):
        texto = "Historial no disponible."
        if os.path.exists(HISTORIAL_FILE):
            with open(HISTORIAL_FILE, "r") as f:
                historial = json.load(f)
                entradas_usuario = [
                    f"{entry['fecha']} - {entry['alias']} ({entry['correo']})"
                    for entry in historial
                    if entry["alias"] == self.nombre_usuario
                ]
                texto = "\n".join(entradas_usuario) if entradas_usuario else "No hay accesos registrados."

        popup = Popup(
            title='Historial de accesos',
            content=MDLabel(
                text=texto,
                halign="center",
                theme_text_color="Custom",
                text_color=COLORES["texto"]
            ),
            size_hint=(0.9, 0.5)
        )
        popup.open()

    def cerrar_sesion(self, instance):
        if self.cerrar_sesion_callback:
            self.cerrar_sesion_callback()

class PantallaInicio(MDScreen):
    def __init__(self, iniciar_sesion_callback, salir_callback, **kwargs):
        super().__init__(**kwargs)
        self.iniciar_sesion_callback = iniciar_sesion_callback
        self.salir_callback = salir_callback

        layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(15))

        label_bienvenida = MDLabel(
            text="📅 Bienvenido a MiAppEscolar",
            halign="center",
            font_style="H5",
            theme_text_color="Custom",
            text_color=COLORES["texto"]
        )
        layout.add_widget(label_bienvenida)

        self.boton_qr = MDRaisedButton(
            text="📷 Escanear QR para ingresar",
            md_bg_color=COLORES["boton"],
            text_color=COLORES["boton_texto"],
            size_hint=TAMAÑOS["boton"],
            pos_hint={"center_x": 0.5},
            on_release=self.iniciar_sesion_callback
        )
        layout.add_widget(self.boton_qr)

        self.boton_salir = MDRaisedButton(
            text="❌ Salir de la aplicación",
            md_bg_color=COLORES["secundario"],
            text_color=COLORES["texto"],
            size_hint=TAMAÑOS["boton"],
            pos_hint={"center_x": 0.5},
            on_release=self.salir_callback
        )
        layout.add_widget(self.boton_salir)

        self.add_widget(layout)