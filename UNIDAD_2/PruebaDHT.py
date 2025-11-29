import time
import board
import adafruit_dht

dht_sensor = adafruit_dht.DHT11(board.D4)

while True:
    try:
        temperatura_c = dht_sensor.temperature
        humedad = dht_sensor.humidity

        temperatura_f = temperatura_c * (9 / 5) + 32

        print(f"Temperatura: {temperatura_c:.1f} °C / {temperatura_f:.1f} °F")
        print(f"Humedad: {humedad} %")
        print("---------------------")

    except RuntimeError as error:
        time.sleep(2.0)
        continue
    except Exception as error:
        dht_sensor.exit()
        raise error

    time.sleep(2.0)
