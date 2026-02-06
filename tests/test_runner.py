import pytest
from fddb_exporter.runner import run_loop


def test_run_loop_single_iteration(mock_runner_deps, monkeypatch):
    monkeypatch.setenv('FDDB_USERNAME', 'testuser')
    monkeypatch.setenv('FDDB_PASSWORD', 'testpass')

    run_loop(port=8001, scrape_interval=0, max_iterations=1)


def test_run_loop_raises_error_missing_credentials(monkeypatch):
    monkeypatch.setattr('fddb_exporter.runner.start_http_server', lambda port: None)

    with pytest.raises(ValueError, match="FDDB_USERNAME and FDDB_PASSWORD are required"):
        run_loop(port=8002, scrape_interval=0, max_iterations=1)


