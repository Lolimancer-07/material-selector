"""
Material Calculators & Physics Simulators
Advanced calculation engine for material properties
"""
import numpy as np
from dataclasses import dataclass

@dataclass
class LoadCondition:
    """Represents a load condition for material"""
    force_newtons: float
    area_mm2: float
    temperature_celsius: float
    corrosive_environment: bool = False

@dataclass
class MaterialPerformance:
    """Results from material property calculations"""
    stress_mpa: float
    safety_factor: float
    deformation_mm: float
    thermal_limit_exceeded: bool
    corrosion_risk: str  # "Low", "Medium", "High"
    cost_per_unit_strength: float

class MaterialCalculator:
    """Advanced material property calculator"""
    
    @staticmethod
    def calculate_stress(force_n: float, area_mm2: float) -> float:
        """Calculate stress in MPa"""
        return (force_n * 1000) / (area_mm2 * 1000)
    
    @staticmethod
    def calculate_safety_factor(material_strength: float, applied_stress: float) -> float:
        """Calculate safety factor"""
        if applied_stress <= 0:
            return float('inf')
        return material_strength / applied_stress
    
    @staticmethod
    def calculate_deformation(force_n: float, area_mm2: float, length_mm: float, 
                             young_modulus: float) -> float:
        """Calculate elastic deformation in mm"""
        stress = MaterialCalculator.calculate_stress(force_n, area_mm2)
        strain = stress / young_modulus if young_modulus > 0 else 0
        return (strain * length_mm) / 1000
    
    @staticmethod
    def calculate_thermal_stress(temp_change: float, cte: float, 
                                modulus: float, area_mm2: float) -> float:
        """Calculate thermal stress (MPa)"""
        thermal_strain = cte * temp_change
        thermal_stress = thermal_strain * modulus
        return abs(thermal_stress)
    
    @staticmethod
    def analyze_material(material_data: dict, load_condition: LoadCondition) -> MaterialPerformance:
        """Comprehensive material analysis"""
        
        # Stress calculation
        applied_stress = MaterialCalculator.calculate_stress(
            load_condition.force_newtons,
            load_condition.area_mm2
        )
        
        # Safety factor
        material_strength = float(material_data.get('strength', 100))
        safety_factor = MaterialCalculator.calculate_safety_factor(
            material_strength,
            applied_stress
        )
        
        # Deformation (approximate)
        young_modulus = material_strength / 0.003  # Rough estimate
        deformation = MaterialCalculator.calculate_deformation(
            load_condition.force_newtons,
            load_condition.area_mm2,
            100,  # Assume 100mm length
            young_modulus
        )
        
        # Temperature check
        temp_limit = float(material_data.get('temp_limit', 500))
        thermal_exceeded = load_condition.temperature_celsius > temp_limit
        
        # Corrosion risk
        corrosion_resistance = float(material_data.get('corrosion', 5))
        if load_condition.corrosive_environment:
            if corrosion_resistance >= 8:
                corrosion_risk = "Low"
            elif corrosion_resistance >= 6:
                corrosion_risk = "Medium"
            else:
                corrosion_risk = "High"
        else:
            corrosion_risk = "Low"
        
        # Cost per unit strength
        cost = float(material_data.get('cost', 50))
        cost_per_strength = cost / material_strength if material_strength > 0 else 0
        
        return MaterialPerformance(
            stress_mpa=applied_stress,
            safety_factor=safety_factor,
            deformation_mm=deformation,
            thermal_limit_exceeded=thermal_exceeded,
            corrosion_risk=corrosion_risk,
            cost_per_unit_strength=cost_per_strength
        )

class ThermalSimulator:
    """Thermal analysis simulator"""
    
    @staticmethod
    def simulate_temperature_distribution(initial_temp: float, ambient_temp: float,
                                         thermal_conductivity: float,
                                         time_seconds: float) -> dict:
        """Simulate temperature change over time"""
        time_steps = int(time_seconds / 10)
        times = np.linspace(0, time_seconds, time_steps)
        
        # Exponential cooling/heating model
        temp_diff = ambient_temp - initial_temp
        temps = ambient_temp + temp_diff * np.exp(-thermal_conductivity * times / 100)
        
        return {
            'times': times,
            'temperatures': temps,
            'final_temperature': temps[-1],
            'equilibrium_time': times[np.argmin(np.abs(temps - ambient_temp))]
        }
    
    @staticmethod
    def calculate_thermal_expansion(initial_length: float, temp_change: float,
                                   cte: float) -> float:
        """Calculate thermal expansion"""
        return initial_length * cte * temp_change

class CostOptimizer:
    """Cost optimization engine"""
    
    @staticmethod
    def cost_per_property(material: dict, property_name: str = 'strength') -> float:
        """Calculate cost per unit of property"""
        cost = float(material.get('cost', 1))
        prop_value = float(material.get(property_name, 1))
        return cost / prop_value if prop_value > 0 else float('inf')
    
    @staticmethod
    def total_material_cost(material: dict, mass_kg: float) -> float:
        """Calculate total cost for mass of material"""
        cost_per_unit = float(material.get('cost', 0))  # Cost per kg (assumed)
        density = float(material.get('weight', 1))  # Proxy for density
        return cost_per_unit * mass_kg
    
    @staticmethod
    def cost_benefit_analysis(materials: list, requirements: dict) -> list:
        """Rank materials by cost-benefit"""
        scores = []
        
        for material in materials:
            strength_score = material.get('strength', 1) / (requirements.get('min_strength', 1) or 1)
            cost_score = 1 / (material.get('cost', 1) + 0.1)
            corrosion_score = material.get('corrosion', 5) / 10
            temp_score = material.get('temp_limit', 500) / (requirements.get('min_temp', 500) or 1)
            
            # Weighted score
            total_score = (strength_score * 0.3 + cost_score * 0.3 + 
                          corrosion_score * 0.2 + temp_score * 0.2)
            
            scores.append({
                'material': material.get('name', 'Unknown'),
                'score': total_score,
                'cost_per_strength': CostOptimizer.cost_per_property(material, 'strength'),
                'total_benefit': total_score
            })
        
        return sorted(scores, key=lambda x: x['score'], reverse=True)

class DurabilityAnalyzer:
    """Material durability & lifetime analysis"""
    
    @staticmethod
    def estimate_service_life(material: dict, load_condition: LoadCondition,
                             annual_stress_cycles: float = 1e6) -> dict:
        """Estimate material service life using Basquin equation"""
        
        strength = material.get('strength', 100)
        corrosion = material.get('corrosion', 5)
        
        # Fatigue limit approximation
        fatigue_limit = strength * 0.4
        
        # Stress amplitude from load
        applied_stress = (load_condition.force_newtons / load_condition.area_mm2) * 1000
        
        # Simplified fatigue calculation
        if applied_stress > fatigue_limit:
            life_cycles = (1e7) * ((fatigue_limit / applied_stress) ** 3)
        else:
            life_cycles = float('inf')
        
        years = life_cycles / annual_stress_cycles
        
        # Corrosion impact
        if load_condition.corrosive_environment and corrosion < 7:
            years *= 0.5  # Reduce life by 50% for corrosive environment
        
        return {
            'estimated_cycles': int(life_cycles),
            'estimated_years': years,
            'fatigue_limit_mpa': fatigue_limit,
            'applied_stress_mpa': applied_stress,
            'safety_margin': (fatigue_limit - applied_stress) / applied_stress if applied_stress > 0 else 0
        }
    
    @staticmethod
    def calculate_degradation_rate(material: dict, environment_severity: str) -> float:
        """Calculate annual material degradation rate"""
        
        base_rate = 0.02  # 2% per year base
        corrosion_factor = (10 - material.get('corrosion', 5)) / 10
        
        severity_multiplier = {
            'mild': 0.5,
            'moderate': 1.0,
            'severe': 2.0,
            'extreme': 4.0
        }
        
        multiplier = severity_multiplier.get(environment_severity, 1.0)
        
        return base_rate * corrosion_factor * multiplier

# Functions for quick access
def quick_safety_check(material: dict, force_n: float, area_mm2: float) -> bool:
    """Quick safety check - returns True if safe (safety factor > 1.5)"""
    stress = MaterialCalculator.calculate_stress(force_n, area_mm2)
    sf = MaterialCalculator.calculate_safety_factor(material.get('strength', 100), stress)
    return sf >= 1.5
