import pytest
from prometheus_client import REGISTRY
from fddb_exporter.reference_values import (
    set_reference_values,
    vitamin_c_ref, vitamin_a_ref, vitamin_d_ref, vitamin_e_ref,
    vitamin_b1_ref, vitamin_b2_ref, vitamin_b6_ref, vitamin_b12_ref,
    iron_ref, zinc_ref, magnesium_ref, calcium_ref,
    potassium_ref, phosphorus_ref, iodine_ref, selenium_ref
)


def test_reference_values_set():
    set_reference_values()

    # Vitamins
    assert vitamin_c_ref._value.get() == 100
    assert vitamin_a_ref._value.get() == 0.85
    assert vitamin_d_ref._value.get() == 0.020
    assert vitamin_e_ref._value.get() == 12
    assert vitamin_b1_ref._value.get() == 1.2
    assert vitamin_b2_ref._value.get() == 1.3
    assert vitamin_b6_ref._value.get() == 1.4
    assert vitamin_b12_ref._value.get() == 0.004

    # Minerals
    assert iron_ref._value.get() == 12.5
    assert zinc_ref._value.get() == 9
    assert magnesium_ref._value.get() == 350
    assert calcium_ref._value.get() == 1000
    assert potassium_ref._value.get() == 4000
    assert phosphorus_ref._value.get() == 700
    assert iodine_ref._value.get() == 0.200
    assert selenium_ref._value.get() == 0.060


def test_reference_values_registered():
    """Ensure reference metrics are registered with Prometheus"""
    metric_names = [m.name for m in REGISTRY.collect()]

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
