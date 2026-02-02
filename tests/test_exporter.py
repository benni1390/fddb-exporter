import os
from prometheus_client import core

from exporter import extract_number, parse_fddb_data, update_metrics


def test_extract_number_basic():
    assert extract_number("1,23 g") == 1.23
    assert extract_number("0") == 0.0
    assert extract_number("") == 0.0
    assert extract_number("1.234") == 1.234
    assert extract_number("abc") == 0.0


def test_parse_fddb_data_table():
    html = '''
    <html><body>
    <table cellspacing="0" cellpadding="2">
      <tr><td>Calorific value</td><td>1000 KJ 240 kcal</td></tr>
      <tr><td>Fat</td><td>10 g</td></tr>
    </table>
    </body></html>
    '''
    data = parse_fddb_data(html)
    assert data.get('Calorific value') == '1000 KJ 240 kcal'
    assert data.get('Fat') == '10 g'


def test_update_metrics_sets_gauges():
    # Use a simple data dict and call update_metrics
    data = {'Calorific value': '1000 KJ 240 kcal', 'Fat': '10 g'}
    update_metrics(data)

    # Read back values from the global registry
    assert core.REGISTRY.get_sample_value('fddb_energy_kj') == 1000.0
    assert core.REGISTRY.get_sample_value('fddb_energy_kcal') == 240.0
    assert core.REGISTRY.get_sample_value('fddb_fat_grams') == 10.0
