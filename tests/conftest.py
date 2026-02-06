import pytest


@pytest.fixture(autouse=True)
def isolate_env(monkeypatch):
    """Ensure test isolation by cleaning up FDDB env vars before each test"""
    env_vars = [
        'FDDB_USERNAME', 'FDDB_PASSWORD', 'FDDB_USE_TEST_DATA',
        'FDDB_DATE_OFFSET', 'FDDB_SKIP_LOGIN_ERRORS', 'DEBUG_OUTPUT_DIR',
        'FDDB_DAILY_CALORIES', 'FDDB_BODYWEIGHT_KG', 'FDDB_FAT_G_PER_KG',
        'FDDB_CARBS_G_PER_KG', 'FDDB_PROTEIN_G_PER_KG', 'FDDB_ALCOHOL_G_PER_KG',
        'EXPORTER_PORT', 'SCRAPE_INTERVAL'
    ]
    for key in env_vars:
        monkeypatch.delenv(key, raising=False)


@pytest.fixture
def mock_runner_deps(monkeypatch):
    """Mock runner dependencies to avoid network calls and opening sockets"""
    monkeypatch.setattr('fddb_exporter.runner.start_http_server', lambda port: None)
    monkeypatch.setattr('fddb_exporter.runner.fetch_fddb_data', lambda **kwargs: '<html></html>')
    monkeypatch.setattr('fddb_exporter.runner.parse_fddb_data', lambda html: {})
    monkeypatch.setattr('fddb_exporter.runner.update_metrics', lambda data: None)
