from prometheus_client import Gauge

# Prometheus Gauges centralized here to avoid duplicate registration
energy_kj = Gauge('fddb_energy_kj', 'Energy in kilojoules')
energy_kcal = Gauge('fddb_energy_kcal', 'Energy in kilocalories')
fat_grams = Gauge('fddb_fat_grams', 'Fat in grams')
carbohydrates_grams = Gauge('fddb_carbohydrates_grams', 'Carbohydrates in grams')
sugar_grams = Gauge('fddb_sugar_grams', 'Sugar in grams')
protein_grams = Gauge('fddb_protein_grams', 'Protein in grams')
alcohol_grams = Gauge('fddb_alcohol_grams', 'Alcohol in grams')
water_liters = Gauge('fddb_water_liters', 'Water in liters')
fiber_grams = Gauge('fddb_fiber_grams', 'Fiber in grams')
cholesterol_mg = Gauge('fddb_cholesterol_mg', 'Cholesterol in milligrams')

# Vitamins
vitamin_c_mg = Gauge('fddb_vitamin_c_mg', 'Vitamin C in milligrams')
vitamin_a_mg = Gauge('fddb_vitamin_a_mg', 'Vitamin A in milligrams')
vitamin_d_mg = Gauge('fddb_vitamin_d_mg', 'Vitamin D in milligrams')
vitamin_e_mg = Gauge('fddb_vitamin_e_mg', 'Vitamin E in milligrams')
vitamin_b1_mg = Gauge('fddb_vitamin_b1_mg', 'Vitamin B1 in milligrams')
vitamin_b2_mg = Gauge('fddb_vitamin_b2_mg', 'Vitamin B2 in milligrams')
vitamin_b6_mg = Gauge('fddb_vitamin_b6_mg', 'Vitamin B6 in milligrams')
vitamin_b12_mg = Gauge('fddb_vitamin_b12_mg', 'Vitamin B12 in milligrams')

# Minerals
salt_grams = Gauge('fddb_salt_grams', 'Salt in grams')
iron_mg = Gauge('fddb_iron_mg', 'Iron in milligrams')
zinc_mg = Gauge('fddb_zinc_mg', 'Zinc in milligrams')
magnesium_mg = Gauge('fddb_magnesium_mg', 'Magnesium in milligrams')
manganese_mg = Gauge('fddb_manganese_mg', 'Manganese in milligrams')
fluoride_mg = Gauge('fddb_fluoride_mg', 'Fluoride in milligrams')
chloride_mg = Gauge('fddb_chloride_mg', 'Chloride in milligrams')
copper_mg = Gauge('fddb_copper_mg', 'Copper in milligrams')
potassium_mg = Gauge('fddb_potassium_mg', 'Potassium in milligrams')
calcium_mg = Gauge('fddb_calcium_mg', 'Calcium in milligrams')
phosphorus_mg = Gauge('fddb_phosphorus_mg', 'Phosphorus in milligrams')
sulfur_mg = Gauge('fddb_sulfur_mg', 'Sulfur in milligrams')
iodine_mg = Gauge('fddb_iodine_mg', 'Iodine in milligrams')
