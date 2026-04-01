import requests
import logging
from config import TRAVELPAYOUTS_TOKEN, TRAVELPAYOUTS_MARKER, ORIGIN, PRICE_THRESHOLDS

logger = logging.getLogger(__name__)
BASE_URL = "https://api.travelpayouts.com"


def get_cheap_prices(destination, currency="usd"):
      url = f"{BASE_URL}/v1/prices/cheap"
      params = {
          "origin": ORIGIN,
          "destination": destination,
          "currency": currency,
          "token": TRAVELPAYOUTS_TOKEN,
      }
      try:
                resp = requests.get(url, params=params, timeout=10)
                resp.raise_for_status()
                data = resp.json()
                if data.get("success") and data.get("data"):
                              dest_data = data["data"].get(destination, {})
                              if dest_data:
                                                return next(iter(dest_data.values()))
      except Exception as e:
                logger.error(f"Error cheap {destination}: {e}")
            return None


def get_special_offers(destination, currency="usd"):
      url = f"{BASE_URL}/v2/prices/latest"
    params = {
              "origin": ORIGIN,
              "destination": destination,
              "currency": currency,
              "token": TRAVELPAYOUTS_TOKEN,
              "limit": 1,
              "sorting": "price",
    }
    try:
              resp = requests.get(url, params=params, timeout=10)
              resp.raise_for_status()
              data = resp.json()
              if data.get("success") and data.get("data"):
                            return data["data"][0]
    except Exception as e:
        logger.error(f"Error special {destination}: {e}")
    return None


def build_affiliate_link(origin, destination, depart_date=""):
      marker = TRAVELPAYOUTS_MARKER or ""
    if depart_date:
              parts = depart_date.replace("-", "")
              date_str = parts[4:6] + parts[6:8] if len(parts) >= 8 else "0101"
else:
        date_str = "0101"
      base = f"https://www.aviasales.com/search/{origin}{destination}{date_str}"
    return f"{base}?marker={marker}" if marker else base


def find_deals(destinations):
      deals = []
    for dest in destinations:
              code = dest["code"]
              name = dest["name"]
              threshold = PRICE_THRESHOLDS.get(code, 300)

        price_data = get_cheap_prices(code)
        if price_data:
                      price = price_data.get("price", 9999)
                      if price <= threshold:
                                        deals.append({
                                                              "destination_code": code,
                                                              "destination_name": name,
                                                              "price": price,
                                                              "depart_date": price_data.get("depart_date", ""),
                                                              "return_date": price_data.get("return_date", ""),
                                                              "airline": price_data.get("airline", ""),
                                                              "link": build_affiliate_link(ORIGIN, code, price_data.get("depart_date", "")),
                                        })
                                    continue

        offer = get_special_offers(code)
        if offer:
                      price = offer.get("value", 9999)
            if price <= threshold:
                              depart = offer.get("depart_date", "")
                              deals.append({
                                  "destination_code": code,
                                  "destination_name": name,
                                  "price": price,
                                  "depart_date": depart,
                                  "return_date": offer.get("return_date", ""),
                                  "airline": offer.get("airline", ""),
                                  "link": build_affiliate_link(ORIGIN, code, depart),
                              })

    deals.sort(key=lambda x: x["price"])
    return deals
