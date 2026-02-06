import os
import sys
import time
import logging
from prometheus_client import start_http_server
from .fetcher import fetch_fddb_data
from .parser import parse_fddb_data
from .updater import update_metrics
from .reference_values import set_reference_values

# Configure logging to stdout (force unbuffered for K8s)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    stream=sys.stdout,
    force=True
)
logger = logging.getLogger("fddb_exporter")
logger.setLevel(logging.INFO)


def run_loop(port=8000, scrape_interval=300, max_iterations=None):
    start_http_server(port)
    logger.info("HTTP metrics server started on port %s", port)

    daily_calories = int(os.getenv('FDDB_DAILY_CALORIES', '2400'))
    bodyweight_kg = float(os.getenv('FDDB_BODYWEIGHT_KG', '90'))
    fat_g_per_kg = float(os.getenv('FDDB_FAT_G_PER_KG', '1.0'))
    carbs_g_per_kg = float(os.getenv('FDDB_CARBS_G_PER_KG', '4.0'))
    protein_g_per_kg = float(os.getenv('FDDB_PROTEIN_G_PER_KG', '2.0'))
    alcohol_g_per_kg = float(os.getenv('FDDB_ALCOHOL_G_PER_KG', '0.0'))

    set_reference_values(daily_calories, bodyweight_kg, fat_g_per_kg,
                        carbs_g_per_kg, protein_g_per_kg, alcohol_g_per_kg)
    logger.info("Reference values initialized (calories=%s, bodyweight=%skg, fat=%sg/kg, carbs=%sg/kg, protein=%sg/kg)",
                daily_calories, bodyweight_kg, fat_g_per_kg, carbs_g_per_kg, protein_g_per_kg)
    iterations = 0
    while True:
        try:
            iterations += 1
            logger.debug("Starting scrape iteration %s", iterations)
            html_content = fetch_fddb_data(username=os.getenv('FDDB_USERNAME'), password=os.getenv('FDDB_PASSWORD'), date_offset=int(os.getenv('FDDB_DATE_OFFSET', '0')), skip_login_errors=os.getenv('FDDB_SKIP_LOGIN_ERRORS','false').lower()=='true', debug_dir=os.getenv('DEBUG_OUTPUT_DIR'))
            data = parse_fddb_data(html_content)
            update_metrics(data)
            logger.info("Scrape iteration %s successful", iterations)
        except Exception as e:
            logger.error("Error during scrape iteration %s: %s", iterations, str(e))
            logger.debug("Full traceback:", exc_info=True)
            # keep previous metrics

        if max_iterations is not None and iterations >= max_iterations:
            logger.info("Max iterations reached (%s), exiting run loop", max_iterations)
            break
        time.sleep(scrape_interval)


def main():
    port = int(os.getenv('EXPORTER_PORT', '8000'))
    scrape_interval = int(os.getenv('SCRAPE_INTERVAL', '3600'))
    logger.info("Starting fddb_exporter main: port=%s scrape_interval=%s", port, scrape_interval)
    run_loop(port, scrape_interval)
