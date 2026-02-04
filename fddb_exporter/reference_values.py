from prometheus_client import Gauge

# D-A-CH reference values (German Nutrition Society)
# Adult average (19-65 years, male/female average where applicable)

# Macronutrient reference values
fat_ref = Gauge('fddb_fat_reference_grams', 'Reference value for Fat in grams')
carbohydrates_ref = Gauge('fddb_carbohydrates_reference_grams', 'Reference value for Carbohydrates in grams')
sugar_ref = Gauge('fddb_sugar_reference_grams', 'Reference value for Sugar in grams')
protein_ref = Gauge('fddb_protein_reference_grams', 'Reference value for Protein in grams')
fiber_ref = Gauge('fddb_fiber_reference_grams', 'Reference value for Fiber in grams')
water_ref = Gauge('fddb_water_reference_liters', 'Reference value for Water in liters')
cholesterol_ref = Gauge('fddb_cholesterol_reference_mg', 'Reference value for Cholesterol in mg')
alcohol_ref = Gauge('fddb_alcohol_reference_grams', 'Reference value for Alcohol in grams (max)')

# Vitamin reference values (RDA - Recommended Daily Allowance)
vitamin_c_ref = Gauge('fddb_vitamin_c_reference_mg', 'Reference value for Vitamin C in mg')
vitamin_a_ref = Gauge('fddb_vitamin_a_reference_mg', 'Reference value for Vitamin A in mg')
vitamin_d_ref = Gauge('fddb_vitamin_d_reference_mg', 'Reference value for Vitamin D in mg')
vitamin_e_ref = Gauge('fddb_vitamin_e_reference_mg', 'Reference value for Vitamin E in mg')
vitamin_b1_ref = Gauge('fddb_vitamin_b1_reference_mg', 'Reference value for Vitamin B1 in mg')
vitamin_b2_ref = Gauge('fddb_vitamin_b2_reference_mg', 'Reference value for Vitamin B2 in mg')
vitamin_b6_ref = Gauge('fddb_vitamin_b6_reference_mg', 'Reference value for Vitamin B6 in mg')
vitamin_b12_ref = Gauge('fddb_vitamin_b12_reference_mg', 'Reference value for Vitamin B12 in mg')

# Mineral reference values (RDA)
iron_ref = Gauge('fddb_iron_reference_mg', 'Reference value for Iron in mg')
zinc_ref = Gauge('fddb_zinc_reference_mg', 'Reference value for Zinc in mg')
magnesium_ref = Gauge('fddb_magnesium_reference_mg', 'Reference value for Magnesium in mg')
calcium_ref = Gauge('fddb_calcium_reference_mg', 'Reference value for Calcium in mg')
potassium_ref = Gauge('fddb_potassium_reference_mg', 'Reference value for Potassium in mg')
phosphorus_ref = Gauge('fddb_phosphorus_reference_mg', 'Reference value for Phosphorus in mg')
iodine_ref = Gauge('fddb_iodine_reference_mg', 'Reference value for Iodine in mg')
selenium_ref = Gauge('fddb_selenium_reference_mg', 'Reference value for Selenium in mg')


def set_reference_values(daily_calories=2400):
    """
    Set reference values based on D-A-CH guidelines (adult average).
    Source: German Nutrition Society (DGE), Austrian Nutrition Society (ÖGE),
    Swiss Society for Nutrition (SGE/SSN)

    Args:
        daily_calories: Daily calorie target (default: 2400 kcal)

    Note: Values scale with energy needs (calories), using 2400 kcal as baseline.
    Reference baseline values are from D-A-CH for adults (19-65 years).
    """
    # Base reference at 2400 kcal
    BASE_CALORIES = 2400
    scale_factor = daily_calories / BASE_CALORIES

    # Macronutrients (calculated based on daily_calories)
    fat_ref.set(round(daily_calories * 0.30 / 9, 1))  # 30% of energy, 9 kcal per g fat
    carbohydrates_ref.set(round(daily_calories * 0.50 / 4, 1))  # 50% of energy, 4 kcal per g carbs
    sugar_ref.set(round(daily_calories * 0.10 / 4, 1))  # max 10% of energy
    protein_ref.set(round(57 * scale_factor, 1))  # 0.8g per kg bodyweight, scales with energy
    fiber_ref.set(round(30 * scale_factor, 1))  # scales with energy intake
    water_ref.set(round(2.0 * scale_factor, 1))  # scales with energy
    cholesterol_ref.set(300)  # max 300mg per day, independent of calories
    alcohol_ref.set(20)  # max 20g per day for men, independent of calories

    # Vitamins (mg/day) - scale with energy needs
    vitamin_c_ref.set(round(100 * scale_factor, 3))  # 95-110 mg at 2400 kcal
    vitamin_a_ref.set(round(0.85 * scale_factor, 3))  # 0.8-1.0 mg (retinol equivalent)
    vitamin_d_ref.set(round(0.020 * scale_factor, 4))  # 20 µg = 0.020 mg
    vitamin_e_ref.set(round(12 * scale_factor, 3))  # 11-15 mg (tocopherol equivalent)
    vitamin_b1_ref.set(round(1.2 * scale_factor, 3))  # 1.0-1.3 mg
    vitamin_b2_ref.set(round(1.3 * scale_factor, 3))  # 1.2-1.4 mg
    vitamin_b6_ref.set(round(1.4 * scale_factor, 3))  # 1.2-1.6 mg
    vitamin_b12_ref.set(round(0.004 * scale_factor, 5))  # 4.0 µg = 0.004 mg

    # Minerals (mg/day) - scale with energy needs
    iron_ref.set(round(12.5 * scale_factor, 3))  # 10-15 mg (average, varies by gender)
    zinc_ref.set(round(9 * scale_factor, 3))  # 7-11 mg
    magnesium_ref.set(round(350 * scale_factor, 1))  # 300-400 mg
    calcium_ref.set(round(1000 * scale_factor, 1))  # 1000 mg
    potassium_ref.set(round(4000 * scale_factor, 1))  # 4000 mg
    phosphorus_ref.set(round(700 * scale_factor, 1))  # 700 mg
    iodine_ref.set(round(0.200 * scale_factor, 4))  # 200 µg = 0.200 mg
    selenium_ref.set(round(0.060 * scale_factor, 4))  # 60 µg = 0.060 mg
