from unittest.mock import MagicMock, patch
import requests
import pytest

from exporter import fetch_fddb_data


class DummyResponse:
    def __init__(self, text='', status_code=200, url='https://fddb.info/foo'):
        self.text = text
        self.status_code = status_code
        self.url = url

    def raise_for_status(self):
        if self.status_code >= 400:
            raise requests.exceptions.HTTPError(f'HTTP {self.status_code}')


@patch('exporter.requests.Session')
def test_login_failure_wrong_credentials(mock_session_class, monkeypatch):
    # Simulate login response staying on login page with 'incorrect' in response
    session = MagicMock()
    login_resp = DummyResponse(text='Incorrect username or password', status_code=200, url='https://fddb.info/db/i18n/account/?lang=en&action=login')
    session.post.return_value = login_resp
    # notepad won't be fetched because login fails and skip not set
    mock_session_class.return_value = session

    monkeypatch.setenv('FDDB_USERNAME', 'user')
    monkeypatch.setenv('FDDB_PASSWORD', 'badpass')
    monkeypatch.delenv('FDDB_SKIP_LOGIN_ERRORS', raising=False)

    with pytest.raises(Exception):
        fetch_fddb_data()


@patch('exporter.requests.Session')
def test_login_failure_loginemailorusername_message(mock_session_class, monkeypatch):
    session = MagicMock()
    login_resp = DummyResponse(text='loginemailorusername', status_code=200, url='https://fddb.info/db/i18n/account/?lang=en&action=login')
    session.post.return_value = login_resp
    mock_session_class.return_value = session

    monkeypatch.setenv('FDDB_USERNAME', 'user')
    monkeypatch.setenv('FDDB_PASSWORD', 'badpass')
    monkeypatch.delenv('FDDB_SKIP_LOGIN_ERRORS', raising=False)

    with pytest.raises(Exception):
        fetch_fddb_data()


@patch('exporter.requests.Session')
def test_login_request_exception_skip(monkey_session_class, monkeypatch):
    # If login request raises RequestException and skip flag true, should continue
    session = MagicMock()
    def raise_req(*args, **kwargs):
        raise requests.exceptions.RequestException('network')
    session.post.side_effect = raise_req
    # notepad and diary responses after skipping login
    notepad_resp = DummyResponse(text='<a href="/db/i18n/myday20/?lang=en">Detail</a>')
    diary_resp = DummyResponse(text='<div>myday content</div>')
    session.get.side_effect = [notepad_resp, diary_resp]
    monkey_session_class.return_value = session

    monkeypatch.setenv('FDDB_USERNAME', 'user')
    monkeypatch.setenv('FDDB_PASSWORD', 'badpass')
    monkeypatch.setenv('FDDB_SKIP_LOGIN_ERRORS', 'true')

    html = fetch_fddb_data()
    assert 'myday' in html


@patch('exporter.requests.Session')
def test_placeholder_username_skipped_login(mock_session_class, monkeypatch):
    # If username equals placeholder, login is skipped and not fatal
    session = MagicMock()
    notepad_resp = DummyResponse(text='<a href="/db/i18n/myday20/?lang=en">Detail</a>')
    diary_resp = DummyResponse(text='<div>myday content</div>')
    session.get.side_effect = [notepad_resp, diary_resp]
    mock_session_class.return_value = session

    monkeypatch.setenv('FDDB_USERNAME', 'your_username')
    monkeypatch.delenv('FDDB_PASSWORD', raising=False)

    html = fetch_fddb_data()
    assert 'myday' in html


@patch('exporter.requests.Session')
def test_unclear_login_status_continues(mock_session_class, monkeypatch):
    # If login response is not clearly successful or login page, code continues
    session = MagicMock()
    login_resp = DummyResponse(text='some page', status_code=200, url='https://fddb.info/somepage')
    session.post.return_value = login_resp
    notepad_resp = DummyResponse(text='<a href="/db/i18n/myday20/?lang=en">Detail</a>')
    diary_resp = DummyResponse(text='<div>content</div>')
    session.get.side_effect = [notepad_resp, diary_resp]
    mock_session_class.return_value = session

    monkeypatch.setenv('FDDB_USERNAME', 'user')
    monkeypatch.setenv('FDDB_PASSWORD', 'pass')

    html = fetch_fddb_data()
    assert 'content' in html
