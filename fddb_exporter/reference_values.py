from prometheus_client import Gauge

# D-A-CH reference values (German Nutrition Society)
# Adult average (19-65 years, male/female average where applicable)

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


def set_reference_values():
    """
    Set reference values based on D-A-CH guidelines (adult average).
    Source: German Nutrition Society (DGE), Austrian Nutrition Society (ÖGE),
    Swiss Society for Nutrition (SGE/SSN)
    """
    # Vitamins (mg/day)
    vitamin_c_ref.set(100)  # 95-110 mg
    vitamin_a_ref.set(0.85)  # 0.8-1.0 mg (retinol equivalent)
    vitamin_d_ref.set(0.020)  # 20 µg = 0.020 mg
    vitamin_e_ref.set(12)  # 11-15 mg (tocopherol equivalent)
    vitamin_b1_ref.set(1.2)  # 1.0-1.3 mg
    vitamin_b2_ref.set(1.3)  # 1.2-1.4 mg
    vitamin_b6_ref.set(1.4)  # 1.2-1.6 mg
    vitamin_b12_ref.set(0.004)  # 4.0 µg = 0.004 mg

    # Minerals (mg/day)
    iron_ref.set(12.5)  # 10-15 mg (average, varies by gender)
    zinc_ref.set(9)  # 7-11 mg
    magnesium_ref.set(350)  # 300-400 mg
    calcium_ref.set(1000)  # 1000 mg
    potassium_ref.set(4000)  # 4000 mg
    phosphorus_ref.set(700)  # 700 mg
    iodine_ref.set(0.200)  # 200 µg = 0.200 mg
    selenium_ref.set(0.060)  # 60 µg = 0.060 mg
