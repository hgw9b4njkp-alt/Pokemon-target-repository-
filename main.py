import os
import requests

TOKEN = os.environ[“TELEGRAM_BOT_TOKEN”]
CHAT_ID = os.environ[“TELEGRAM_CHAT_ID”]

def send_message(text):
url = f”https://api.telegram.org/bot{TOKEN}/sendMessage”
response = requests.post(
url,
json={“chat_id”: CHAT_ID, “text”: text},
timeout=20
)
response.raise_for_status()

def main():
send_message(
“🟢 Pokémon Target Monitor працює!\n\n”
“Хмарний запуск успішний. “
“Наступний крок — підключити моніторинг товарів Pokémon.”
)
print(“Telegram notification sent successfully.”)

if name == “main”:
main()
