from unittest.mock import patch, MagicMock
from fddb_exporter.runner import run_loop


def test_run_loop_single_iteration(monkeypatch):
    # Patch start_http_server so it doesn't open a socket
    monkeypatch.setattr('fddb_exporter.runner.start_http_server', lambda port: None)

    # Patch fetcher, parser, updater
    monkeypatch.setattr('fddb_exporter.runner.fetch_fddb_data', lambda **kwargs: '<html></html>')
    monkeypatch.setattr('fddb_exporter.runner.parse_fddb_data', lambda html: {})
    monkeypatch.setattr('fddb_exporter.runner.update_metrics', lambda data: None)

    # Run loop with max_iterations=1 to exit immediately
    run_loop(port=8001, scrape_interval=0, max_iterations=1)
