import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHANNEL_ID = os.getenv("TELEGRAM_CHANNEL_ID")

TRAVELPAYOUTS_TOKEN = os.getenv("TRAVELPAYOUTS_TOKEN")
TRAVELPAYOUTS_MARKER = os.getenv("TRAVELPAYOUTS_MARKER")

ORIGIN = "MEX"
MAX_PRICE_USD = int(os.getenv("MAX_PRICE_USD", "250"))
CHECK_INTERVAL_HOURS = int(os.getenv("CHECK_INTERVAL_HOURS", "4"))

DESTINATIONS = [
      {"code": "MIA", "name": "Miami, EE.UU."},
      {"code": "JFK", "name": "Nueva York, EE.UU."},
      {"code": "LAX", "name": "Los Angeles, EE.UU."},
      {"code": "MAD", "name": "Madrid, Espana"},
      {"code": "BCN", "name": "Barcelona, Espana"},
      {"code": "BOG", "name": "Bogota, Colombia"},
      {"code": "LIM", "name": "Lima, Peru"},
      {"code": "GRU", "name": "Sao Paulo, Brasil"},
      {"code": "EZE", "name": "Buenos Aires, Argentina"},
      {"code": "SCL", "name": "Santiago, Chile"},
      {"code": "HAV", "name": "La Habana, Cuba"},
      {"code": "CUN", "name": "Cancun, Mexico"},
      {"code": "GDL", "name": "Guadalajara, Mexico"},
      {"code": "MTY", "name": "Monterrey, Mexico"},
      {"code": "ORD", "name": "Chicago, EE.UU."},
      {"code": "YYZ", "name": "Toronto, Canada"},
      {"code": "CDG", "name": "Paris, Francia"},
      {"code": "LHR", "name": "Londres, Reino Unido"},
      {"code": "AMS", "name": "Amsterdam, Holanda"},
      {"code": "FCO", "name": "Roma, Italia"},
]

PRICE_THRESHOLDS = {
      "MIA": 200, "JFK": 220, "LAX": 180, "MAD": 380, "BCN": 400,
      "BOG": 180, "LIM": 200, "GRU": 250, "EZE": 280, "SCL": 280,
      "HAV": 250, "CUN": 80,  "GDL": 60,  "MTY": 70,  "ORD": 180,
      "YYZ": 230, "CDG": 400, "LHR": 380, "AMS": 390, "FCO": 410,
}
