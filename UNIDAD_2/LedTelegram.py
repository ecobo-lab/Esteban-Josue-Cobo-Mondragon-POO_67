import time
import requests
import RPi.GPIO as GPIO

# PRECAUCIÓN: En la foto aparece un token real. 
# Si vas a compartir este código, procura borrarlo o regenerarlo en BotFather.
token = "8503526674:AAGY4Tc8P6VJ20jSn6rcGdBehghUCQXsako"
led_pin = 18
allowed_chat_id = None

base_url = f"https://api.telegram.org/bot{token}/"

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(led_pin, GPIO.OUT)
GPIO.output(led_pin, GPIO.LOW)

def send_message(chat_id, text):
    url = base_url + "sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    try:
        requests.post(url, data=payload, timeout=5)
    except Exception as e:
        print("Error enviando mensaje:", e)

def get_updates(offset=None, timeout=30):
    url = base_url + "getUpdates"
    params = {"timeout": timeout}
    if offset:
        params["offset"] = offset
    try:
        r = requests.get(url, params=params, timeout=timeout + 10)
        return r.json()
    except Exception as e:
        print("Error getUpdates:", e)
        return None

def handle_message(msg):
    if "message" not in msg:
        return

    m = msg["message"]
    chat_id = m["chat"]["id"]
    text = m.get("text", "").strip().lower()

    print(f"Mensaje de {chat_id}: {text}")

    if text == "/off":
        GPIO.output(led_pin, GPIO.HIGH)
        send_message(chat_id, "LED encendido ✅")

    elif text == "/on":
        GPIO.output(led_pin, GPIO.LOW)
        send_message(chat_id, "LED apagado ✅")

    elif text == "/status":
        state = GPIO.input(led_pin)
        send_message(chat_id, f"Estado del LED: {'ON' if state else 'OFF'}")

    elif text == "/id":
        send_message(chat_id, f"Tu chat ID es: {chat_id}")

    else:
        send_message(chat_id, "Comandos disponibles:\n/on\n/off\n/status\n/id")

def main_loop():
    print("Bot arrancando...")
    last_update_id = None

    while True:
        data = get_updates(offset=(last_update_id + 1) if last_update_id else None)

        if not data or not data.get("ok"):
            time.sleep(1)
            continue

        for item in data.get("result", []):
            last_update_id = item["update_id"]
            try:
                handle_message(item)
            except Exception as e:
                print("Error procesando mensaje:", e)

if _name_ == "_main_":
    try:
        main_loop()
    except KeyboardInterrupt:
        print("Deteniendo bot...")
    finally:
        GPIO.cleanup()
