import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import pickle
import os

df = pd.read_csv("materials.csv")

# Use only the core numeric features for ML model
X = df[["strength","weight","cost","temp_limit","corrosion","hardness"]]
y = df["name"]

# Add feature scaling to handle different ranges
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Train model with regularization to prevent overfitting
model = RandomForestClassifier(
    n_estimators=50, 
    random_state=42, 
    max_depth=6,
    min_samples_split=2,
    min_samples_leaf=1
)
model.fit(X_scaled, y)

# Calculate training accuracy
train_score = model.score(X_scaled, y)

print(f"✨ Material Selector Model Training Complete!")
print(f"📊 Dataset: {len(df)} materials across {df['category'].nunique()} categories")
print(f"📈 Training accuracy: {train_score:.2%}")
print(f"🏷️  Categories: {', '.join(df['category'].unique())}")
print(f"📌 Features: strength, weight, cost, temperature, corrosion, hardness")

# Save both scaler and model
pickle.dump({'model': model, 'scaler': scaler}, open("model.pkl", "wb"))
print("✅ Model and scaler saved successfully!")