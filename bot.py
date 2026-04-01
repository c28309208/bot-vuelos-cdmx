import requests
import logging
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHANNEL_ID

logger = logging.getLogger(__name__)
TELEGRAM_API = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"

REGION_EMOJIS = {
      "MIA": "🇺🇸", "JFK": "🇺🇸", "LAX": "🇺🇸", "ORD": "🇺🇸",
      "MAD": "🇪🇸", "BCN": "🇪🇸",
      "BOG": "🇨🇴", "LIM": "🇵🇪", "SCL": "🇨🇱", "GRU": "🇧🇷",
      "EZE": "🇦🇷", "UIO": "🇪🇨", "GUA": "🇬🇹", "SAL": "🇸🇻",
      "MGA": "🇳🇮", "SJO": "🇨🇷", "PTY": "🇵🇦", "SDQ": "🇩🇴",
      "CUN": "🇲🇽", "GDL": "🇲🇽",
}

AIRLINE_NAMES = {
      "AM": "Aeromexico", "VB": "VivaAerobus", "Y4": "Volaris",
      "IB": "Iberia", "AA": "American", "UA": "United",
      "DL": "Delta", "LA": "LATAM", "AV": "Avianca",
      "CM": "Copa", "WN": "Southwest",
}


def build_deal_message(deal):
      code = deal["destination_code"]
      name = deal["destination_name"]
      price = deal["price"]
      depart = deal.get("depart_date", "")
      ret = deal.get("return_date", "")
      airline_code = deal.get("airline", "")
      airline = AIRLINE_NAMES.get(airline_code, airline_code)
      link = deal.get("link", "")
      flag = REGION_EMOJIS.get(code, "✈️")

    lines = [
              f"🔥 *OFERTA: {name}* {flag}",
              f"",
              f"💵 *Precio: ${price} USD* (ida y vuelta)",
    ]
    if depart:
              lines.append(f"📅 Salida: {depart}")
          if ret:
                    lines.append(f"🔙 Regreso: {ret}")
                if airline:
                          lines.append(f"✈️ Aerolínea: {airline}")
                      lines.append(f"")
    lines.append(f"👉 [Ver vuelo y reservar]({link})")
    lines.append(f"")
    lines.append(f"_Precios sujetos a cambio. Verifica disponibilidad._")
    return "\n".join(lines)


def send_message(text, parse_mode="Markdown"):
      url = f"{TELEGRAM_API}/sendMessage"
      payload = {
          "chat_id": TELEGRAM_CHANNEL_ID,
          "text": text,
          "parse_mode": parse_mode,
          "disable_web_page_preview": False,
      }
      try:
                resp = requests.post(url, json=payload, timeout=10)
                resp.raise_for_status()
                return resp.json()
except Exception as e:
        logger.error(f"Error sending message: {e}")
        return None


def send_deal(deal):
      msg = build_deal_message(deal)
      return send_message(msg)


def send_deals_summary(deals):
      if not deals:
                return
            header = f"🛫 *{len(deals)} OFERTAS DESDE CDMX* 🛫\n\n¡Precios increíbles encontrados ahora mismo!"
    send_message(header)
    for deal in deals:
              send_deal(deal)


def test_bot_connection():
      url = f"{TELEGRAM_API}/getMe"
    try:
              resp = requests.get(url, timeout=10)
              resp.raise_for_status()
              data = resp.json()
              if data.get("ok"):
                            bot_name = data["result"].get("username", "unknown")
                            logger.info(f"Bot conectado: @{bot_name}")
                            return True
    except Exception as e:
        logger.error(f"Error conectando bot: {e}")
    return False
