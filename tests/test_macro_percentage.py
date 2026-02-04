import pytest
from fddb_exporter.updater import update_metrics
from fddb_exporter.metrics import (
    fat_percentage, carbohydrates_percentage,
    protein_percentage, alcohol_percentage
)


def test_macronutrient_percentage_calculation():
    """Test that macronutrient percentages are calculated correctly"""
    data = {
        'Calorific value': '8368 KJ / 2000 kcal',
        'Fat': '66.7 g',
        'Carbohydrates': '250.0 g',
        'Protein': '100.0 g',
        'Alcohol': '0 g'
    }

    update_metrics(data)

    # Fat: 66.7g * 9 kcal/g = 600.3 kcal -> 30%
    # Carbs: 250g * 4 kcal/g = 1000 kcal -> 50%
    # Protein: 100g * 4 kcal/g = 400 kcal -> 20%
    # Alcohol: 0g * 7 kcal/g = 0 kcal -> 0%

    assert fat_percentage._value.get() == 30.0
    assert carbohydrates_percentage._value.get() == 50.0
    assert protein_percentage._value.get() == 20.0
    assert alcohol_percentage._value.get() == 0.0


def test_macronutrient_percentage_with_alcohol():
    """Test macronutrient percentages with alcohol"""
    data = {
        'Calorific value': '2100 KJ / 500 kcal',
        'Fat': '10 g',
        'Carbohydrates': '50 g',
        'Protein': '20 g',
        'Alcohol': '10 g'
    }

    update_metrics(data)

    # Fat: 10g * 9 = 90 kcal -> 18%
    # Carbs: 50g * 4 = 200 kcal -> 40%
    # Protein: 20g * 4 = 80 kcal -> 16%
    # Alcohol: 10g * 7 = 70 kcal -> 14%
    # Total: 440 kcal (88% of reported 500 kcal - typical discrepancy)

    assert fat_percentage._value.get() == 18.0
    assert carbohydrates_percentage._value.get() == 40.0
    assert protein_percentage._value.get() == 16.0
    assert alcohol_percentage._value.get() == 14.0


def test_macronutrient_percentage_zero_calories():
    """Test that zero calories doesn't cause division by zero"""
    data = {
        'Calorific value': '0 KJ / 0 kcal',
        'Fat': '0 g',
        'Carbohydrates': '0 g',
        'Protein': '0 g',
        'Alcohol': '0 g'
    }

    update_metrics(data)

    assert fat_percentage._value.get() == 0
    assert carbohydrates_percentage._value.get() == 0
    assert protein_percentage._value.get() == 0
    assert alcohol_percentage._value.get() == 0
