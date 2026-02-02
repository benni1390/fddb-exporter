import re
from . import metrics


def extract_number(text):
    if not text:
        return 0.0
    # Remove all non-numeric except comma and dot
    cleaned = re.sub(r'[^\d,.]', '', text)
    cleaned = cleaned.replace(',', '.')
    try:
        return float(cleaned)
    except ValueError:
        return 0.0


def update_metrics(data):
    # Energy
    if 'Calorific value' in data:
        match = re.search(r"(\d+)\s*KJ.*?(\d+)\s*kcal", data['Calorific value'])
        if match:
            metrics.energy_kj.set(float(match.group(1)))
            metrics.energy_kcal.set(float(match.group(2)))

    # Macros
    if 'Fat' in data:
        metrics.fat_grams.set(extract_number(data['Fat']))
    if 'Carbohydrates' in data:
        metrics.carbohydrates_grams.set(extract_number(data['Carbohydrates']))
    if 'thereof Sugar' in data:
        metrics.sugar_grams.set(extract_number(data['thereof Sugar']))
    if 'Protein' in data:
        metrics.protein_grams.set(extract_number(data['Protein']))
    if 'Alcohol' in data:
        metrics.alcohol_grams.set(extract_number(data['Alcohol']))
    if 'Water' in data:
        metrics.water_liters.set(extract_number(data['Water']))
    if 'Dietary fibre' in data:
        metrics.fiber_grams.set(extract_number(data['Dietary fibre']))
    if 'Cholesterol' in data:
        metrics.cholesterol_mg.set(extract_number(data['Cholesterol']))

    # Vitamins
    if 'Vitamin C' in data:
        metrics.vitamin_c_mg.set(extract_number(data['Vitamin C']))
    if 'Retinol' in data:
        metrics.vitamin_a_mg.set(extract_number(data['Retinol']))
    if 'Vitamin D' in data:
        metrics.vitamin_d_mg.set(extract_number(data['Vitamin D']))
    if 'Vitamin E' in data:
        metrics.vitamin_e_mg.set(extract_number(data['Vitamin E']))
    if 'Thiamine' in data:
        metrics.vitamin_b1_mg.set(extract_number(data['Thiamine']))
    if 'Riboflavin' in data:
        metrics.vitamin_b2_mg.set(extract_number(data['Riboflavin']))
    if 'Vitamin B6' in data:
        metrics.vitamin_b6_mg.set(extract_number(data['Vitamin B6']))
    if 'Vitamin B12' in data:
        metrics.vitamin_b12_mg.set(extract_number(data['Vitamin B12']))

    # Minerals
    if 'Salt' in data:
        metrics.salt_grams.set(extract_number(data['Salt']))
    if 'Iron' in data:
        metrics.iron_mg.set(extract_number(data['Iron']))
    if 'Zinc' in data:
        metrics.zinc_mg.set(extract_number(data['Zinc']))
    if 'Magnesium' in data:
        metrics.magnesium_mg.set(extract_number(data['Magnesium']))
    if 'Manganese' in data:
        metrics.manganese_mg.set(extract_number(data['Manganese']))
    if 'Fluorine' in data:
        metrics.fluoride_mg.set(extract_number(data['Fluorine']))
    if 'Chlorine' in data:
        metrics.chloride_mg.set(extract_number(data['Chlorine']))
    if 'Copper' in data:
        metrics.copper_mg.set(extract_number(data['Copper']))
    if 'Potassium' in data:
        metrics.potassium_mg.set(extract_number(data['Potassium']))
    if 'Calcium' in data:
        metrics.calcium_mg.set(extract_number(data['Calcium']))
    if 'Phosphorus' in data:
        metrics.phosphorus_mg.set(extract_number(data['Phosphorus']))
    if 'Sulphur' in data:
        metrics.sulfur_mg.set(extract_number(data['Sulphur']))
    if 'Iodine' in data:
        metrics.iodine_mg.set(extract_number(data['Iodine']))
