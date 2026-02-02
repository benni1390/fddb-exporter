from prometheus_client import core
from exporter import update_metrics


def make_data():
    return {
        'Calorific value': '1000 KJ 240 kcal',
        'Fat': '10 g',
        'Carbohydrates': '20 g',
        'thereof Sugar': '5 g',
        'Protein': '30 g',
        'Alcohol': '0 g',
        'Water': '0.5 l',
        'Dietary fibre': '3 g',
        'Cholesterol': '2 mg',
        'Vitamin C': '50 mg',
        'Retinol': '0.1 mg',
        'Vitamin D': '0.01 mg',
        'Vitamin E': '1 mg',
        'Thiamine': '0.2 mg',
        'Riboflavin': '0.3 mg',
        'Vitamin B6': '0.4 mg',
        'Vitamin B12': '0.005 mg',
        'Salt': '1 g',
        'Iron': '2 mg',
        'Zinc': '3 mg',
        'Magnesium': '4 mg',
        'Manganese': '0.1 mg',
        'Fluorine': '0.02 mg',
        'Chlorine': '0.5 mg',
        'Copper': '0.05 mg',
        'Potassium': '150 mg',
        'Calcium': '100 mg',
        'Phosphorus': '200 mg',
        'Sulphur': '10 mg',
        'Iodine': '0.01 mg',
    }


def test_update_metrics_all_keys():
    data = make_data()
    update_metrics(data)

    # spot-check a few metrics were set
    assert core.REGISTRY.get_sample_value('fddb_energy_kj') == 1000.0
    assert core.REGISTRY.get_sample_value('fddb_fat_grams') == 10.0
    assert core.REGISTRY.get_sample_value('fddb_vitamin_c_mg') == 50.0
    assert core.REGISTRY.get_sample_value('fddb_iron_mg') == 2.0
    assert core.REGISTRY.get_sample_value('fddb_calcium_mg') == 100.0
