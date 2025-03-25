from kivymd.app import MDApp
from kivymd.uix.screen import Screen
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.textfield import MDTextField
from kivy.uix.image import Image
from gestion_usuarios import cargar_usuarios, guardar_usuario
from gestion_historial import guardar_historial
from utils_qr import generar_qr, leer_qr
from vista.pantalla_principal import PantallaPrincipal
from estilos import COLORES, TAMAÑOS
import os, re

class MiAppEscolar(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Blue"
        self.pantalla = Screen()
        self.mostrar_menu_inicio()
        return self.pantalla

    def mostrar_menu_inicio(self):
        self.pantalla.clear_widgets()
        self.etiqueta = MDLabel(
            text="Bienvenido a MiApp Escolar",
            halign="center",
            pos_hint={"center_y": 0.8},
            theme_text_color="Custom",
            text_color=COLORES["texto"]
        )
        self.entrada = MDTextField(
            hint_text="correo@ejemplo.com",
            pos_hint={"center_x": 0.5, "center_y": 0.7},
            size_hint_x=0.8
        )
        self.boton = MDRaisedButton(
            text="Continuar",
            pos_hint={"center_x": 0.5, "center_y": 0.6},
            on_release=self.validar_correo
        )
        self.boton_qr = MDRaisedButton(
            text="📷 Escanear QR para ingresar",
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            md_bg_color=COLORES["boton"],
            on_release=self.login_con_qr
        )
        self.boton_salir = MDRaisedButton(
            text="Salir",
            pos_hint={"center_x": 0.5, "center_y": 0.4},
            md_bg_color=COLORES["secundario"],
            on_release=self.salir_aplicacion
        )

        self.pantalla.add_widget(self.etiqueta)
        self.pantalla.add_widget(self.entrada)
        self.pantalla.add_widget(self.boton)
        self.pantalla.add_widget(self.boton_qr)
        self.pantalla.add_widget(self.boton_salir)

    def validar_correo(self, obj):
        correo = self.entrada.text.strip()
        if re.match(r"[^@\s]+@[^@\s]+\.[^@\s]+", correo):
            usuarios = cargar_usuarios()
            if correo in usuarios:
                alias = usuarios[correo]["alias"]
                guardar_historial(correo, alias)
                self.ir_a_pantalla_principal(alias)
            else:
                self.mostrar_form_alias(correo)
        else:
            self.etiqueta.text = "Correo inválido. Intenta nuevamente."

    def mostrar_form_alias(self, correo):
        self.pantalla.clear_widgets()
        self.correo_nuevo = correo
        etiqueta = MDLabel(text="Crea tu alias:", halign="center", pos_hint={"center_y": 0.8})
        entrada = MDTextField(hint_text="Tu alias", pos_hint={"center_x": 0.5, "center_y": 0.7}, size_hint_x=0.8)
        boton = MDRaisedButton(text="Registrar", pos_hint={"center_x": 0.5, "center_y": 0.6},
                               on_release=lambda x: self.registrar_alias(self.correo_nuevo, entrada.text))
        self.pantalla.add_widget(etiqueta)
        self.pantalla.add_widget(entrada)
        self.pantalla.add_widget(boton)

    def registrar_alias(self, correo, alias):
        if alias.isalnum() and len(alias) <= 15:
            guardar_usuario(correo, alias)
            guardar_historial(correo, alias)
            generar_qr(correo, alias)
            self.ir_a_pantalla_principal(alias)
        else:
            self.etiqueta.text = "Alias inválido. Solo letras/números, máx. 15."

    def ir_a_pantalla_principal(self, alias):
        self.pantalla.clear_widgets()
        pantalla = PantallaPrincipal(nombre_usuario=alias, cerrar_sesion_callback=self.mostrar_menu_inicio)
        self.pantalla.add_widget(pantalla)

    def salir_aplicacion(self, instance):
        self.stop()

    def login_con_qr(self, instance):
        resultado = leer_qr()
        if resultado:
            correo = resultado.get("correo")
            alias = resultado.get("alias")
            usuarios = cargar_usuarios()
            if correo in usuarios and usuarios[correo]["alias"] == alias:
                guardar_historial(correo, alias)
                self.ir_a_pantalla_principal(alias)
            else:
                self.etiqueta.text = "QR inválido o usuario no registrado."
        else:
            self.etiqueta.text = "No se detectó QR válido."

MiAppEscolar().run()