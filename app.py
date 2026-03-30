import streamlit as st
import pandas as pd
import pickle
import numpy as np
import matplotlib.pyplot as plt

# Load data
df = pd.read_csv("materials.csv")
model = pickle.load(open("model.pkl", "rb"))

st.set_page_config(layout="wide")
st.title("🤖 Advanced AI Material Selection System")

if "messages" not in st.session_state:
    st.session_state.messages = []

# ================= INPUT MODE =================
st.markdown("## 🔄 Choose Input Mode")

mode = st.radio("Select Mode:", ["💬 Chat Mode", "📥 Engineering Mode"])

def parse_input(text):
    text = text.lower()
    strength, weight, cost, temp, corrosion, hardness = 300, 5, 100, 200, 5, 5

    if "high strength" in text: strength = 800
    if "light" in text: weight = 2
    if "cheap" in text: cost = 50
    if "high temperature" in text: temp = 500
    if "corrosion" in text: corrosion = 9
    if "hard" in text: hardness = 8

    return strength, weight, cost, temp, corrosion, hardness

# ================= CHAT MODE =================
if mode == "💬 Chat Mode":
    user_input = st.chat_input("Describe your requirement...")

    if user_input:
        values = parse_input(user_input)
        st.session_state.messages.append(("user", user_input))

# ================= FORM MODE =================
else:
    st.markdown("### ⚙️ Enter Engineering Values")

    col1, col2 = st.columns(2)

    with col1:
        strength = st.number_input("Strength", 50, 1000, 300)
        weight = st.number_input("Weight", 1.0, 10.0, 5.0)
        cost = st.number_input("Cost", 10, 300, 100)

    with col2:
        temp = st.number_input("Temperature", 50, 600, 200)
        corrosion = st.number_input("Corrosion Resistance", 1, 10, 5)
        hardness = st.number_input("Hardness", 1, 10, 5)

    if st.button("Analyze"):
        values = (strength, weight, cost, temp, corrosion, hardness)
        st.session_state.messages.append(("user", f"Manual Input: {values}"))

# ================= PROCESS =================
if "values" in locals():

    input_data = [list(values)]

    prediction = model.predict(input_data)[0]

    confidence = ""
    if hasattr(model, "predict_proba"):
        confidence = f"{np.max(model.predict_proba(input_data))*100:.1f}%"

    results = []
    for i, row in df.iterrows():
        score = 0
        reasons = []
        rejects = []

        if row["strength"] >= values[0]:
            score += 1
            reasons.append("Strong")
        else:
            rejects.append("Weak")

        if row["weight"] <= values[1]:
            score += 1
            reasons.append("Light")
        else:
            rejects.append("Heavy")

        if row["cost"] <= values[2]:
            score += 1
            reasons.append("Affordable")
        else:
            rejects.append("Expensive")

        if row["temp_limit"] >= values[3]:
            score += 1
            reasons.append("Heat resistant")
        else:
            rejects.append("Temp issue")

        if row["corrosion"] >= values[4]:
            score += 1
            reasons.append("Corrosion resistant")

        if row["hardness"] >= values[5]:
            score += 1
            reasons.append("Hard material")

        results.append((row["name"], score, reasons, rejects, row))

    ranked = sorted(results, key=lambda x: x[1], reverse=True)
    best = ranked[0]

    # ================= PROFESSIONAL GRAPH =================
    fig, ax = plt.subplots(figsize=(8,6))

    colors = []
    for mat in df["name"]:
        if mat in ["Steel", "Stainless Steel", "Cast Iron"]:
            colors.append("blue")
        elif mat in ["Aluminum", "Magnesium"]:
            colors.append("green")
        elif mat in ["Plastic", "Rubber"]:
            colors.append("red")
        else:
            colors.append("gray")

    ax.scatter(df["weight"], df["strength"], c=colors, s=80, alpha=0.7)

    ax.scatter(best[4]["weight"], best[4]["strength"],
               color="orange", s=200, edgecolors="black", label="Best Choice")

    for i, txt in enumerate(df["name"]):
        ax.annotate(txt,
                    (df["weight"][i], df["strength"][i]),
                    textcoords="offset points",
                    xytext=(5,5),
                    fontsize=9)

    ax.set_xlabel("Weight (g/cm³)", fontsize=12)
    ax.set_ylabel("Strength (MPa)", fontsize=12)
    ax.set_title("Material Selection Map", fontsize=14, weight='bold')

    ax.grid(True, linestyle='--', alpha=0.5)
    ax.legend()

    ax.set_facecolor("#f8f9fa")
    fig.patch.set_facecolor("#ffffff")

    plt.tight_layout()

    # ================= RESPONSE =================
    reply = f"""
### 🏆 Best Material: **{best[0]}**

🤖 ML Prediction: **{prediction}**  
📊 Confidence: **{confidence}**

---

### 🧠 Why:
{", ".join(best[2])}

---

### ❌ Why NOT Others:
"""

    for mat in ranked[1:3]:
        reply += f"\n**{mat[0]}** → {', '.join(mat[3])}"

    reply += """

---

### ⚖️ Trade-offs
- Higher strength → higher cost  
- Lower weight → lower durability  

---

### ⚠️ Risk
Wrong material may cause structural failure.
"""

    st.session_state.messages.append(("assistant", reply))

    st.pyplot(fig)

# ================= CHAT DISPLAY =================
st.markdown("---")

for role, msg in st.session_state.messages:
    with st.chat_message(role):
        st.markdown(msg)