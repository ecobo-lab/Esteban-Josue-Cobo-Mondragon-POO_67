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

class RegistroDatos:
    def _init_(self):
        self.eventos = {
            "encendidos": 0,
            "apagados": 0,
            "temperaturas": 0,
            "humedades": 0,
            "boton_presiones": 0,
            "exploraciones": 0
        }

    def guardar(self, archivo, texto):
        with open(archivo, "a") as f:
            f.write(texto + "\n")
        return f"Datos guardados en {archivo}"

    def registrar_evento(self, tipo):
        if tipo in self.eventos:
            self.eventos[tipo] += 1

    def obtener_reporte(self):
        return (
            "📊 REGISTRO DE ACTIVIDADES\n\n"
            f"• LED encendido: {self.eventos['encendidos']}\n"
            f"• LED apagado: {self.eventos['apagados']}\n"
            f"• Lecturas temperatura: {self.eventos['temperaturas']}\n"
            f"• Lecturas humedad: {self.eventos['humedades']}\n"
            f"• Botón presionado: {self.eventos['boton_presiones']}\n"
            f"• Exploraciones: {self.eventos['exploraciones']}\n"
        )

class Robot:
    def _init_(self, nombre, registro):
        self.nombre = nombre
        self.registro = registro

class RobotConstructor(Robot):
    def encender(self):
        GPIO.output(PIN_LED, True)
        self.registro.registrar_evento("encendidos")
        return "Constructor encendido (LED ON)"

    def apagar(self):
        GPIO.output(PIN_LED, False)
        self.registro.registrar_evento("apagados")
        return "Constructor apagado (LED OFF)"

class RobotMedico(Robot):
    def _init_(self, nombre, registro):
        super()._init_(nombre, registro)
        self.sensor = adafruit_dht.DHT11(board.D4)

    def medir_temperatura(self):
        try:
            time.sleep(2)
            t = self.sensor.temperature
            self.registro.registrar_evento("temperaturas")
            return f"Temperatura: {t}°C"
        except:
            return "⚠ Error al leer temperatura."

    def medir_humedad(self):
        try:
            time.sleep(2)
            h = self.sensor.humidity
            self.registro.registrar_evento("humedades")
            return f"Humedad: {h}%"
        except:
            return "⚠ Error al leer humedad."

class RobotExplorador(Robot):
    def explorar(self):
        while GPIO.input(PIN_BOTON) == GPIO.LOW:
            time.sleep(0.01)

        self.registro.registrar_evento("boton_presiones")
        self.registro.registrar_evento("exploraciones")

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
            "Menú principal:\n\n"
            "/constructor_on\n"
            "/constructor_off\n"
            "/medico_temp\n"
            "/medico_hum\n"
            "/explorar\n\n"
            "Guardar datos:\n"
            "/guardar_constructor\n"
            "/guardar_medico\n"
            "/guardar_explorador\n"
            "/guardar_todo\n"
            "/reporte\n\n"
            "/estado\n"
            "/salir\n"
        )


#controlador
import time
import telepot
from telepot.loop import MessageLoop
import RPi.GPIO as GPIO

from modelo import RobotConstructor, RobotMedico, RobotExplorador, RegistroDatos
from vista import TelegramView

class Controlador:
    def _init_(self, bot):
        self.bot = bot
        self.vista = TelegramView()

        self.registro = RegistroDatos()

        self.constructor = RobotConstructor("Constructor", self.registro)
        self.medico = RobotMedico("Médico", self.registro)
        self.explorador = RobotExplorador("Explorador", self.registro)

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
            self.vista.enviar(self.bot, chat_id, "Esperando botón para detener...")
            res = self.explorador.explorar()
            self.vista.enviar(self.bot, chat_id, res)

        elif comando == "/guardar_constructor":
            texto = f"{time.ctime()} - Constructor: encendidos={self.registro.eventos['encendidos']}, apagados={self.registro.eventos['apagados']}"
            self.vista.enviar(self.bot, chat_id, self.registro.guardar("constructor.log", texto))

        elif comando == "/guardar_medico":
            texto = f"{time.ctime()} - Médico: temp={self.registro.eventos['temperaturas']}, humedades={self.registro.eventos['humedades']}"
            self.vista.enviar(self.bot, chat_id, self.registro.guardar("medico.log", texto))

        elif comando == "/guardar_explorador":
            texto = f"{time.ctime()} - Explorador: botones={self.registro.eventos['boton_presiones']}, exploraciones={self.registro.eventos['exploraciones']}"
            self.vista.enviar(self.bot, chat_id, self.registro.guardar("explorador.log", texto))

        elif comando == "/guardar_todo":
            texto = f"{time.ctime()}\n{self.registro.obtener_reporte()}"
            self.vista.enviar(self.bot, chat_id, self.registro.guardar("general.log", texto))

        elif comando == "/reporte":
            self.vista.enviar(self.bot, chat_id, self.registro.obtener_reporte())

        elif comando == "/estado":
            self.vista.enviar(self.bot, chat_id, "Sistema funcionando correctamente.")

        elif comando == "/salir":
            GPIO.cleanup()
            self.vista.enviar(self.bot, chat_id, "Sistema apagado.")

        else:
            self.vista.enviar(self.bot, chat_id, "Comando no reconocido.")

TOKEN = "8535227713:AAFMaxvsBrdkoUD2xN0_X3IXiaPtVQkBg8k"

bot = telepot.Bot(TOKEN)
controlador = Controlador(bot)

MessageLoop(bot, controlador.manejar_mensaje).run_as_thread()

print("🤖 Bot Telegram activo...")

while True:
    time.sleep(10)


#general.log
Mon Nov 17 20:33:09 2025
📊 REGISTRO DE ACTIVIDADES

• LED encendido: 1
• LED apagado: 1
• Lecturas temperatura: 1
• Lecturas humedad: 1
• Botón presionado: 1
• Exploraciones: 1


#constructor.log
Mon Nov 17 20:32:56 2025 - Constructor: encendidos=1, apagados=1


#explorador.log
Mon Nov 17 20:33:04 2025 - Explorador: botones=1, exploraciones=1


#medico.log
Mon Nov 17 20:33:00 2025 - Médico: temp=1, humedades=1
