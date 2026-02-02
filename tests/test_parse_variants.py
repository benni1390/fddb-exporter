from exporter import parse_fddb_data


def test_parse_empty_diary():
    html = '<html><body><table cellspacing="0" cellpadding="2"><tr><td>Calorific value</td><td>0 kJ 0 kcal</td></tr></table></body></html>'
    data = parse_fddb_data(html)
    # Should still return the key/value
    assert 'Calorific value' in data
    assert data['Calorific value'] == '0 kJ 0 kcal'


def test_parse_multiple_tables_and_rows():
    html = '''
    <html><body>
    <table cellspacing="0" cellpadding="2">
      <tr><td>Fat</td><td>5 g</td></tr>
    </table>
    <table cellspacing="0" cellpadding="2">
      <tr><td>Carbohydrates</td><td>20 g</td></tr>
      <tr><td>Protein</td><td>10 g</td></tr>
    </table>
    </body></html>
    '''
    data = parse_fddb_data(html)
    assert data.get('Fat') == '5 g'
    assert data.get('Carbohydrates') == '20 g'
    assert data.get('Protein') == '10 g'


def test_parse_ignores_empty_cells():
    html = '''
    <html><body>
    <table cellspacing="0" cellpadding="2">
      <tr><td></td><td> </td></tr>
      <tr><td>Salt</td><td>0.5 g</td></tr>
    </table>
    </body></html>
    '''
    data = parse_fddb_data(html)
    assert 'Salt' in data and data['Salt'] == '0.5 g'
