import logging
import time
import schedule
from datetime import datetime
from config import DESTINATIONS, CHECK_INTERVAL_HOURS
from flights import find_deals
from bot import send_deal, send_deals_summary, test_bot_connection

logging.basicConfig(
      level=logging.INFO,
      format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
      datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

POSTED_DEALS: set = set()


def deal_key(deal: dict) -> str:
      return f"{deal['destination_code']}_{deal['price']}_{deal.get('depart_date', '')}"


def run_check():
      logger.info("=" * 50)
      logger.info(f"Iniciando busqueda - {datetime.now().strftime('%H:%M:%S')}")
      deals = find_deals(DESTINATIONS)
      if not deals:
                logger.info("No se encontraron ofertas.")
                return
            new_deals = [d for d in deals if deal_key(d) not in POSTED_DEALS]
    if not new_deals:
              logger.info("Todas las ofertas ya fueron publicadas.")
              return
          logger.info(f"{len(new_deals)} nuevas ofertas para publicar.")
    published = 0
    for deal in new_deals[:5]:
              success = send_deal(deal)
              if success:
                            POSTED_DEALS.add(deal_key(deal))
                            published += 1
                            time.sleep(2)
                    if len(new_deals) >= 3:
                              time.sleep(3)
                              send_deals_summary(new_deals[:10])
                          logger.info(f"Ciclo completado. {published} ofertas publicadas.")


def main():
      logger.info("Bot de Vuelos CDMX iniciando...")
    if not test_bot_connection():
              logger.error("No se pudo conectar con Telegram.")
        return
    logger.info(f"Revisando cada {CHECK_INTERVAL_HOURS} hora(s).")
    run_check()
    schedule.every(CHECK_INTERVAL_HOURS).hours.do(run_check)
    while True:
              schedule.run_pending()
        time.sleep(60)


if __name__ == "__main__":
      main()
