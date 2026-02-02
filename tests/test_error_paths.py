import os
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
def test_notepad_timeout_raises(mock_session_class):
    session = MagicMock()
    # simulate timeout on notepad fetch
    session.get.side_effect = requests.exceptions.Timeout()
    mock_session_class.return_value = session

    with pytest.raises(Exception):
        fetch_fddb_data()


@patch('exporter.requests.Session')
def test_diary_timeout_raises(mock_session_class, monkeypatch):
    # notepad ok, diary raises Timeout
    session = MagicMock()
    notepad_resp = DummyResponse(text='<a href="/db/i18n/myday20/?lang=en">Detail</a>')
    session.get.side_effect = [notepad_resp, requests.exceptions.Timeout()]
    session.post.return_value = DummyResponse(text='logged in', url='https://fddb.info/myfddb')
    mock_session_class.return_value = session

    monkeypatch.setenv('FDDB_USERNAME', 'user')
    monkeypatch.setenv('FDDB_PASSWORD', 'pass')

    with pytest.raises(requests.exceptions.Timeout):
        fetch_fddb_data()


@patch('exporter.requests.Session')
def test_http_error_in_notepad(mock_session_class, monkeypatch):
    session = MagicMock()
    notepad_resp = DummyResponse(text='error', status_code=500)
    session.get.side_effect = [notepad_resp]
    session.post.return_value = DummyResponse(text='logged in', url='https://fddb.info/myfddb')
    mock_session_class.return_value = session

    monkeypatch.setenv('FDDB_USERNAME', 'user')
    monkeypatch.setenv('FDDB_PASSWORD', 'pass')

    with pytest.raises(Exception):
        fetch_fddb_data()


@patch('exporter.requests.Session')
def test_debug_output_writes_file(mock_session_class, tmp_path, monkeypatch):
    # notepad and diary ok
    session = MagicMock()
    notepad_resp = DummyResponse(text='<a href="/db/i18n/myday20/?lang=en">Detail</a>')
    diary_resp = DummyResponse(text='<div>myday content</div>')
    session.get.side_effect = [notepad_resp, diary_resp]
    session.post.return_value = DummyResponse(text='logged in', url='https://fddb.info/myfddb')
    mock_session_class.return_value = session

    monkeypatch.setenv('FDDB_USERNAME', 'user')
    monkeypatch.setenv('FDDB_PASSWORD', 'pass')
    debug_dir = tmp_path / "debug"
    monkeypatch.setenv('DEBUG_OUTPUT_DIR', str(debug_dir))

    html = fetch_fddb_data()
    assert 'myday' in html

    # check debug file exists
    files = list(debug_dir.iterdir())
    assert len(files) == 1
    assert files[0].suffix == '.html'


@patch('exporter.requests.Session')
def test_notepad_multiple_links_offset(mock_session_class, monkeypatch):
    # multiple links, offset selects second link
    session = MagicMock()
    notepad_html = '<a href="/db/i18n/myday20/1?lang=en">one</a><a href="/db/i18n/myday20/2?lang=en">two</a>'
    notepad_resp = DummyResponse(text=notepad_html)
    # diary for second link
    diary_second = DummyResponse(text='<div>second</div>', url='https://fddb.info/db/i18n/myday20/2?lang=en')
    session.get.side_effect = [notepad_resp, diary_second]
    session.post.return_value = DummyResponse(text='logged in', url='https://fddb.info/myfddb')
    mock_session_class.return_value = session

    monkeypatch.setenv('FDDB_USERNAME', 'user')
    monkeypatch.setenv('FDDB_PASSWORD', 'pass')
    monkeypatch.setenv('FDDB_DATE_OFFSET', '-1')

    html = fetch_fddb_data()
    assert 'second' in html
