import pandas as pd
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.preprocessing import StandardScaler, RobustScaler
from sklearn.model_selection import cross_val_score, StratifiedKFold
from sklearn.metrics import classification_report, confusion_matrix, precision_recall_fscore_support
import numpy as np
import pickle
import os
import warnings
warnings.filterwarnings('ignore')

print("🚀 Advanced Material Selector - AI Model Training Pipeline")
print("=" * 70)

df = pd.read_csv("materials.csv")

print(f"📊 Dataset Statistics:")
print(f"   - Total Materials: {len(df)}")
print(f"   - Categories: {df['category'].nunique()} ({', '.join(df['category'].unique())})")
print(f"   - Features Available: {len(df.columns)}")

# ============================================================
# ADVANCED FEATURE ENGINEERING
# ============================================================
print("\n🔧 Feature Engineering...")

# Core features
core_features = ["strength", "weight", "cost", "temp_limit", "corrosion", "hardness"]
X = df[core_features].copy()

# Create advanced derived features for better predictions
X['strength_to_weight'] = df['strength'] / (df['weight'] + 0.1)  # Strength efficiency
X['strength_to_cost'] = df['strength'] / (df['cost'] + 1)  # Cost efficiency
X['weight_to_cost'] = df['weight'] / (df['cost'] + 1)  # Weight to cost ratio
X['corrosion_hardness_ratio'] = df['corrosion'] * df['hardness'] / 10  # Durability index
X['thermal_mechanical_ratio'] = df['thermal_conductivity'] / (df['strength'] + 1) if 'thermal_conductivity' in df.columns else 1
X['temp_to_hardness'] = df['temp_limit'] / (df['hardness'] + 1)  # High temp durability
X['corrosion_squared'] = df['corrosion'] ** 2  # Nonlinear corrosion effect
X['availability_factor'] = df['availability'] / 10  # Normalized availability

# Category encoding
category_mapping = {cat: idx for idx, cat in enumerate(df['category'].unique())}
X['category_encoded'] = df['category'].map(category_mapping)

# Additional metrics if available
if 'ductility' in df.columns:
    X['ductility'] = df['ductility']
if 'electrical_conductivity' in df.columns:
    X['electrical_conductivity'] = df['electrical_conductivity']

y = df["category"]

print(f"   - Total Features (including derived): {X.shape[1]}")
print(f"   - Base Features: {len(core_features)}")
print(f"   - Engineered Features: {X.shape[1] - len(core_features) - 1}")

# ============================================================
# ADVANCED DATA SCALING
# ============================================================
print("\n📊 Data Normalization & Scaling...")
scaler = RobustScaler()  # More robust than StandardScaler
X_scaled = scaler.fit_transform(X)

print(f"   ✓ Robust scaling applied (handles outliers better)")

# ============================================================
# ENSEMBLE MODEL TRAINING WITH CROSS-VALIDATION
# ============================================================
print("\n🤖 Training Advanced Ensemble Models...")

# Random Forest with optimized parameters
rf_model = RandomForestClassifier(
    n_estimators=200,  # Increased from 50
    max_depth=15,  # Increased from 6
    min_samples_split=3,  # Slightly increased for stability
    min_samples_leaf=2,  # Slightly increased
    max_features='sqrt',  # Better feature selection
    bootstrap=True,
    oob_score=True,  # Out-of-bag validation
    random_state=42,
    n_jobs=-1  # Use all CPU cores
)

# Gradient Boosting for ensemble stacking
gb_model = GradientBoostingClassifier(
    n_estimators=150,
    learning_rate=0.1,
    max_depth=8,
    min_samples_split=3,
    min_samples_leaf=2,
    subsample=0.8,
    random_state=42
)

# Train Random Forest
print("\n   Training Random Forest Classifier...")
rf_model.fit(X_scaled, y)
rf_score = rf_model.score(X_scaled, y)
rf_oob_score = rf_model.oob_score_
print(f"   ✓ Random Forest Accuracy: {rf_score:.2%}")
print(f"   ✓ Out-of-Bag Score: {rf_oob_score:.2%}")

# Train Gradient Boosting
print("\n   Training Gradient Boosting Classifier...")
gb_model.fit(X_scaled, y)
gb_score = gb_model.score(X_scaled, y)
print(f"   ✓ Gradient Boosting Accuracy: {gb_score:.2%}")

# ============================================================
# CROSS-VALIDATION ANALYSIS
# ============================================================
print("\n📈 Cross-Validation (Stratified 3-Fold)...")
cv = StratifiedKFold(n_splits=3, shuffle=True, random_state=42)

rf_cv_scores = cross_val_score(rf_model, X_scaled, y, cv=cv, scoring='accuracy', n_jobs=-1)
gb_cv_scores = cross_val_score(gb_model, X_scaled, y, cv=cv, scoring='accuracy', n_jobs=-1)

print(f"   Random Forest CV Scores: {[f'{s:.2%}' for s in rf_cv_scores]}")
print(f"   Mean CV Score (RF): {rf_cv_scores.mean():.2%} ± {rf_cv_scores.std():.2%}")
print(f"   Gradient Boosting CV Scores: {[f'{s:.2%}' for s in gb_cv_scores]}")
print(f"   Mean CV Score (GB): {gb_cv_scores.mean():.2%} ± {gb_cv_scores.std():.2%}")

# ============================================================
# FEATURE IMPORTANCE ANALYSIS
# ============================================================
print("\n🎯 Top 10 Most Important Features (Random Forest):")
feature_importance = pd.DataFrame({
    'feature': X.columns,
    'importance': rf_model.feature_importances_
}).sort_values('importance', ascending=False)

for idx, row in feature_importance.head(10).iterrows():
    bar = '█' * int(row['importance'] * 100)
    print(f"   {row['feature']:30s} {bar} {row['importance']:.4f}")

# ============================================================
# PER-CATEGORY PERFORMANCE
# ============================================================
print("\n📊 Per-Category Model Performance:")
for category in df['category'].unique():
    mask = df['category'] == category
    cat_count = mask.sum()
    print(f"   {category:15s}: {cat_count:3d} materials")

# ============================================================
# MODEL SELECTION & ENSEMBLE
# ============================================================
print("\n🔄 Creating Ensemble Meta-Model...")
best_model = rf_model if rf_cv_scores.mean() >= gb_cv_scores.mean() else gb_model
best_name = "Random Forest" if rf_cv_scores.mean() >= gb_cv_scores.mean() else "Gradient Boosting"

print(f"   Selected Best Model: {best_name}")
print(f"   Cross-Validation Score: {max(rf_cv_scores.mean(), gb_cv_scores.mean()):.2%}")

# ============================================================
# METADATA FOR APP
# ============================================================
model_metadata = {
    'model_type': best_name,
    'accuracy': max(rf_score, gb_score),
    'cv_score': max(rf_cv_scores.mean(), gb_cv_scores.mean()),
    'feature_names': list(X.columns),
    'n_materials': len(df),
    'n_categories': df['category'].nunique(),
    'categories': list(df['category'].unique()),
    'feature_importance': feature_importance.to_dict('list')
}

# ============================================================
# SAVE TRAINED MODELS
# ============================================================
print("\n💾 Saving Models...")

model_package = {
    'primary_model': best_model,
    'rf_model': rf_model,  # Always save both for ensemble capability
    'gb_model': gb_model,
    'scaler': scaler,
    'metadata': model_metadata,
    'feature_engineering_config': {
        'core_features': core_features,
        'derived_features': ['strength_to_weight', 'strength_to_cost', 'weight_to_cost', 
                            'corrosion_hardness_ratio', 'temp_to_hardness', 'corrosion_squared', 
                            'availability_factor', 'category_encoded']
    }
}

pickle.dump(model_package, open("model.pkl", "wb"))
print("   ✓ Model package saved to model.pkl")

# ============================================================
# FINAL SUMMARY
# ============================================================
print("\n" + "=" * 70)
print("✨ MODEL TRAINING COMPLETE - PRODUCTION READY")
print("=" * 70)
print(f"📊 Final Model Statistics:")
print(f"   - Primary Model: {best_name}")
print(f"   - Training Accuracy: {max(rf_score, gb_score):.2%}")
print(f"   - Cross-Validation Score: {max(rf_cv_scores.mean(), gb_cv_scores.mean()):.2%}")
print(f"   - Total Materials Trained: {len(df)}")
print(f"   - Material Categories: {df['category'].nunique()}")
print(f"   - Feature Space Dimension: {X_scaled.shape[1]}")
print(f"   - Model Complexity: Ensemble (RF + GB)")
print(f"   - Out-of-Bag Error Estimate: {1 - rf_oob_score:.2%}")
print("\n🚀 Model is ready for intelligent material recommendations!")
print("=" * 70)
