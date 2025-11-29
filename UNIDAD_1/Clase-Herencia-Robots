import RPi.GPIO as GPIO
import time
import adafruit_dht
import board

# Configuración de GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Definición de pines
LED_PIN = 18
BUTTON_PIN = 25
DHT_PIN = board.D4

# Configuración de entrada/salida
GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# --- Definición de Clases ---

class Robot:
    def _init_(self, nombre, modelo):
        self.nombre = nombre
        self.modelo = modelo

    def encender(self):
        print(f"{self.nombre} está encendido.")

    def apagar(self):
        print(f"{self.nombre} está apagado.")

    def estado(self):
        print(f"Robot: {self.nombre}, Modelo: {self.modelo}")

class RobotExplorador(Robot):
    def _init_(self, nombre, modelo, zona_exploracion):
        super()._init_(nombre, modelo)
        self.zona_exploracion = zona_exploracion

    def explorar(self):
        print("Presiona el botón para comenzar la exploración...")
        while True:
            # Espera a que se presione el botón (estado LOW)
            if GPIO.input(BUTTON_PIN) == GPIO.LOW:
                GPIO.output(LED_PIN, GPIO.HIGH)
                print(f"{self.nombre} está explorando la zona: {self.zona_exploracion}")
                time.sleep(2)
                GPIO.output(LED_PIN, GPIO.LOW)
                break
        print("Exploración finalizada.\n")

class RobotConstructor(Robot):
    def _init_(self, nombre, modelo):
        super()._init_(nombre, modelo)

    def encender_led(self):
        GPIO.output(LED_PIN, GPIO.HIGH)
        print("LED encendido (Robot Constructor listo).")

    def construir(self):
        print("Escribe 'construir' para iniciar la construcción:")
        comando = input(">> ").strip().lower()
        if comando == "construir":
            print("Robot construyendo ")
            # Parpadeo del LED para simular construcción
            for _ in range(5):
                GPIO.output(LED_PIN, GPIO.HIGH)
                time.sleep(0.5)
                GPIO.output(LED_PIN, GPIO.LOW)
                time.sleep(0.5)
        else:
            print("Comando no reconocido. El robot espera instrucciones.")

class RobotMedico(Robot):
    def _init_(self, nombre, modelo):
        super()._init_(nombre, modelo)

    def diagnosticar(self):
        print("¿Qué deseas medir? (temperatura / humedad)")
        opcion = input(">> ").strip().lower()

        # Inicializar el sensor DHT11
        sensor = adafruit_dht.DHT11(DHT_PIN)

        intentos = 0
        temperatura = None
        humedad = None

        # Intentar leer el sensor hasta 5 veces
        while intentos < 5:
            try:
                time.sleep(2) # Espera necesaria para el sensor DHT
                temperatura = sensor.temperature
                humedad = sensor.humidity

                if temperatura is not None and humedad is not None:
                    break
            except RuntimeError as e:
                print("Error al leer el sensor:", e)
                intentos += 1
                time.sleep(1)

        # Mostrar resultados
        if temperatura is None or humedad is None:
            print("No se pudo obtener una lectura válida del sensor.")
        else:
            if opcion == "temperatura":
                print(f"Temperatura actual: {temperatura:.1f} °C")
            elif opcion == "humedad":
                print(f"Humedad actual: {humedad:.1f} %")
            else:
                print("Opción no válida.")

        sensor.exit()
        GPIO.output(LED_PIN, GPIO.LOW)
        print()

# --- Función Principal de Simulación ---

def simulacion():
    try:
        while True:
            print("\nSelecciona el robot:")
            print("1. Explorador")
            print("2. Constructor")
            print("3. Médico")
            print("4. Salir")

            opcion = input(">> ")

            if opcion == "1":
                robot = RobotExplorador("R-Explorer", "XJ-9", "Zona Ártica")
                robot.encender()
                robot.explorar()
                robot.apagar()

            elif opcion == "2":
                robot = RobotConstructor("R-Builder", "MK-3")
                robot.encender()
                robot.encender_led()
                robot.construir()
                robot.apagar()

            elif opcion == "3":
                robot = RobotMedico("R-Med", "MED-5")
                robot.encender()
                robot.diagnosticar()
                robot.apagar()

            elif opcion == "4":
                print("Saliendo del programa...")
                break

            else:
                print("Opción inválida.")

    except KeyboardInterrupt:
        print("\nPrograma interrumpido manualmente.")
    finally:
        # Limpieza de los pines GPIO al finalizar
        GPIO.cleanup()
        print("GPIO limpiado. Fin del programa.")

# --- Punto de Entrada del Programa ---
if _name_ == "_main_":
    simulacion()
