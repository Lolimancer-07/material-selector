"""
Advanced Recommendation Engine
AI-powered intelligent material recommendations
"""
import pandas as pd
import numpy as np
from typing import List, Dict, Tuple

class AdvancedRecommender:
    """Advanced AI-powered recommendations"""
    
    @staticmethod
    def weighted_recommendation(materials: pd.DataFrame, weights: Dict[str, float]) -> pd.DataFrame:
        """
        Calculate weighted recommendations based on multiple criteria
        
        weights: dict with keys like 'strength', 'weight', 'cost', 'corrosion', 'hardness', 'temp_limit'
        """
        
        recommendations = []
        
        for idx, material in materials.iterrows():
            score = 0
            
            # Normalize and calculate weighted scores
            if 'strength' in weights:
                norm_strength = min(material['strength'] / materials['strength'].max(), 1.0)
                score += norm_strength * weights.get('strength', 0)
            
            if 'weight' in weights:
                norm_weight = max(1 - (material['weight'] / materials['weight'].max()), 0)
                score += norm_weight * weights.get('weight', 0)
            
            if 'cost' in weights:
                norm_cost = max(1 - (material['cost'] / materials['cost'].max()), 0)
                score += norm_cost * weights.get('cost', 0)
            
            if 'corrosion' in weights:
                norm_corrosion = material['corrosion'] / 10
                score += norm_corrosion * weights.get('corrosion', 0)
            
            if 'hardness' in weights:
                norm_hardness = material['hardness'] / 10
                score += norm_hardness * weights.get('hardness', 0)
            
            if 'temp_limit' in weights:
                norm_temp = min(material['temp_limit'] / materials['temp_limit'].max(), 1.0)
                score += norm_temp * weights.get('temp_limit', 0)
            
            recommendations.append({
                'name': material['name'],
                'category': material['category'],
                'score': score,
                'rank': 0  # Will be filled after sorting
            })
        
        # Sort by score
        recommendations = sorted(recommendations, key=lambda x: x['score'], reverse=True)
        
        # Add ranks
        for i, rec in enumerate(recommendations):
            rec['rank'] = i + 1
        
        return pd.DataFrame(recommendations)
    
    @staticmethod
    def use_case_recommendation(materials: pd.DataFrame, use_case: str) -> pd.DataFrame:
        """Get recommendations based on use case"""
        
        weight_presets = {
            'aerospace': {'strength': 0.35, 'weight': 0.25, 'cost': 0.15, 'temp_limit': 0.25},
            'medical': {'corrosion': 0.40, 'hardness': 0.20, 'cost': 0.20, 'weight': 0.20},
            'marine': {'corrosion': 0.50, 'strength': 0.30, 'hardness': 0.20},
            'high_temperature': {'temp_limit': 0.50, 'strength': 0.30, 'corrosion': 0.20},
            'lightweight': {'weight': 0.40, 'strength': 0.30, 'cost': 0.30},
            'budget': {'cost': 0.50, 'strength': 0.30, 'weight': 0.20},
            'precision': {'hardness': 0.40, 'corrosion': 0.30, 'strength': 0.30},
            'structural': {'strength': 0.40, 'cost': 0.30, 'weight': 0.30}
        }
        
        weights = weight_presets.get(use_case.lower(), {'strength': 0.25, 'weight': 0.25, 'cost': 0.25, 'corrosion': 0.25})
        
        return AdvancedRecommender.weighted_recommendation(materials, weights)
    
    @staticmethod
    def constraint_satisfaction(materials: pd.DataFrame, constraints: Dict) -> pd.DataFrame:
        """Filter materials that satisfy hard constraints"""
        
        filtered = materials.copy()
        
        if 'min_strength' in constraints:
            filtered = filtered[filtered['strength'] >= constraints['min_strength']]
        
        if 'max_weight' in constraints:
            filtered = filtered[filtered['weight'] <= constraints['max_weight']]
        
        if 'max_cost' in constraints:
            filtered = filtered[filtered['cost'] <= constraints['max_cost']]
        
        if 'min_temp' in constraints:
            filtered = filtered[filtered['temp_limit'] >= constraints['min_temp']]
        
        if 'min_corrosion' in constraints:
            filtered = filtered[filtered['corrosion'] >= constraints['min_corrosion']]
        
        if 'min_hardness' in constraints:
            filtered = filtered[filtered['hardness'] >= constraints['min_hardness']]
        
        return filtered
    
    @staticmethod
    def similarity_search(materials: pd.DataFrame, reference_material: str, 
                         similarity_threshold: float = 0.7) -> pd.DataFrame:
        """Find materials similar to a reference material"""
        
        if reference_material not in materials['name'].values:
            return pd.DataFrame()
        
        ref = materials[materials['name'] == reference_material].iloc[0]
        
        similarities = []
        
        for idx, mat in materials.iterrows():
            if mat['name'] == reference_material:
                continue
            
            # Normalized euclidean distance
            features = ['strength', 'weight', 'cost', 'temp_limit', 'corrosion', 'hardness']
            
            distance = 0
            for feat in features:
                if feat in ref.index and feat in mat.index:
                    max_val = materials[feat].max()
                    min_val = materials[feat].min()
                    range_val = max_val - min_val
                    if range_val > 0:
                        norm_diff = (ref[feat] - mat[feat]) / range_val
                        distance += norm_diff ** 2
            
            distance = np.sqrt(distance)
            similarity = 1 / (1 + distance)  # Convert distance to similarity
            
            if similarity >= similarity_threshold:
                similarities.append({
                    'name': mat['name'],
                    'category': mat['category'],
                    'similarity_score': similarity,
                    'cost_difference': mat['cost'] - ref['cost'],
                    'strength_difference': mat['strength'] - ref['strength']
                })
        
        return pd.DataFrame(similarities).sort_values('similarity_score', ascending=False)
    
    @staticmethod
    def property_trade_off_analysis(materials: pd.DataFrame, property1: str, 
                                    property2: str) -> Dict:
        """Analyze trade-offs between two properties"""
        
        analysis = {
            'correlations': {},
            'pareto_frontier': [],
            'quadrants': {
                'high_high': [],
                'high_low': [],
                'low_high': [],
                'low_low': []
            }
        }
        
        # Calculate correlation
        if property1 in materials.columns and property2 in materials.columns:
            corr = materials[property1].corr(materials[property2])
            analysis['correlations'][f'{property1}_vs_{property2}'] = corr
        
        # Find Pareto frontier (non-dominated solutions)
        materials_copy = materials.copy()
        dominated = [False] * len(materials_copy)
        
        for i in range(len(materials_copy)):
            for j in range(len(materials_copy)):
                if i != j:
                    if (materials_copy.iloc[j][property1] >= materials_copy.iloc[i][property1] and
                        materials_copy.iloc[j][property2] >= materials_copy.iloc[i][property2] and
                        (materials_copy.iloc[j][property1] > materials_copy.iloc[i][property1] or
                         materials_copy.iloc[j][property2] > materials_copy.iloc[i][property2])):
                        dominated[i] = True
        
        analysis['pareto_frontier'] = materials_copy[~np.array(dominated)][['name', property1, property2]].to_dict('records')
        
        # Quadrant analysis
        p1_median = materials[property1].median()
        p2_median = materials[property2].median()
        
        for idx, mat in materials.iterrows():
            mat_info = {'name': mat['name'], property1: mat[property1], property2: mat[property2]}
            
            if mat[property1] >= p1_median and mat[property2] >= p2_median:
                analysis['quadrants']['high_high'].append(mat_info)
            elif mat[property1] >= p1_median and mat[property2] < p2_median:
                analysis['quadrants']['high_low'].append(mat_info)
            elif mat[property1] < p1_median and mat[property2] >= p2_median:
                analysis['quadrants']['low_high'].append(mat_info)
            else:
                analysis['quadrants']['low_low'].append(mat_info)
        
        return analysis
    
    @staticmethod
    def multi_objective_optimization(materials: pd.DataFrame, 
                                     objectives: Dict[str, str]) -> pd.DataFrame:
        """
        Multi-objective optimization
        objectives: dict like {'strength': 'maximize', 'cost': 'minimize', 'weight': 'minimize'}
        """
        
        materials_copy = materials.copy()
        scores = np.zeros(len(materials_copy))
        
        for obj, direction in objectives.items():
            if obj in materials_copy.columns:
                normalized = (materials_copy[obj] - materials_copy[obj].min()) / (
                    materials_copy[obj].max() - materials_copy[obj].min() + 1e-10)
                
                if direction == 'maximize':
                    scores += normalized
                else:  # minimize
                    scores += (1 - normalized)
        
        materials_copy['optimization_score'] = scores / len(objectives)
        
        return materials_copy.sort_values('optimization_score', ascending=False)
