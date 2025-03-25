
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivy.metrics import dp
from kivy.uix.image import Image
from kivymd.uix.screen import MDScreen
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.boxlayout import MDBoxLayout
import json, os
from estilos import COLORES, TAMAÑOS

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
        entradas_usuario = []
        if os.path.exists(HISTORIAL_FILE):
            with open(HISTORIAL_FILE, "r") as f:
                historial = json.load(f)
                entradas_usuario = [
                    f"{entry['fecha']} - {entry['alias']} ({entry['correo']})"
                    for entry in historial
                    if entry["alias"] == self.nombre_usuario
                ]
                texto = "\n".join(entradas_usuario) if entradas_usuario else "No hay accesos registrados."

        scroll_view = MDScrollView()
        contenedor = MDBoxLayout(orientation='vertical', adaptive_height=True, padding=dp(10), spacing=dp(5))

        for entrada in entradas_usuario:
            contenedor.add_widget(MDLabel(
                text=entrada,
                halign="left",
                theme_text_color="Custom",
                text_color=(1, 1, 1, 1),
                size_hint_y=None,
                height=dp(30),
                font_style="Body1"
            ))

        scroll_view.add_widget(contenedor)

        popup = Popup(
            title='Historial de accesos',
            content=scroll_view,
            size_hint=(0.9, 0.7),
            background_color=(0, 0, 0, 0.8),
            auto_dismiss=True
        )
        popup.open()

    def cerrar_sesion(self, instance):
        if self.cerrar_sesion_callback:
            self.cerrar_sesion_callback()
