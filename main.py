import os
import time
import requests
from datetime import datetime

TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

PRODUCT_URLS = [
    url.strip()
    for url in os.environ.get("PRODUCT_URLS", "").split(";")
    if url.strip()
]

CHECK_INTERVAL = 600  # Перевірка кожні 10 хвилин

session = requests.Session()
session.headers.update({
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/131.0.0.0 Safari/537.36"
    )
})

last_states = {}


def send_message(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    response = requests.post(
        url,
        json={"chat_id": CHAT_ID, "text": text},
        timeout=20
    )
    response.raise_for_status()


def check_product(url):
    response = session.get(url, timeout=25)
    response.raise_for_status()
    html = response.text.lower()

    # Не повідомляємо про наявність, якщо сторінка
    # не містить очевидних ознак товару.
    if "add to cart" in html or "add to basket" in html:
        return "possible_stock"

    if any(word in html for word in [
        "out of stock",
        "sold out",
        "currently unavailable",
    ]):
        return "unavailable"

    return "unknown"


def main():
    send_message(
        "🟢 Pokémon Target Monitor запущено!\n"
        f"Товарів у списку: {len(PRODUCT_URLS)}\n"
        "Перевірка кожні 10 хвилин."
    )

    while True:
        for url in PRODUCT_URLS:
            try:
                state = check_product(url)
                previous = last_states.get(url)

                if state == "possible_stock" and previous != "possible_stock":
                    send_message(
                        "🎯 Можлива наявність Pokémon у Target!\n\n"
                        f"{url}\n\n"
                        "Перевір сторінку вручну: наявність ще потрібно підтвердити."
                    )

                last_states[url] = state

            except Exception as error:
                print(
                    f"[{datetime.now().isoformat()}] "
                    f"Помилка перевірки {url}: {error}",
                    flush=True
                )

        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    main()
