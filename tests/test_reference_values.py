import pytest
from prometheus_client import REGISTRY
from fddb_exporter.reference_values import (
    set_reference_values,
    fat_ref, carbohydrates_ref, sugar_ref, protein_ref, fiber_ref, water_ref, cholesterol_ref, alcohol_ref,
    vitamin_c_ref, vitamin_a_ref, vitamin_d_ref, vitamin_e_ref,
    vitamin_b1_ref, vitamin_b2_ref, vitamin_b6_ref, vitamin_b12_ref,
    iron_ref, zinc_ref, magnesium_ref, calcium_ref,
    potassium_ref, phosphorus_ref, iodine_ref, selenium_ref
)


def test_reference_values_set():
    set_reference_values()

    # Macronutrients (2400 kcal default, 90kg bodyweight)
    assert fat_ref._value.get() == 90.0  # 1.0 g/kg * 90kg
    assert carbohydrates_ref._value.get() == 360.0  # 4.0 g/kg * 90kg
    assert sugar_ref._value.get() == 60.0  # 2400 * 0.10 / 4
    assert protein_ref._value.get() == 180.0  # 2.0 g/kg * 90kg
    assert fiber_ref._value.get() == 30.0
    assert water_ref._value.get() == 2.0
    assert cholesterol_ref._value.get() == 300
    assert alcohol_ref._value.get() == 20  # default when 0 g/kg

    # Vitamins (at 2400 kcal baseline, scale_factor = 1.0)
    assert vitamin_c_ref._value.get() == 100.0
    assert vitamin_a_ref._value.get() == 0.85
    assert vitamin_d_ref._value.get() == 0.020
    assert vitamin_e_ref._value.get() == 12.0
    assert vitamin_b1_ref._value.get() == 1.2
    assert vitamin_b2_ref._value.get() == 1.3
    assert vitamin_b6_ref._value.get() == 1.4
    assert vitamin_b12_ref._value.get() == 0.004

    # Minerals (at 2400 kcal baseline, scale_factor = 1.0)
    assert iron_ref._value.get() == 12.5
    assert zinc_ref._value.get() == 9.0
    assert magnesium_ref._value.get() == 350.0
    assert calcium_ref._value.get() == 1000.0
    assert potassium_ref._value.get() == 4000.0
    assert phosphorus_ref._value.get() == 700.0
    assert iodine_ref._value.get() == 0.200
    assert selenium_ref._value.get() == 0.060


def test_reference_values_registered():
    """Ensure reference metrics are registered with Prometheus"""
    metric_names = [m.name for m in REGISTRY.collect()]

    assert 'fddb_fat_reference_grams' in metric_names
    assert 'fddb_carbohydrates_reference_grams' in metric_names
    assert 'fddb_sugar_reference_grams' in metric_names
    assert 'fddb_protein_reference_grams' in metric_names
    assert 'fddb_fiber_reference_grams' in metric_names
    assert 'fddb_water_reference_liters' in metric_names
    assert 'fddb_cholesterol_reference_mg' in metric_names
    assert 'fddb_alcohol_reference_grams' in metric_names
    assert 'fddb_vitamin_c_reference_mg' in metric_names
    assert 'fddb_vitamin_a_reference_mg' in metric_names
    assert 'fddb_vitamin_d_reference_mg' in metric_names
    assert 'fddb_vitamin_e_reference_mg' in metric_names
    assert 'fddb_vitamin_b1_reference_mg' in metric_names
    assert 'fddb_vitamin_b2_reference_mg' in metric_names
    assert 'fddb_vitamin_b6_reference_mg' in metric_names
    assert 'fddb_vitamin_b12_reference_mg' in metric_names
    assert 'fddb_iron_reference_mg' in metric_names
    assert 'fddb_zinc_reference_mg' in metric_names
    assert 'fddb_magnesium_reference_mg' in metric_names
    assert 'fddb_calcium_reference_mg' in metric_names
    assert 'fddb_potassium_reference_mg' in metric_names
    assert 'fddb_phosphorus_reference_mg' in metric_names
    assert 'fddb_iodine_reference_mg' in metric_names
    assert 'fddb_selenium_reference_mg' in metric_names


def test_reference_values_custom_calories():
    """Test reference values with custom daily calories and bodyweight"""
    set_reference_values(daily_calories=3000, bodyweight_kg=80,
                        fat_g_per_kg=1.2, carbs_g_per_kg=5.0,
                        protein_g_per_kg=2.5, alcohol_g_per_kg=0.1)

    scale_factor = 3000 / 2400  # 1.25

    # Macronutrients should use bodyweight-based calculation
    assert fat_ref._value.get() == 96.0  # 1.2 * 80
    assert carbohydrates_ref._value.get() == 400.0  # 5.0 * 80
    assert sugar_ref._value.get() == 75.0  # 3000 * 0.10 / 4
    assert protein_ref._value.get() == 200.0  # 2.5 * 80
    assert fiber_ref._value.get() == 37.5  # 30 * 1.25
    assert water_ref._value.get() == 2.5  # 2.0 * 1.25
    assert alcohol_ref._value.get() == 8.0  # 0.1 * 80

    # These should remain constant
    assert cholesterol_ref._value.get() == 300

    # Vitamins should scale
    assert vitamin_c_ref._value.get() == round(100 * scale_factor, 3)
    assert vitamin_e_ref._value.get() == round(12 * scale_factor, 3)

    # Minerals should scale
    assert magnesium_ref._value.get() == round(350 * scale_factor, 1)
    assert calcium_ref._value.get() == round(1000 * scale_factor, 1)

