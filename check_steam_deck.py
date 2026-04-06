import os
import requests

TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

URL_NEW = "https://store.steampowered.com/api/appdetails?appids=1675200"
URL_REFURB = "https://store.steampowered.com/sale/steamdeckrefurbished?l=english"


def send_telegram(text):
    try:
        requests.post(
            f"https://api.telegram.org/bot{TOKEN}/sendMessage",
            json={"chat_id": CHAT_ID, "text": text},
            timeout=10,
        )
        print("Telegram sent:", text[:60])
    except Exception as e:
        print("Telegram error:", e)


def check_new():
    try:
        r = requests.get(URL_NEW, timeout=10)
        data = r.json()
        store_data = data["1675200"]["data"]
        if "purchase_options" in store_data:
            return True
    except Exception as e:
        print("Error checking new stock:", e)
    return False


def check_refurb():
    try:
        r = requests.get(
            URL_REFURB,
            headers={"User-Agent": "Mozilla/5.0"},
            timeout=15,
        )
        text = r.text
        if "currently out of stock" not in text and "$5XX" not in text:
            return True
    except Exception as e:
        print("Error checking refurb stock:", e)
    return False


new_in_stock = check_new()
refurb_in_stock = check_refurb()

print(f"New Steam Deck in stock: {new_in_stock}")
print(f"Refurb 512GB OLED in stock: {refurb_in_stock}")

if new_in_stock:
    send_telegram(
        "🔥 Steam Deck В НАЛИЧИИ!\n"
        "https://store.steampowered.com/steamdeck"
    )

if refurb_in_stock:
    send_telegram(
        "♻️ Steam Deck 512GB OLED (восстановленный) В НАЛИЧИИ!\n"
        "https://store.steampowered.com/sale/steamdeckrefurbished"
    )

if not new_in_stock and not refurb_in_stock:
    print("Nothing in stock. No notification sent.")
