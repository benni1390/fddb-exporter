import os
from unittest.mock import MagicMock, patch
import pytest

from exporter import fetch_fddb_data


class DummyResponse:
    def __init__(self, text='', status_code=200, url='https://fddb.info/foo'):
        self.text = text
        self.status_code = status_code
        self.url = url

    def raise_for_status(self):
        if self.status_code >= 400:
            raise Exception(f'HTTP {self.status_code}')


def make_session(login_ok=True, detail_href='/db/i18n/myday20/?lang=en'):
    session = MagicMock()

    # login post
    login_resp = DummyResponse(text='logged in', status_code=200, url='https://fddb.info/myfddb') if login_ok else DummyResponse(text='account?action=login', status_code=200, url='https://fddb.info/db/i18n/account/?lang=en&action=login')
    session.post.return_value = login_resp

    # notepad page: contains a link to detail
    notepad_html = f'<a href="{detail_href}">Detailansicht</a>'
    notepad_resp = DummyResponse(text=notepad_html, status_code=200, url='https://fddb.info/db/i18n/notepad/?lang=en')
    session.get.side_effect = [notepad_resp, DummyResponse(text='<div>myday content</div>', status_code=200, url='https://fddb.info/db/i18n/myday20/?lang=en')]

    return session


@patch('exporter.requests.Session')
def test_fetch_success(mock_session_class, tmp_path, monkeypatch):
    # ensure test data path not used
    monkeypatch.delenv('FDDB_USE_TEST_DATA', raising=False)

    mock_session_class.return_value = make_session(login_ok=True)

    # set credentials so login path is used
    monkeypatch.setenv('FDDB_USERNAME', 'user')
    monkeypatch.setenv('FDDB_PASSWORD', 'pass')

    html = fetch_fddb_data()
    assert 'myday' in html or 'myday' in html.lower()


@patch('exporter.requests.Session')
def test_fetch_skip_login(mock_session_class, monkeypatch):
    # simulate login failure but skip_login flag set
    session = make_session(login_ok=False)
    mock_session_class.return_value = session

    monkeypatch.setenv('FDDB_SKIP_LOGIN_ERRORS', 'true')
    monkeypatch.setenv('FDDB_USERNAME', 'user')
    monkeypatch.setenv('FDDB_PASSWORD', 'wrong')

    html = fetch_fddb_data()
    assert 'myday' in html


@patch('exporter.requests.Session')
def test_fetch_no_detail_link(mock_session_class, monkeypatch):
    # notepad page without detail links
    session = MagicMock()
    notepad_resp = DummyResponse(text='<html><body>No links</body></html>', status_code=200)
    session.post.return_value = DummyResponse(text='logged in', status_code=200, url='https://fddb.info/myfddb')
    session.get.side_effect = [notepad_resp]
    mock_session_class.return_value = session

    monkeypatch.setenv('FDDB_USERNAME', 'user')
    monkeypatch.setenv('FDDB_PASSWORD', 'pass')

    with pytest.raises(Exception):
        fetch_fddb_data()
