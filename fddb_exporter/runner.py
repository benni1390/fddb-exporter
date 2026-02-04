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
    set_reference_values()
    logger.info("Reference values initialized")
    iterations = 0
    while True:
        try:
            logger.debug("Starting scrape iteration %s", iterations + 1)
            html_content = fetch_fddb_data(username=os.getenv('FDDB_USERNAME'), password=os.getenv('FDDB_PASSWORD'), date_offset=int(os.getenv('FDDB_DATE_OFFSET', '0')), skip_login_errors=os.getenv('FDDB_SKIP_LOGIN_ERRORS','false').lower()=='true', debug_dir=os.getenv('DEBUG_OUTPUT_DIR'))
            data = parse_fddb_data(html_content)
            update_metrics(data)
            logger.debug("Completed scrape iteration %s", iterations + 1)
        except Exception:
            logger.exception("Error during scrape iteration %s", iterations + 1)
            # keep previous metrics

        iterations += 1
        if max_iterations is not None and iterations >= max_iterations:
            logger.info("Max iterations reached (%s), exiting run loop", max_iterations)
            break
        time.sleep(scrape_interval)


def main():
    port = int(os.getenv('EXPORTER_PORT', '8000'))
    scrape_interval = int(os.getenv('SCRAPE_INTERVAL', '3600'))
    logger.info("Starting fddb_exporter main: port=%s scrape_interval=%s", port, scrape_interval)
    run_loop(port, scrape_interval)
