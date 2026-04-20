import pandas as pd
import numpy as np
from datetime import datetime

np.random.seed(42)

materials_data = []

metals_data = [
    ('Steel-Mild', 'Steel', 250, 7.85, 25, 500, 4, 5.5, 8, 7, 8, 'General construction'),
    ('Steel-Carbon', 'Steel', 350, 7.85, 35, 700, 4, 6.5, 8, 6, 9, 'Structural applications'),
    ('Steel-Stainless-304', 'Stainless Steel', 210, 8.0, 45, 425, 9, 5.0, 7, 8, 9, 'Corrosion-resistant'),
    ('Steel-Stainless-316', 'Stainless Steel', 190, 8.0, 55, 400, 9.5, 4.8, 7, 8, 9, 'Marine applications'),
    ('Steel-Tool', 'Steel', 650, 7.75, 85, 1200, 5, 8.0, 6, 4, 8, 'Cutting tools'),
    ('Steel-High-Speed', 'Steel', 900, 9.0, 120, 1500, 4, 9.0, 5, 3, 7, 'Drill bits'),
    ('Steel-Armor', 'Steel', 1400, 8.4, 250, 1100, 3, 9.5, 4, 2, 6, 'Military applications'),
    ('Aluminum-Pure', 'Aluminum', 45, 2.70, 15, 230, 7, 3.0, 3, 9, 9, 'Casting, foil'),
    ('Aluminum-2024', 'Aluminum', 325, 2.78, 55, 200, 4, 6.5, 5, 7, 8, 'Aircraft'),
    ('Aluminum-6061', 'Aluminum', 275, 2.7, 45, 260, 6.5, 6.0, 6, 8, 9, 'General purpose'),
    ('Aluminum-7075', 'Aluminum', 505, 2.81, 75, 250, 3, 8.5, 4, 5, 8, 'High-strength aircraft'),
    ('Aluminum-5083', 'Aluminum', 215, 2.66, 50, 280, 8, 5.5, 7, 8, 8, 'Marine structures'),
    ('Titanium-Grade1', 'Titanium', 345, 4.51, 120, 885, 9.5, 6.0, 7, 8, 8, 'Chemical equipment'),
    ('Titanium-Grade2', 'Titanium', 380, 4.51, 145, 925, 9.5, 6.5, 7, 8, 8, 'Welded structures'),
    ('Titanium-Grade5', 'Titanium', 880, 4.43, 250, 1650, 8, 8.5, 5, 4, 7, 'Aerospace alloy'),
    ('Titanium-Grade7', 'Titanium', 365, 4.54, 150, 950, 10, 6.0, 7, 8, 8, 'Palladium alloy'),
    ('Copper-Pure', 'Copper', 200, 8.96, 25, 200, 9.5, 3.0, 3, 9, 8, 'Electrical wiring'),
    ('Copper-Deoxidized', 'Copper', 210, 8.94, 28, 210, 9, 3.2, 3, 9, 8, 'Tubes and pipe'),
    ('Brass-Yellow', 'Copper', 300, 8.5, 20, 250, 6.5, 4.5, 5, 8, 8, 'Decorative parts'),
    ('Bronze-Phosphor', 'Copper', 400, 8.8, 55, 300, 7.5, 6.0, 6, 7, 7, 'Springs, bearings'),
    ('Nickel-Pure', 'Nickel', 380, 8.88, 85, 1000, 9.5, 6.5, 5, 6, 7, 'Electroplating'),
    ('Nickel-Monel', 'Nickel', 520, 8.8, 150, 1150, 9.5, 7.5, 5, 5, 6, 'Marine corrosion'),
    ('Magnesium-AZ31', 'Magnesium', 260, 1.77, 35, 250, 4, 6.0, 6, 7, 7, 'Lightweight parts'),
    ('Magnesium-AZ91', 'Magnesium', 160, 1.81, 60, 200, 3, 5.5, 5, 6, 7, 'Casting alloy'),
    ('Cobalt-Alloy', 'Specialty', 800, 8.9, 250, 1600, 6, 8.5, 4, 3, 5, 'High-temp applications'),
    ('Molybdenum-Pure', 'Specialty', 625, 10.2, 200, 2660, 2, 8.0, 3, 3, 6, 'High-temperature'),
    ('Tungsten-Pure', 'Specialty', 1510, 19.3, 450, 3400, 1, 9.0, 2, 2, 5, 'Extreme heat'),
    ('Tantalum-Pure', 'Specialty', 180, 16.6, 350, 3300, 9.5, 4.0, 2, 2, 4, 'Chemical vessels'),
    ('Beryllium-Pure', 'Specialty', 380, 1.85, 250, 1300, 3, 6.5, 4, 4, 5, 'Aerospace'),
    ('Zirconium-Pure', 'Specialty', 210, 6.49, 180, 1850, 9, 5.0, 3, 3, 5, 'Nuclear reactors'),
]

for name, category, strength, weight, cost, temp, corr, hard, weld, mach, avail, uses in metals_data:
    materials_data.append({
        'name': name,
        'category': category,
        'strength': strength,
        'weight': weight,
        'cost': cost,
        'temp_limit': temp,
        'corrosion': corr,
        'hardness': hard,
        'weldability': weld,
        'machinability': mach,
        'availability': avail,
        'use_cases': uses,
        'density_factor': weight / 2.5,
        'cost_per_strength': cost / (strength + 1),
        'thermal_index': temp / 500,
        'wear_resistance': hard * 0.8,
        'fatigue_resistance': (strength / 500) * (11 - hard) * 0.5,
        'processing_difficulty': (hard + (1200 - temp) / 200) / 2.5,
        'recyclability': np.random.uniform(5, 9.5),
        'supply_score': np.random.uniform(4, 9.5),
    })

polymer_names = [
    ('Polyethylene-LDPE', 'Low-Density PE'),
    ('Polyethylene-HDPE', 'High-Density PE'),
    ('Polypropylene-PP', 'Polypropylene'),
    ('Polyvinyl-Chloride-PVC', 'PVC'),
    ('Polyethylene-Terephthalate-PET', 'PET'),
    ('Polystyrene-PS', 'Polystyrene'),
    ('Polycarbonate-PC', 'Polycarbonate'),
    ('Polymethyl-Methacrylate-PMMA', 'Acrylic'),
    ('Polyamide-6-PA6', 'Nylon 6'),
    ('Polyamide-66-PA66', 'Nylon 66'),
    ('Polyoxymethylene-POM', 'Acetal'),
    ('Polyurethane-PU', 'Polyurethane'),
    ('Polyester-Unsaturated', 'Unsaturated Polyester'),
    ('Epoxy-Resin', 'Epoxy'),
    ('Phenolic-Resin', 'Phenolic'),
    ('Polyetheretherketone-PEEK', 'PEEK'),
    ('Polyphenylene-Sulfide-PPS', 'PPS'),
    ('Polyetherimide-PEI', 'Polyetherimide'),
    ('Polysulfone-PSU', 'Polysulfone'),
    ('Silicone-Elastomer', 'Silicone'),
]

for name, display_name in polymer_names:
    strength = np.random.uniform(30, 120)
    cost = np.random.uniform(5, 45)
    materials_data.append({
        'name': name,
        'category': 'Polymer',
        'strength': strength,
        'weight': np.random.uniform(0.9, 1.5),
        'cost': cost,
        'temp_limit': np.random.uniform(80, 280),
        'corrosion': np.random.uniform(7, 9.5),
        'hardness': np.random.uniform(3, 7),
        'weldability': np.random.uniform(6, 9),
        'machinability': np.random.uniform(7, 9),
        'availability': np.random.uniform(7, 9.5),
        'use_cases': f'{display_name} applications',
        'density_factor': np.random.uniform(0.3, 0.6),
        'cost_per_strength': cost / (strength + 1),
        'thermal_index': np.random.uniform(0.2, 0.6),
        'wear_resistance': np.random.uniform(3, 6),
        'fatigue_resistance': np.random.uniform(2, 5),
        'processing_difficulty': np.random.uniform(2, 6),
        'recyclability': np.random.uniform(4, 8),
        'supply_score': np.random.uniform(6, 9.5),
    })

ceramic_types = [
    'Alumina', 'Zirconia', 'Silicon Carbide', 'Silicon Nitride', 'Boron Carbide',
    'Advanced Ceramic', 'Thermal Ceramic', 'Structural Ceramic', 'Technical Ceramic',
    'Oxide Ceramic', 'Carbide Ceramic', 'Nitride Ceramic'
]

for ceramic in ceramic_types:
    strength = np.random.uniform(200, 800)
    cost = np.random.uniform(50, 500)
    materials_data.append({
        'name': f'{ceramic}-Grade-{np.random.randint(1, 10)}',
        'category': 'Ceramic',
        'strength': strength,
        'weight': np.random.uniform(2.5, 4.0),
        'cost': cost,
        'temp_limit': np.random.uniform(800, 2500),
        'corrosion': np.random.uniform(9, 10),
        'hardness': np.random.uniform(7, 10),
        'weldability': np.random.uniform(2, 5),
        'machinability': np.random.uniform(2, 5),
        'availability': np.random.uniform(5, 8.5),
        'use_cases': f'High-temperature {ceramic.lower()} applications',
        'density_factor': np.random.uniform(0.8, 1.6),
        'cost_per_strength': cost / (strength + 1),
        'thermal_index': np.random.uniform(1.6, 5.0),
        'wear_resistance': np.random.uniform(8, 10),
        'fatigue_resistance': np.random.uniform(5, 8),
        'processing_difficulty': np.random.uniform(6, 9),
        'recyclability': np.random.uniform(2, 5),
        'supply_score': np.random.uniform(4, 7.5),
    })

composite_types = [
    'Carbon Fiber Reinforced Polymer', 'Glass Fiber Reinforced Polymer',
    'Kevlar Reinforced Composite', 'Metal Matrix Composite',
    'Ceramic Matrix Composite', 'Hybrid Composite', 'Advanced Composite',
    'Structural Composite', 'Lay-up Composite', 'Woven Composite'
]

for composite in composite_types:
    strength = np.random.uniform(400, 1200)
    cost = np.random.uniform(80, 300)
    materials_data.append({
        'name': f'{composite}-Grade-{np.random.randint(1, 8)}',
        'category': 'Composite',
        'strength': strength,
        'weight': np.random.uniform(1.5, 3.0),
        'cost': cost,
        'temp_limit': np.random.uniform(150, 600),
        'corrosion': np.random.uniform(8, 9.5),
        'hardness': np.random.uniform(5, 8),
        'weldability': np.random.uniform(3, 6),
        'machinability': np.random.uniform(6, 8),
        'availability': np.random.uniform(5, 8),
        'use_cases': f'Aerospace {composite.lower()} parts',
        'density_factor': np.random.uniform(0.5, 1.2),
        'cost_per_strength': cost / (strength + 1),
        'thermal_index': np.random.uniform(0.3, 1.2),
        'wear_resistance': np.random.uniform(6, 9),
        'fatigue_resistance': np.random.uniform(7, 9.5),
        'processing_difficulty': np.random.uniform(5, 8),
        'recyclability': np.random.uniform(3, 6),
        'supply_score': np.random.uniform(5, 8.5),
    })

specialty_alloys = [
    'Inconel-625', 'Inconel-718', 'Hastelloy-C276', 'Invar-36',
    'Copper-Beryllium', 'Aluminum-Lithium', 'Titanium-Aluminum',
    'Nickel-Titanium', 'Shape-Memory-Alloy', 'Bulk-Metallic-Glass',
]

for alloy in specialty_alloys:
    strength = np.random.uniform(600, 1400)
    cost = np.random.uniform(150, 600)
    materials_data.append({
        'name': alloy,
        'category': 'Specialty',
        'strength': strength,
        'weight': np.random.uniform(4.5, 9.5),
        'cost': cost,
        'temp_limit': np.random.uniform(1000, 2500),
        'corrosion': np.random.uniform(8, 10),
        'hardness': np.random.uniform(7, 9.5),
        'weldability': np.random.uniform(2, 6),
        'machinability': np.random.uniform(2, 6),
        'availability': np.random.uniform(3, 7),
        'use_cases': f'Extreme performance {alloy.lower()} applications',
        'density_factor': np.random.uniform(1.5, 2.5),
        'cost_per_strength': cost / (strength + 1),
        'thermal_index': np.random.uniform(2.0, 5.0),
        'wear_resistance': np.random.uniform(8, 9.5),
        'fatigue_resistance': np.random.uniform(8, 10),
        'processing_difficulty': np.random.uniform(7, 9.5),
        'recyclability': np.random.uniform(5, 8),
        'supply_score': np.random.uniform(2, 5.5),
    })

for i in range(500):
    category = np.random.choice([
        'Steel', 'Stainless Steel', 'Aluminum', 'Titanium', 'Copper',
        'Nickel', 'Magnesium', 'Specialty', 'Polymer', 'Ceramic', 'Composite'
    ])
    
    strength = np.random.uniform(40, 1500)
    cost = np.random.uniform(5, 500)
    
    materials_data.append({
        'name': f'{category}-Grade-V{i+1}',
        'category': category,
        'strength': strength,
        'weight': np.random.uniform(0.8, 20),
        'cost': cost,
        'temp_limit': np.random.uniform(100, 3400),
        'corrosion': np.random.uniform(1, 10),
        'hardness': np.random.uniform(1, 10),
        'weldability': np.random.uniform(1, 10),
        'machinability': np.random.uniform(1, 10),
        'availability': np.random.uniform(1, 10),
        'use_cases': f'Variant {i+1} applications',
        'density_factor': np.random.uniform(0.1, 5),
        'cost_per_strength': cost / (strength + 1),
        'thermal_index': np.random.uniform(0.1, 6),
        'wear_resistance': np.random.uniform(1, 10),
        'fatigue_resistance': np.random.uniform(1, 10),
        'processing_difficulty': np.random.uniform(1, 10),
        'recyclability': np.random.uniform(1, 10),
        'supply_score': np.random.uniform(1, 10),
    })

df = pd.DataFrame(materials_data)
df = df.drop_duplicates(subset=['name']).reset_index(drop=True)
df = df.sort_values(['category', 'strength'], ascending=[True, False]).reset_index(drop=True)

print(f"✅ Generated {len(df)} materials across {df['category'].nunique()} categories")
print(f"\nCategory breakdown:")
print(df['category'].value_counts())

df.to_csv('materials.csv', index=False)
print(f"\n✅ Saved to materials.csv")
print(f"Database size: {len(df)} materials")
