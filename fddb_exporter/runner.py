import os
import time
from prometheus_client import start_http_server
from .fetcher import fetch_fddb_data
from .parser import parse_fddb_data
from .updater import update_metrics


def run_loop(port=8000, scrape_interval=300, max_iterations=None):
    start_http_server(port)
    iterations = 0
    while True:
        try:
            html_content = fetch_fddb_data(username=os.getenv('FDDB_USERNAME'), password=os.getenv('FDDB_PASSWORD'), date_offset=int(os.getenv('FDDB_DATE_OFFSET', '0')), skip_login_errors=os.getenv('FDDB_SKIP_LOGIN_ERRORS','false').lower()=='true', debug_dir=os.getenv('DEBUG_OUTPUT_DIR'))
            data = parse_fddb_data(html_content)
            update_metrics(data)
        except Exception:
            # keep previous metrics
            pass
        iterations += 1
        if max_iterations is not None and iterations >= max_iterations:
            break
        time.sleep(scrape_interval)


def main():
    port = int(os.getenv('EXPORTER_PORT', '8000'))
    scrape_interval = int(os.getenv('SCRAPE_INTERVAL', '300'))
    run_loop(port, scrape_interval)
