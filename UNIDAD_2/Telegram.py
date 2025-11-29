import time
import datetime
import telepot
import RPi.GPIO as GPIO
from telepot.loop import MessageLoop

led = 18
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(led, GPIO.OUT)
GPIO.output(led, 0)

def action(msg):
    chat_id = msg['chat']['id']
    command = msg.get('text', '').lower()

    if 'on' in command:
        if 'led' in command:
            GPIO.output(led, 1)
            telegram_bot.sendMessage(chat_id, "LED 💡 encendido")

    elif 'off' in command:
        if 'led' in command:
            GPIO.output(led, 0)
            telegram_bot.sendMessage(chat_id, "LED 💡 apagado")

TOKEN = "TU_TOKEN_DE_TELEGRAM_AQUI"
telegram_bot = telepot.Bot(TOKEN)

MessageLoop(telegram_bot, action).run_as_thread()
print("🤖 Bot funcionando... Envíale 'on led' o 'off led' desde Telegram")

while True:
    time.sleep(10)
