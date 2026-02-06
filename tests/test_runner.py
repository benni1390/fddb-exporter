from unittest.mock import patch, MagicMock
from fddb_exporter.runner import run_loop
import logging


def test_run_loop_single_iteration(monkeypatch):
    # Patch start_http_server so it doesn't open a socket
    monkeypatch.setattr('fddb_exporter.runner.start_http_server', lambda port: None)

    # Patch fetcher, parser, updater
    monkeypatch.setattr('fddb_exporter.runner.fetch_fddb_data', lambda **kwargs: '<html></html>')
    monkeypatch.setattr('fddb_exporter.runner.parse_fddb_data', lambda html: {})
    monkeypatch.setattr('fddb_exporter.runner.update_metrics', lambda data: None)

    # Set required credentials
    monkeypatch.setenv('FDDB_USERNAME', 'testuser')
    monkeypatch.setenv('FDDB_PASSWORD', 'testpass')

    # Run loop with max_iterations=1 to exit immediately
    run_loop(port=8001, scrape_interval=0, max_iterations=1)


def test_run_loop_raises_error_missing_credentials(monkeypatch):
    monkeypatch.setattr('fddb_exporter.runner.start_http_server', lambda port: None)

    # Set to empty string to ensure they are falsy
    monkeypatch.setenv('FDDB_USERNAME', '')
    monkeypatch.setenv('FDDB_PASSWORD', '')

    import pytest
    with pytest.raises(ValueError, match="FDDB_USERNAME and FDDB_PASSWORD are required"):
        run_loop(port=8002, scrape_interval=0, max_iterations=1)


