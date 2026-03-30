import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import pickle

df = pd.read_csv("materials.csv")

X = df[["strength","weight","cost","temp_limit","corrosion","hardness"]]
y = df["name"]

model = RandomForestClassifier(n_estimators=100)
model.fit(X, y)

pickle.dump(model, open("model.pkl", "wb"))

print("Advanced model trained!")