"""
Advanced Report Generation Engine
Generate professional material analysis reports
"""
from datetime import datetime
import pandas as pd

class ReportGenerator:
    """Generate comprehensive material analysis reports"""
    
    @staticmethod
    def generate_material_summary(material: dict, include_specs: bool = True) -> str:
        """Generate material summary report"""
        
        report = f"""
        ╔════════════════════════════════════════════════════════╗
        ║  MATERIAL ANALYSIS REPORT                             ║
        ║  Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}                     ║
        ╚════════════════════════════════════════════════════════╝
        
        MATERIAL IDENTIFICATION
        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        Name:           {material.get('name', 'Unknown')}
        Category:       {material.get('category', 'Unknown')}
        Use Cases:      {material.get('use_cases', 'N/A')}
        
        KEY PROPERTIES
        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        Strength:       {material.get('strength', 0):.0f} MPa
        Weight:         {material.get('weight', 0):.2f} g/cm³
        Cost:           ${material.get('cost', 0):.0f}
        Temperature:    {material.get('temp_limit', 0):.0f}°C
        Corrosion:      {material.get('corrosion', 0)}/10
        Hardness:       {material.get('hardness', 0)}/10
        
        SECONDARY PROPERTIES
        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        """
        
        if 'ductility' in material and pd.notna(material['ductility']):
            report += f"Ductility:      {material['ductility']}/10\n"
        if 'impact_resistance' in material and pd.notna(material['impact_resistance']):
            report += f"Impact:         {material['impact_resistance']}/10\n"
        if 'weldability' in material and pd.notna(material['weldability']):
            report += f"Weldability:    {material['weldability']}/10\n"
        if 'machinability' in material and pd.notna(material['machinability']):
            report += f"Machinability:  {material['machinability']}/10\n"
        
        report += """
        
        PERFORMANCE RATIOS
        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        """
        
        strength = material.get('strength', 1)
        weight = material.get('weight', 1)
        cost = material.get('cost', 1)
        
        strength_to_weight = strength / (weight or 1)
        strength_to_cost = strength / (cost or 1)
        cost_efficiency = cost / (strength or 1)
        
        report += f"""
        Strength/Weight:    {strength_to_weight:.2f}
        Strength/Cost:      {strength_to_cost:.4f}
        Cost/Strength:      {cost_efficiency:.4f}
        
        RATING & SUITABILITY
        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        Overall Score:      {ReportGenerator._calculate_score(material):.1f}/10
        Recommendation:     {ReportGenerator._get_recommendation(material)}
        
        ═══════════════════════════════════════════════════════
        """
        
        return report
    
    @staticmethod
    def generate_comparison_report(materials: list, title: str = "Material Comparison") -> str:
        """Generate comparison report for multiple materials"""
        
        report = f"""
        ╔════════════════════════════════════════════════════════╗
        ║  {title}
        ║  Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        ╚════════════════════════════════════════════════════════╝
        
        MATERIAL COMPARISON TABLE
        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        
        """
        
        # Create comparison table
        df = pd.DataFrame({
            'Material': [m.get('name', 'N/A') for m in materials],
            'Strength': [m.get('strength', 0) for m in materials],
            'Weight': [m.get('weight', 0) for m in materials],
            'Cost': [m.get('cost', 0) for m in materials],
            'Temp': [m.get('temp_limit', 0) for m in materials],
            'Corrosion': [m.get('corrosion', 0) for m in materials],
            'Hardness': [m.get('hardness', 0) for m in materials]
        })
        
        report += df.to_string(index=False)
        
        report += """
        
        COMPARATIVE ANALYSIS
        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        """
        
        # Find best performers
        strongest = max(materials, key=lambda x: x.get('strength', 0))
        lightest = min(materials, key=lambda x: x.get('weight', 0))
        cheapest = min(materials, key=lambda x: x.get('cost', 0))
        most_corrosion_resistant = max(materials, key=lambda x: x.get('corrosion', 0))
        
        report += f"""
        Best Strength:      {strongest.get('name', 'N/A')} ({strongest.get('strength', 0):.0f} MPa)
        Lightest:           {lightest.get('name', 'N/A')} ({lightest.get('weight', 0):.2f} g/cm³)
        Most Affordable:    {cheapest.get('name', 'N/A')} (${cheapest.get('cost', 0):.0f})
        Best Corrosion:     {most_corrosion_resistant.get('name', 'N/A')} ({most_corrosion_resistant.get('corrosion', 0)}/10)
        
        RECOMMENDATION
        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        """
        
        # Calculate overall best
        best_overall = max(materials, key=lambda x: ReportGenerator._calculate_score(x))
        report += f"\nBest Overall Choice: {best_overall.get('name', 'N/A')}\n"
        report += f"Score: {ReportGenerator._calculate_score(best_overall):.1f}/10\n"
        
        report += "\n═══════════════════════════════════════════════════════\n"
        
        return report
    
    @staticmethod
    def generate_requirements_analysis(material: dict, requirements: dict) -> str:
        """Analyze how well material matches requirements"""
        
        report = """
        ╔════════════════════════════════════════════════════════╗
        ║  REQUIREMENT MATCHING ANALYSIS                        ║
        ╚════════════════════════════════════════════════════════╝
        
        REQUIREMENT VERIFICATION
        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        """
        
        checks = []
        
        # Strength
        if 'min_strength' in requirements:
            actual = material.get('strength', 0)
            required = requirements['min_strength']
            passed = actual >= required
            checks.append(f"Strength:     {actual:.0f} MPa {'✓' if passed else '✗'} (Required: {required:.0f})")
        
        # Weight
        if 'max_weight' in requirements:
            actual = material.get('weight', 0)
            required = requirements['max_weight']
            passed = actual <= required
            checks.append(f"Weight:       {actual:.2f} g/cm³ {'✓' if passed else '✗'} (Max: {required:.2f})")
        
        # Cost
        if 'max_cost' in requirements:
            actual = material.get('cost', 0)
            required = requirements['max_cost']
            passed = actual <= required
            checks.append(f"Cost:         ${actual:.0f} {'✓' if passed else '✗'} (Max: ${required:.0f})")
        
        # Temperature
        if 'min_temp' in requirements:
            actual = material.get('temp_limit', 0)
            required = requirements['min_temp']
            passed = actual >= required
            checks.append(f"Temperature:  {actual:.0f}°C {'✓' if passed else '✗'} (Required: {required:.0f}°C)")
        
        # Corrosion
        if 'min_corrosion' in requirements:
            actual = material.get('corrosion', 0)
            required = requirements['min_corrosion']
            passed = actual >= required
            checks.append(f"Corrosion:    {actual:.0f}/10 {'✓' if passed else '✗'} (Required: {required:.0f}/10)")
        
        report += "\n".join(checks)
        
        # Summary
        passed_count = sum(1 for check in checks if '✓' in check)
        total_count = len(checks)
        percentage = (passed_count / total_count * 100) if total_count > 0 else 0
        
        report += f"""
        
        SUMMARY
        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        Requirements Met: {passed_count}/{total_count} ({percentage:.0f}%)
        Match Rating: {ReportGenerator._get_match_rating(percentage)}
        
        ═══════════════════════════════════════════════════════
        """
        
        return report
    
    @staticmethod
    def _calculate_score(material: dict) -> float:
        """Calculate material overall score"""
        strength_norm = min(material.get('strength', 0) / 1000, 1)
        weight_norm = max(1 - (material.get('weight', 10) / 10), 0)
        cost_norm = max(1 - (material.get('cost', 100) / 100), 0)
        corrosion_norm = material.get('corrosion', 5) / 10
        hardness_norm = material.get('hardness', 5) / 10
        
        score = (strength_norm * 0.3 + weight_norm * 0.1 + cost_norm * 0.2 +
                corrosion_norm * 0.2 + hardness_norm * 0.2) * 10
        
        return min(max(score, 0), 10)
    
    @staticmethod
    def _get_recommendation(material: dict) -> str:
        """Get recommendation text"""
        score = ReportGenerator._calculate_score(material)
        
        if score >= 8:
            return "Excellent - Highly Recommended"
        elif score >= 6:
            return "Good - Suitable for most applications"
        elif score >= 4:
            return "Fair - Limited use cases"
        else:
            return "Poor - Not recommended"
    
    @staticmethod
    def _get_match_rating(percentage: float) -> str:
        """Get match rating text"""
        if percentage >= 90:
            return "Excellent Match ✓✓✓"
        elif percentage >= 70:
            return "Good Match ✓✓"
        elif percentage >= 50:
            return "Fair Match ✓"
        else:
            return "Poor Match ✗"

class ExcelExporter:
    """Export materials and reports to Excel"""
    
    @staticmethod
    def export_materials(materials: list, filename: str = "materials.xlsx"):
        """Export materials to Excel"""
        df = pd.DataFrame(materials)
        df.to_excel(filename, index=False)
        return filename
    
    @staticmethod
    def export_comparison(materials: list, filename: str = "comparison.xlsx"):
        """Export comparison to Excel"""
        df = pd.DataFrame({
            'Material': [m.get('name') for m in materials],
            'Category': [m.get('category') for m in materials],
            'Strength (MPa)': [m.get('strength') for m in materials],
            'Weight (g/cm³)': [m.get('weight') for m in materials],
            'Cost ($)': [m.get('cost') for m in materials],
            'Temp Limit (°C)': [m.get('temp_limit') for m in materials],
            'Corrosion (1-10)': [m.get('corrosion') for m in materials],
            'Hardness (1-10)': [m.get('hardness') for m in materials]
        })
        df.to_excel(filename, index=False)
        return filename
