import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime


def fetch_fddb_data(session=None, username=None, password=None, date_offset=None, skip_login_errors=None, use_test_data=None, debug_dir=None):
    """Fetch data from FDDB. Accepts injected session for easier testing.
    If parameters are None, fall back to environment variables for backwards compatibility.
    """
    # resolve from env when not explicitly provided
    if use_test_data is None:
        use_test_data = os.getenv('FDDB_USE_TEST_DATA', 'false').lower() == 'true'
    if username is None:
        username = os.getenv('FDDB_USERNAME')
    if password is None:
        password = os.getenv('FDDB_PASSWORD')
    if date_offset is None:
        date_offset = int(os.getenv('FDDB_DATE_OFFSET', '0'))
    if skip_login_errors is None:
        skip_login_errors = os.getenv('FDDB_SKIP_LOGIN_ERRORS', 'false').lower() == 'true'
    if debug_dir is None:
        debug_dir = os.getenv('DEBUG_OUTPUT_DIR')

    if use_test_data:
        with open('.local/fddb_response_en.html', 'r', encoding='utf-8') as f:
            return f.read()

    sess = session or requests.Session()
    sess.headers.update({'User-Agent': 'fddb-exporter'})

    if username and password:
        login_url = 'https://fddb.info/db/i18n/account/?lang=en&action=login'
        login_data = {
            'loginemailorusername': username,
            'loginpassword': password,
            'returnurl': ''
        }
        try:
            login_response = sess.post(login_url, data=login_data, timeout=10, allow_redirects=True)
            login_response.raise_for_status()
            response_lower = login_response.text.lower()
            if 'myfddb' in login_response.url or 'abmelden' in response_lower or 'loginsuccess' in login_response.url:
                pass
            elif ('account' in login_response.url and 'action=login' in login_response.url):
                if 'falsch' in response_lower or 'incorrect' in response_lower:
                    if not skip_login_errors:
                        raise Exception('Login failed')
                elif 'loginemailorusername' in response_lower:
                    if not skip_login_errors:
                        raise Exception('Login failed')
                else:
                    if not skip_login_errors:
                        raise Exception('Login failed')
        except requests.exceptions.RequestException:
            if not skip_login_errors:
                raise

    notepad_url = 'https://fddb.info/db/i18n/notepad/?lang=en'
    notepad_response = sess.get(notepad_url, timeout=10)
    notepad_response.raise_for_status()

    soup = BeautifulSoup(notepad_response.text, 'html.parser')

    # check for "no entries" message
    page_text = notepad_response.text.lower()
    if 'no entries for this period' in page_text or 'keine einträge' in page_text:
        return '<html><body><table cellspacing="0" cellpadding="2"><tr><td>Energy:</td><td>0 kJ / 0 kcal</td></tr></table></body></html>'

    detail_links = soup.find_all('a', string=lambda text: text and 'detailansicht' in text.lower())
    if not detail_links:
        detail_links = soup.find_all('a', href=lambda href: href and 'myday20' in href)

    if detail_links:
        links_to_check = detail_links[:5] if date_offset == 0 else detail_links
        diary_url = None
        for i, link in enumerate(links_to_check):
            href = link.get('href')
            if href:
                if not href.startswith('http'):
                    diary_url = f"https://fddb.info/{href.lstrip('/')}"
                else:
                    diary_url = href
                if date_offset == 0 and i == 0:
                    break
                elif date_offset != 0 and i == abs(date_offset):
                    break
        if not diary_url and detail_links:
            href = detail_links[0].get('href')
            diary_url = f"https://fddb.info/{href.lstrip('/')}" if not href.startswith('http') else href
    else:
        if debug_dir:
            try:
                os.makedirs(debug_dir, exist_ok=True)
                debug_file = f"{debug_dir}/fddb_notepad_nodetail_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
                with open(debug_file, 'w', encoding='utf-8') as f:
                    f.write(notepad_response.text)
            except Exception:
                pass
        return notepad_response.text

    response = sess.get(diary_url, timeout=10)
    response.raise_for_status()

    # debug save
    if debug_dir:
        try:
            os.makedirs(debug_dir, exist_ok=True)
            debug_file = f"{debug_dir}/fddb_response_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
            with open(debug_file, 'w', encoding='utf-8') as f:
                f.write(response.text)
        except Exception:
            pass

    return response.text
