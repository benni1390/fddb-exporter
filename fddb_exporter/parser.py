from bs4 import BeautifulSoup
from datetime import datetime


def parse_fddb_data(html_content):
    """Parse FDDB HTML and extract nutritional data."""
    soup = BeautifulSoup(html_content, 'html.parser')

    tables = soup.find_all('table', {'cellspacing': '0', 'cellpadding': '2'})
    data = {}

    for table in tables:
        rows = table.find_all('tr')
        for row in rows:
            cells = row.find_all('td')
            if len(cells) >= 2:
                key = cells[0].get_text(strip=True)
                value = cells[1].get_text(strip=True)
                if key and value:
                    data[key] = value

    # empty diary heuristic preserved
    if len(data) == 1 and '0 kJ' in str(data) and '0 kcal' in str(data):
        print(f"[{datetime.now()}] WARNING: Diary appears to be empty (0 kJ, 0 kcal)", flush=True)
        print(f"[{datetime.now()}] TIP: Try FDDB_DATE_OFFSET=-1 for yesterday's data", flush=True)

    return data
