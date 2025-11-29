#modelo
import RPi.GPIO as GPIO
import time
import adafruit_dht
import board

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

LED_PIN = 18
DHT_PIN = board.D4

GPIO.setup(LED_PIN, GPIO.OUT)

class Robot:
    def _init_(self, nombre, modelo):
        self.nombre = nombre
        self.modelo = modelo

    def encender(self):
        return f"🟢 {self.nombre} ({self.modelo}) está ENCENDIDO."

    def apagar(self):
        return f"🔴 {self.nombre} apagándose..."

class RobotExplorador(Robot):
    def _init_(self, nombre, modelo, zona):
        super()._init_(nombre, modelo)
        self.zona = zona

    def explorar(self):
        GPIO.output(LED_PIN, GPIO.HIGH)
        time.sleep(2)
        GPIO.output(LED_PIN, GPIO.LOW)
        return f"🚀 {self.nombre} ha explorado la zona: {self.zona} con éxito."

class RobotConstructor(Robot):
    def _init_(self, nombre, modelo):
        super()._init_(nombre, modelo)

    def preparar(self):
        GPIO.output(LED_PIN, GPIO.HIGH)
        return "💡 LED encendido. Robot listo para construir."

    def construir(self):
        for _ in range(5):
            GPIO.output(LED_PIN, GPIO.HIGH)
            time.sleep(0.5)
            GPIO.output(LED_PIN, GPIO.LOW)
            time.sleep(0.5)
        return "🏗 Construcción finalizada correctamente."

class RobotMedico(Robot):
    def _init_(self, nombre, modelo):
        super()._init_(nombre, modelo)

    def leer_sensor(self, tipo_lectura):
        sensor = adafruit_dht.DHT11(DHT_PIN)
        intentos = 0
        temperatura = None
        humedad = None

        while intentos < 5:
            try:
                time.sleep(2)
                temperatura = sensor.temperature
                humedad = sensor.humidity
                if temperatura is not None and humedad is not None:
                    break
            except RuntimeError:
                intentos += 1
                time.sleep(1)

        sensor.exit()
        GPIO.output(LED_PIN, GPIO.LOW)

        if temperatura is None or humedad is None:
            return "⚠ Error: No se pudo leer el sensor."

        if tipo_lectura == "temperatura":
            return f"🌡 Temperatura: {temperatura:.1f} °C"
        elif tipo_lectura == "humedad":
            return f"💧 Humedad: {humedad:.1f}%"
        else:
            return "Opción no válida."

def limpiar_gpio():
    GPIO.cleanup()
    print("Hardware liberado.")


#vista
from telebot import types

def menu_principal():
    markup = types.InlineKeyboardMarkup()
    markup.row_width = 1
    btn1 = types.InlineKeyboardButton("🚀 Robot Explorador", callback_data="accion_explorar")
    btn2 = types.InlineKeyboardButton("🏗 Robot Constructor", callback_data="accion_construir")
    btn3 = types.InlineKeyboardButton("🩺 Robot Médico", callback_data="menu_medico")

    markup.add(btn1, btn2, btn3)
    return markup

def menu_medico():
    markup = types.InlineKeyboardMarkup()
    markup.row_width = 2
    btn_temp = types.InlineKeyboardButton("Medir Temperatura 🌡", callback_data="medir_temp")
    btn_hum = types.InlineKeyboardButton("Medir Humedad 💧", callback_data="medir_hum")

    markup.add(btn_temp, btn_hum)
    return markup

def msg_bienvenida():
    return "🤖 *Centro de Control de Robots*\nSeleccione una unidad para operar:"

def msg_espera():
    return "⏳ Procesando solicitud... por favor espere."


#controlador
import sys
import os
import telebot
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(_file_), '..')))

from modelo import robot_model as model
from vista import telegram_view as view

TOKEN = "8487921064:AAHArmBl0KvCv7qZV0IghR9mSlx2kTXrlk"
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def iniciar(message):
    bot.send_message(message.chat.id, view.msg_bienvenida(), reply_markup=view.menu_principal(), parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: True)
def procesar_botones(call):
    cid = call.message.chat.id
    accion = call.data

    bot.answer_callback_query(call.id)

    try:
        if accion == "accion_explorar":
            bot.send_message(cid, view.msg_espera())

            robot = model.RobotExplorador("Explorer-1", "XJ9", "Ártico")
            bot.send_message(cid, robot.encender())

            resultado = robot.explorar()
            bot.send_message(cid, resultado)
            bot.send_message(cid, robot.apagar())

        elif accion == "accion_construir":
            bot.send_message(cid, "Preparando materiales...")

            robot = model.RobotConstructor("Builder-X", "MK3")
            bot.send_message(cid, robot.encender())
            bot.send_message(cid, robot.preparar())

            bot.send_message(cid, "🔨 Construyendo... (Espere 5s)")
            resultado = robot.construir()
            bot.send_message(cid, resultado)
            bot.send_message(cid, robot.apagar())

        elif accion == "menu_medico":
            bot.edit_message_text("¿Qué diagnóstico desea realizar?", cid, call.message.message_id, reply_markup=view.menu_medico())
            return

        elif accion in ["medir_temp", "medir_hum"]:
            bot.send_message(cid, view.msg_espera())

            robot = model.RobotMedico("Baymax", "Health-V1")
            bot.send_message(cid, robot.encender())

            tipo = "temperatura" if accion == "medir_temp" else "humedad"
            resultado = robot.leer_sensor(tipo)

            bot.send_message(cid, resultado)
            bot.send_message(cid, robot.apagar())

        time.sleep(1)
        bot.send_message(cid, "✅ Tarea finalizada. ¿Siguiente orden?", reply_markup=view.menu_principal())

    except Exception as e:
        bot.send_message(cid, f"❌ Error crítico: {str(e)}")
        print(f"Error: {e}")

if _name_ == "_main_":
    print("🤖 Bot Controlador Iniciado...")
    try:
        bot.polling(none_stop=True)
    except KeyboardInterrupt:
        print("\nApagando sistema...")
    finally:
        model.limpiar_gpio()
        print("GPIO Limpio. Adiós.")
