#modelo
import RPi.GPIO as GPIO
import time
import adafruit_dht
import board

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

PIN_LED = 18
PIN_BOTON = 25

GPIO.setup(PIN_LED, GPIO.OUT)
GPIO.setup(PIN_BOTON, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

class Robot:
    def _init_(self, nombre):
        self.nombre = nombre

class RobotConstructor(Robot):
    def encender(self):
        GPIO.output(PIN_LED, True)
        return "Constructor encendido (LED ON)"

    def apagar(self):
        GPIO.output(PIN_LED, False)
        return "Constructor apagado (LED OFF)"

class RobotMedico(Robot):
    def _init_(self, nombre):
        super()._init_(nombre)
        self.sensor = adafruit_dht.DHT11(board.D4)

    def medir_temperatura(self):
        try:
            time.sleep(2)
            t = self.sensor.temperature
            return f"Temperatura: {t}°C"
        except:
            return "⚠ Error al leer temperatura."

    def medir_humedad(self):
        try:
            time.sleep(2)
            h = self.sensor.humidity
            return f"Humedad: {h}%"
        except:
            return "⚠ Error al leer humedad."

class RobotExplorador(Robot):
    def explorar(self):
        while GPIO.input(PIN_BOTON) == GPIO.LOW:
            time.sleep(0.01)

        GPIO.output(PIN_LED, True)

        while GPIO.input(PIN_BOTON) == GPIO.HIGH:
            time.sleep(0.01)

        GPIO.output(PIN_LED, False)
        return "Exploración detenida"


#vista
class TelegramView:
    def enviar(self, bot, chat_id, mensaje):
        bot.sendMessage(chat_id, mensaje)

    def menu_principal(self):
        return (
            "Robots disponibles:\n\n"
            "/constructor_on\n"
            "/constructor_off\n"
            "/medico_temp\n"
            "/medico_hum\n"
            "/explorar\n"
            "/estado\n"
            "/salir\n"
        )


#controlador
import time
import telepot
from telepot.loop import MessageLoop
from modelo import RobotConstructor, RobotMedico, RobotExplorador
from vista import TelegramView
import RPi.GPIO as GPIO

class Controlador:
    def _init_(self, bot):
        self.bot = bot
        self.vista = TelegramView()

        self.constructor = RobotConstructor("Constructor")
        self.medico = RobotMedico("Medico")
        self.explorador = RobotExplorador("Explorador")

    def manejar_mensaje(self, msg):
        chat_id = msg["chat"]["id"]
        comando = msg["text"]

        if comando == "/start":
            self.vista.enviar(self.bot, chat_id, self.vista.menu_principal())

        elif comando == "/constructor_on":
            resp = self.constructor.encender()
            self.vista.enviar(self.bot, chat_id, resp)

        elif comando == "/constructor_off":
            resp = self.constructor.apagar()
            self.vista.enviar(self.bot, chat_id, resp)

        elif comando == "/medico_temp":
            resp = self.medico.medir_temperatura()
            self.vista.enviar(self.bot, chat_id, resp)

        elif comando == "/medico_hum":
            resp = self.medico.medir_humedad()
            self.vista.enviar(self.bot, chat_id, resp)

        elif comando == "/explorar":
            self.vista.enviar(self.bot, chat_id, "Presiona el botón para detener exploracion")
            resultado = self.explorador.explorar()
            self.vista.enviar(self.bot, chat_id, resultado)

        elif comando == "/estado":
            self.vista.enviar(self.bot, chat_id, "Sistema funcionando perfectamente.")

        elif comando == "/salir":
            GPIO.cleanup()
            self.vista.enviar(self.bot, chat_id, "Sistema apagado.")

        else:
            self.vista.enviar(self.bot, chat_id, "Comando no reconocido.")

TOKEN = "8487921064:AAHArmBl0KvCv7qZV0IghR9mSlx2kTXrlk"

bot = telepot.Bot(TOKEN)
controlador = Controlador(bot)

MessageLoop(bot, controlador.manejar_mensaje).run_as_thread()

print("Bot Telegram activo...")

while True:
    time.sleep(10)
