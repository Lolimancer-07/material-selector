import streamlit as st
import pandas as pd
import pickle
import numpy as np
import matplotlib.pyplot as plt
import os

# ============================================================

# ============================================================
st.set_page_config(
    page_title="Material Selector Pro",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)


st.markdown("""
    <style>
        * {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        
        [data-testid="stAppViewContainer"] {
            background: linear-gradient(135deg, #0f1419 0%, #1a1f2e 100%);
            color: #ffffff;
        }
        
        .main {
            background: linear-gradient(135deg, #0f1419 0%, #1a1f2e 100%);
        }
        
        /* Header styling */
        h1 {
            background: linear-gradient(90deg, #00d4ff 0%, #0099ff 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            font-weight: 900;
            font-size: 3.5em !important;
            margin-bottom: 10px;
        }
        
        h2 {
            background: linear-gradient(90deg, #00d4ff 0%, #0099ff 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            font-weight: 800;
            margin-top: 30px;
        }
        
        h3 {
            color: #00d4ff;
            font-weight: 700;
        }
        
        h4 {
            color: #ffffff;
            font-weight: 700;
        }
        
        p {
            color: #e0e0e0;
        }
        
        /* Tab styling */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
            background: transparent;
        }
        
        .stTabs [data-baseweb="tab"] {
            background: linear-gradient(90deg, rgba(0, 212, 255, 0.1) 0%, rgba(0, 153, 255, 0.1) 100%);
            border: 1px solid rgba(0, 212, 255, 0.3);
            border-radius: 12px;
            padding: 12px 24px;
            font-weight: 600;
            transition: all 0.3s ease;
        }
        
        .stTabs [data-baseweb="tab"]:hover {
            background: linear-gradient(90deg, rgba(0, 212, 255, 0.2) 0%, rgba(0, 153, 255, 0.2) 100%);
            border-color: rgba(0, 212, 255, 0.6);
            transform: translateY(-2px);
        }
        
        .stTabs [aria-selected="true"] [data-baseweb="tab"] {
            background: linear-gradient(90deg, #00d4ff 0%, #0099ff 100%);
            color: #0f1419;
            border-color: #00d4ff;
        }
        
        /* Metric styling */
        .metric-card, [data-testid="metric-container"] {
            background: linear-gradient(135deg, rgba(0, 212, 255, 0.1) 0%, rgba(0, 153, 255, 0.1) 100%);
            border: 1px solid rgba(0, 212, 255, 0.3);
            border-radius: 15px;
            padding: 20px;
            backdrop-filter: blur(10px);
        }
        
        /* Material card styling */
        .material-card {
            background: linear-gradient(135deg, rgba(0, 212, 255, 0.05) 0%, rgba(0, 153, 255, 0.05) 100%);
            border: 2px solid rgba(0, 212, 255, 0.3);
            border-left: 5px solid #00d4ff;
            border-radius: 12px;
            padding: 20px;
            margin: 15px 0;
            backdrop-filter: blur(10px);
            transition: all 0.3s ease;
        }
        
        .material-card:hover {
            border-color: rgba(0, 212, 255, 0.6);
            background: linear-gradient(135deg, rgba(0, 212, 255, 0.1) 0%, rgba(0, 153, 255, 0.1) 100%);
            transform: translateX(5px);
            box-shadow: 0 8px 24px rgba(0, 212, 255, 0.2);
        }
        
        .material-card h4 {
            color: #00d4ff;
            font-size: 1.3em;
            margin-bottom: 10px;
        }
        
        /* Input styling */
        .stNumberInput, .stSlider, .stSelectbox, .stMultiSelect, .stTextInput {
            background: transparent;
        }
        
        input, select, textarea {
            background-color: rgba(255, 255, 255, 0.05) !important;
            border: 1px solid rgba(0, 212, 255, 0.3) !important;
            color: #ffffff !important;
            border-radius: 8px !important;
        }
        
        input::placeholder {
            color: #888888;
        }
        
        input:focus, select:focus, textarea:focus {
            background-color: rgba(0, 212, 255, 0.1) !important;
            border-color: #00d4ff !important;
            box-shadow: 0 0 10px rgba(0, 212, 255, 0.3);
        }
        
        /* Button styling */
        .stButton > button {
            background: linear-gradient(90deg, #00d4ff 0%, #0099ff 100%);
            color: #0f1419 !important;
            border: none;
            font-weight: 700;
            border-radius: 10px;
            padding: 10px 24px;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(0, 212, 255, 0.3);
        }
        
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(0, 212, 255, 0.5);
        }
        
        .stButton > button:active {
            transform: translateY(0);
        }
        
        /* Info/Warning boxes */
        .stInfo, [data-testid="stAlert"] {
            background: linear-gradient(135deg, rgba(0, 212, 255, 0.15) 0%, rgba(0, 153, 255, 0.15) 100%);
            border: 1px solid rgba(0, 212, 255, 0.4);
            border-radius: 12px;
            padding: 20px;
        }
        
        .stWarning {
            background: linear-gradient(135deg, rgba(255, 153, 0, 0.15) 0%, rgba(255, 102, 0, 0.15) 100%);
            border: 1px solid rgba(255, 153, 0, 0.4);
            border-radius: 12px;
        }
        
        .stError {
            background: linear-gradient(135deg, rgba(255, 0, 0, 0.15) 0%, rgba(255, 102, 102, 0.15) 100%);
            border: 1px solid rgba(255, 0, 0, 0.4);
            border-radius: 12px;
        }
        
        .stSuccess {
            background: linear-gradient(135deg, rgba(0, 255, 100, 0.15) 0%, rgba(0, 200, 100, 0.15) 100%);
            border: 1px solid rgba(0, 255, 100, 0.4);
            border-radius: 12px;
        }
        
        /* Divider */
        .stDivider {
            border-top: 2px solid rgba(0, 212, 255, 0.2);
            margin: 30px 0;
        }
        
        /* Expander styling */
        .streamlit-expander {
            background: linear-gradient(135deg, rgba(0, 212, 255, 0.05) 0%, rgba(0, 153, 255, 0.05) 100%);
            border: 1px solid rgba(0, 212, 255, 0.2);
            border-radius: 10px;
        }
        
        /* Dataframe styling */
        .stDataFrame {
            color: #ffffff;
        }
        
        /* Markdown styling */
        .stMarkdown, div[data-testid="stMarkdownContainer"] {
            color: #e0e0e0;
        }
        
        /* Caption styling */
        .stCaption {
            color: #a0a0a0;
            font-style: italic;
        }
        
        /* Metric label styling */
        [data-testid="metric-container"] label {
            color: #00d4ff;
            font-weight: 600;
        }
        
        /* Smooth transitions */
        transition: all 0.3s ease;
    </style>
""", unsafe_allow_html=True)

# ============================================================

# ============================================================
@st.cache_resource
def load_data_and_model():
    """Load data and model with error handling"""
    try:
        if not os.path.exists("materials.csv"):
            st.error("❌ materials.csv not found!")
            st.stop()
        if not os.path.exists("model.pkl"):
            st.error("❌ model.pkl not found! Run model.py first.")
            st.stop()
        
        df = pd.read_csv("materials.csv")
        model_data = pickle.load(open("model.pkl", "rb"))
        
        if isinstance(model_data, dict):
            model = model_data['model']
            scaler = model_data['scaler']
        else:
            model = model_data
            scaler = None
        
        return df, model, scaler
    except Exception as e:
        st.error(f"❌ Error loading files: {str(e)}")
        st.stop()

df, model, scaler = load_data_and_model()


if "comparison_materials" not in st.session_state:
    st.session_state.comparison_materials = []
if "favorites" not in st.session_state:
    st.session_state.favorites = []

# ============================================================

# ============================================================
def score_material(material_row, requirements):
    """Score how well a material matches requirements"""
    score = 0
    mismatches = []
    
    if material_row["strength"] >= requirements[0]:
        score += 1
    else:
        mismatches.append(f"Strength: {material_row['strength']:.0f} MPa (need {requirements[0]:.0f})")
    
    if material_row["weight"] <= requirements[1]:
        score += 1
    else:
        mismatches.append(f"Weight: {material_row['weight']:.2f} g/cm³ (max {requirements[1]:.2f})")
    
    if material_row["cost"] <= requirements[2]:
        score += 1
    else:
        mismatches.append(f"Cost: ${material_row['cost']:.0f} (max ${requirements[2]:.0f})")
    
    if material_row["temp_limit"] >= requirements[3]:
        score += 1
    else:
        mismatches.append(f"Temp: {material_row['temp_limit']:.0f}°C (need {requirements[3]:.0f})")
    
    if material_row["corrosion"] >= requirements[4]:
        score += 1
    else:
        mismatches.append(f"Corrosion resistance: {material_row['corrosion']:.0f}/10")
    
    if material_row["hardness"] >= requirements[5]:
        score += 1
    else:
        mismatches.append(f"Hardness: {material_row['hardness']:.0f}/10")
    
    return score, mismatches

def get_recommendations_by_usecase(usecase):
    """Get materials recommended for specific use cases"""
    if usecase == "Aerospace":
        return df[(df['temp_limit'] >= 500) & (df['strength'] >= 300) & (df['weight'] <= 10)]
    elif usecase == "Medical":
        return df[df['corrosion'] >= 8].sort_values('corrosion', ascending=False)
    elif usecase == "Marine":
        return df[df['corrosion'] >= 8].sort_values('corrosion', ascending=False)
    elif usecase == "High-Temperature":
        return df[df['temp_limit'] >= 800].sort_values('temp_limit', ascending=False)
    elif usecase == "Lightweight":
        return df[df['weight'] <= 3].sort_values('weight')
    elif usecase == "Budget":
        return df[df['cost'] <= 50].sort_values('cost')
    return df

# ============================================================

# ============================================================


st.markdown("""
<div style='text-align: center; padding: 40px 20px; background: linear-gradient(135deg, rgba(0, 212, 255, 0.1) 0%, rgba(0, 153, 255, 0.1) 100%); border-radius: 20px; margin-bottom: 30px; border: 2px solid rgba(0, 212, 255, 0.3);'>
    <h1 style='margin: 0; font-size: 3.5em;'>🔬 Material Selector Pro</h1>
    <p style='color: #00d4ff; font-size: 1.2em; margin: 10px 0 0 0;'>Advanced intelligent material selection system</p>
    <p style='color: #a0a0a0; font-size: 1em; margin: 5px 0 0 0;'>62 premium materials | 4 categories | ML-powered matching</p>
</div>
""", unsafe_allow_html=True)


stat1, stat2, stat3, stat4 = st.columns(4)
with stat1:
    st.metric("📦 Total Materials", len(df), delta="60+ options")
with stat2:
    st.metric("🏢 Categories", df['category'].nunique(), delta="Metal, Composite, Polymer, Ceramic")
with stat3:
    st.metric("💪 Avg Strength", f"{df['strength'].mean():.0f} MPa", delta="300-800 MPa range")
with stat4:
    st.metric("💰 Price Range", f"${df['cost'].min():.0f}-${df['cost'].max():.0f}", delta="Budget friendly")


tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🎯 Quick Select", 
    "🔍 Advanced Search", 
    "⚖️ Compare Materials",
    "💡 Use Cases",
    "📊 Analytics"
])

# ============================================================

# ============================================================
with tab1:
    st.markdown("""
    <div style='background: linear-gradient(135deg, rgba(0, 212, 255, 0.1) 0%, rgba(0, 153, 255, 0.1) 100%); padding: 20px; border-radius: 12px; border: 1px solid rgba(0, 212, 255, 0.3); margin-bottom: 20px;'>
        <h3 style='color: #00d4ff; margin-top: 0;'>⚡ Quick Material Selection</h3>
        <p>Set your requirements and find the perfect material instantly</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 2], gap="large")
    
    with col1:
        st.markdown("<h4 style='color: #00d4ff;'>📋 Filter by Category</h4>", unsafe_allow_html=True)
        categories = df['category'].unique()
        selected_category = st.selectbox("Select Material Category", ["All"] + list(categories), label_visibility="collapsed")
        
        if selected_category != "All":
            category_df = df[df['category'] == selected_category]
        else:
            category_df = df
        
        st.markdown(f"<p style='color: #00d4ff; font-weight: bold; margin: 15px 0 10px 0;'>✅ Found {len(category_df)} materials</p>", unsafe_allow_html=True)
        
        st.markdown("<h4 style='color: #00d4ff;'>🎚️ Set Your Requirements</h4>", unsafe_allow_html=True)
        strength_req = st.slider("💪 Min Strength (MPa)", 0, 1000, 300, help="Material must meet this strength")
        weight_req = st.slider("⚖️ Max Weight (g/cm³)", 0.0, 20.0, 5.0, help="Lower is lighter")
        cost_req = st.slider("💰 Max Cost ($)", 0, 400, 100, help="Budget constraint")
        temp_req = st.slider("🔥 Min Temperature (°C)", 0, 3500, 300, help="Heat tolerance needed")
        corrosion_req = st.slider("🛡️ Min Corrosion Resistance", 1, 10, 5, help="1=Low, 10=Excellent")
        hardness_req = st.slider("💎 Min Hardness", 1, 10, 5, help="1=Soft, 10=Very Hard")
    
    with col2:
        requirements = (strength_req, weight_req, cost_req, temp_req, corrosion_req, hardness_req)
        
        
        results = []
        for idx, row in category_df.iterrows():
            score, mismatches = score_material(row, requirements)
            results.append((row, score, mismatches))
        
        results.sort(key=lambda x: x[1], reverse=True)
        
        if results:
            best_material = results[0]
            
            
            st.markdown("""
            <div style='background: linear-gradient(135deg, rgba(0, 255, 100, 0.1) 0%, rgba(0, 200, 100, 0.1) 100%); padding: 25px; border-radius: 15px; border: 2px solid rgba(0, 255, 100, 0.4); margin-bottom: 20px;'>
                <h3 style='color: #00ff64; margin-top: 0;'>🏆 Best Match Found!</h3>
            </div>
            """, unsafe_allow_html=True)
            
            col_m1, col_m2, col_m3 = st.columns(3)
            
            with col_m1:
                st.metric("Material", best_material[0]['name'], border=True)
            with col_m2:
                score_pct = (best_material[1] / 6) * 100
                st.metric("Match Score", f"{score_pct:.0f}%", delta=f"{best_material[1]}/6 criteria", border=True)
            with col_m3:
                st.metric("Category", best_material[0]['category'], border=True)
            
            
            st.divider()
            st.markdown("<h4 style='color: #00d4ff;'>📊 Material Properties</h4>", unsafe_allow_html=True)
            
            props_col1, props_col2, props_col3 = st.columns(3)
            
            with props_col1:
                st.metric("💪 Strength", f"{best_material[0]['strength']:.0f} MPa", border=True)
                st.metric("⚖️ Weight", f"{best_material[0]['weight']:.2f} g/cm³", border=True)
                st.metric("💰 Cost", f"${best_material[0]['cost']:.0f}", border=True)
            
            with props_col2:
                st.metric("🔥 Max Temp", f"{best_material[0]['temp_limit']:.0f}°C", border=True)
                st.metric("🛡️ Corrosion Resist.", f"{best_material[0]['corrosion']:.0f}/10", border=True)
                st.metric("💎 Hardness", f"{best_material[0]['hardness']:.0f}/10", border=True)
            
            with props_col3:
                st.metric("📐 Ductility", f"{best_material[0]['ductility']:.0f}/10", border=True)
                st.metric("🌡️ Thermal Cond.", f"{best_material[0]['thermal_conductivity']:.1f} W/mK", border=True)
                st.metric("⚡ Electrical Cond.", f"{best_material[0]['electrical_conductivity']:.0f}", border=True)
            
            
            st.divider()
            st.markdown(f"<p style='background: linear-gradient(135deg, rgba(0, 212, 255, 0.1) 0%, rgba(0, 153, 255, 0.1) 100%); padding: 15px; border-radius: 10px; border-left: 4px solid #00d4ff;'><strong style='color: #00d4ff;'>🎯 Common Uses:</strong> <span style='color: #e0e0e0;'>{best_material[0]['use_cases']}</span></p>", unsafe_allow_html=True)
            
            
            st.divider()
            st.markdown("<h4 style='color: #00d4ff;'>🔄 Also Consider (Top Alternatives)</h4>", unsafe_allow_html=True)
            
            for i, (mat, score, mismatches) in enumerate(results[1:4], 1):
                with st.expander(f"#{i} **{mat['name']}** • {mat['category']} • ${mat['cost']:.0f} • Match: {score}/6", expanded=i==1):
                    col_a1, col_a2, col_a3 = st.columns(3)
                    with col_a1:
                        st.metric("💪 Strength", f"{mat['strength']:.0f} MPa", border=True)
                    with col_a2:
                        st.metric("⚖️ Weight", f"{mat['weight']:.2f} g/cm³", border=True)
                    with col_a3:
                        st.metric("💰 Cost", f"${mat['cost']:.0f}", border=True)
                    
                    if mismatches:
                        st.warning("⚠️ **Mismatches:**\n" + "\n".join(mismatches))
                    
                    st.caption(f"**🎯 Use Cases:** {mat['use_cases']}")
                    
                    col_btn1, col_btn2 = st.columns([1, 3])
                    with col_btn1:
                        if st.button("➕ Compare", key=f"add_{i}"):
                            if mat['name'] not in st.session_state.comparison_materials:
                                st.session_state.comparison_materials.append(mat['name'])
                                st.success(f"✅ Added {mat['name']} to comparison!")


# ============================================================

# ============================================================
with tab2:
    st.markdown("""
    <div style='background: linear-gradient(135deg, rgba(0, 212, 255, 0.1) 0%, rgba(0, 153, 255, 0.1) 100%); padding: 20px; border-radius: 12px; border: 1px solid rgba(0, 212, 255, 0.3); margin-bottom: 20px;'>
        <h3 style='color: #00d4ff; margin-top: 0;'>🔍 Advanced Material Search</h3>
        <p>Fine-tune your search with detailed filters</p>
    </div>
    """, unsafe_allow_html=True)
    
    search_col1, search_col2 = st.columns(2, gap="large")
    
    with search_col1:
        st.markdown("<h4 style='color: #00d4ff;'>🔎 Search & Filter</h4>", unsafe_allow_html=True)
        
        search_text = st.text_input("🔎 Search materials by name", placeholder="e.g., Steel, Aluminum, Carbon Fiber")
        
        if search_text:
            search_df = df[df['name'].str.contains(search_text, case=False)]
        else:
            search_df = df
        
        category_filter = st.multiselect("Filter by Category", df['category'].unique(), default=df['category'].unique())
        search_df = search_df[search_df['category'].isin(category_filter)]
        
        st.markdown("<h4 style='color: #00d4ff;'>📊 Property Ranges</h4>", unsafe_allow_html=True)
        col_min_str, col_max_str = st.columns(2)
        with col_min_str:
            min_strength = st.number_input("Min Strength (MPa)", 0, 1000, 0)
        with col_max_str:
            max_strength = st.number_input("Max Strength", 0, 1000, 1000)
        
        col_min_w, col_max_w = st.columns(2)
        with col_min_w:
            min_weight = st.number_input("Min Weight (g/cm³)", 0.0, 20.0, 0.0)
        with col_max_w:
            max_weight = st.number_input("Max Weight", 0.0, 20.0, 20.0)
        
        col_min_c, col_max_c = st.columns(2)
        with col_min_c:
            min_cost = st.number_input("Min Cost ($)", 0, 400, 0)
        with col_max_c:
            max_cost = st.number_input("Max Cost", 0, 400, 400)
    
    with search_col2:
        col_min_t, col_max_t = st.columns(2)
        with col_min_t:
            min_temp = st.number_input("Min Temp (°C)", 0, 4000, 0)
        with col_max_t:
            max_temp = st.number_input("Max Temp", 0, 4000, 4000)
        
        col_min_corr, col_max_corr = st.columns(2)
        with col_min_corr:
            min_corrosion = st.number_input("Min Corrosion Resist", 1, 10, 1)
        with col_max_corr:
            max_corrosion = st.number_input("Max Corrosion Resist", 1, 10, 10)
        
        col_min_hard, col_max_hard = st.columns(2)
        with col_min_hard:
            min_hardness = st.number_input("Min Hardness", 1, 10, 1)
        with col_max_hard:
            max_hardness = st.number_input("Max Hardness", 1, 10, 10)
        
        st.markdown("<h4 style='color: #00d4ff;'>🎯 Sort Options</h4>", unsafe_allow_html=True)
        sort_by = st.selectbox("Sort Results By", ["Name", "Strength", "Weight", "Cost", "Temperature", "Corrosion", "Hardness"])
    
    
    filtered_df = search_df[
        (search_df['strength'] >= min_strength) & (search_df['strength'] <= max_strength) &
        (search_df['weight'] >= min_weight) & (search_df['weight'] <= max_weight) &
        (search_df['cost'] >= min_cost) & (search_df['cost'] <= max_cost) &
        (search_df['temp_limit'] >= min_temp) & (search_df['temp_limit'] <= max_temp) &
        (search_df['corrosion'] >= min_corrosion) & (search_df['corrosion'] <= max_corrosion) &
        (search_df['hardness'] >= min_hardness) & (search_df['hardness'] <= max_hardness)
    ]
    
    st.divider()
    
    if filtered_df.empty:
        st.markdown("""
        <div style='background: linear-gradient(135deg, rgba(255, 153, 0, 0.15) 0%, rgba(255, 102, 0, 0.15) 100%); padding: 20px; border-radius: 12px; border: 1px solid rgba(255, 153, 0, 0.4); text-align: center;'>
            <p style='color: #ffaa00; font-size: 1.1em;'>😕 No materials match your criteria.</p>
            <p style='color: #a0a0a0;'>Try adjusting your filters for more results</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        
        sort_col_map = {
            "Name": "name",
            "Strength": "strength",
            "Weight": "weight",
            "Cost": "cost",
            "Temperature": "temp_limit",
            "Corrosion": "corrosion",
            "Hardness": "hardness"
        }
        
        filtered_df = filtered_df.sort_values(sort_col_map[sort_by])
        
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, rgba(0, 255, 100, 0.1) 0%, rgba(0, 200, 100, 0.1) 100%); padding: 15px; border-radius: 10px; border: 1px solid rgba(0, 255, 100, 0.3); margin-bottom: 20px;'>
            <h4 style='color: #00ff64; margin: 0;'>✅ {len(filtered_df)} Materials Found</h4>
        </div>
        """, unsafe_allow_html=True)
        
        
        for idx, row in filtered_df.iterrows():
            col_name, col_btn = st.columns([4, 1])
            
            with col_name:
                with st.expander(f"🔹 **{row['name']}** • {row['category']} • ${row['cost']:.0f}"):
                    disp_col1, disp_col2, disp_col3 = st.columns(3)
                    
                    with disp_col1:
                        st.metric("💪 Strength", f"{row['strength']:.0f} MPa", border=True)
                        st.metric("⚖️ Weight", f"{row['weight']:.2f} g/cm³", border=True)
                        st.metric("💰 Cost", f"${row['cost']:.0f}", border=True)
                    
                    with disp_col2:
                        st.metric("🔥 Max Temp", f"{row['temp_limit']:.0f}°C", border=True)
                        st.metric("🛡️ Corrosion", f"{row['corrosion']:.0f}/10", border=True)
                        st.metric("💎 Hardness", f"{row['hardness']:.0f}/10", border=True)
                    
                    with disp_col3:
                        st.metric("📐 Ductility", f"{row['ductility']:.0f}/10", border=True)
                        st.metric("🌡️ Thermal", f"{row['thermal_conductivity']:.1f} W/mK", border=True)
                        st.metric("⚡ Electrical", f"{row['electrical_conductivity']:.0f}", border=True)
                    
                    st.divider()
                    st.markdown(f"<p style='color: #00d4ff;'><strong>🎯 Use Cases:</strong> {row['use_cases']}</p>", unsafe_allow_html=True)
            
            with col_btn:
                if st.button("➕", key=f"add_btn_{idx}", help="Add to comparison"):
                    if row['name'] not in st.session_state.comparison_materials:
                        st.session_state.comparison_materials.append(row['name'])
                        st.rerun()


# ============================================================

# ============================================================
with tab3:
    st.markdown("""
    <div style='background: linear-gradient(135deg, rgba(0, 212, 255, 0.1) 0%, rgba(0, 153, 255, 0.1) 100%); padding: 20px; border-radius: 12px; border: 1px solid rgba(0, 212, 255, 0.3); margin-bottom: 20px;'>
        <h3 style='color: #00d4ff; margin-top: 0;'>⚖️ Compare Materials</h3>
        <p>Side-by-side property comparison with visual analysis</p>
    </div>
    """, unsafe_allow_html=True)
    
    col_sel1, col_sel2, col_sel3 = st.columns([1.5, 1.5, 1], gap="large")
    
    with col_sel1:
        material1 = st.selectbox("🔹 Material 1", df['name'].values, label_visibility="collapsed")
    
    with col_sel2:
        material2 = st.selectbox("🔹 Material 2", df['name'].values, index=1, label_visibility="collapsed")
    
    with col_sel3:
        if st.button("🔄 Compare", use_container_width=True):
            st.rerun()
    
    
    mat1 = df[df['name'] == material1].iloc[0]
    mat2 = df[df['name'] == material2].iloc[0]
    
    
    st.divider()
    st.markdown(f"""
    <div style='display: flex; justify-content: space-between; gap: 20px;'>
        <div style='flex: 1; background: linear-gradient(135deg, rgba(0, 212, 255, 0.1) 0%, rgba(0, 153, 255, 0.1) 100%); padding: 20px; border-radius: 12px; border: 2px solid rgba(0, 212, 255, 0.3); text-align: center;'>
            <h3 style='color: #00d4ff; margin: 0;'>💪 {material1}</h3>
            <p style='color: #a0a0a0; margin: 10px 0 0 0;'>{mat1['category']}</p>
        </div>
        <div style='flex: 1; background: linear-gradient(135deg, rgba(0, 153, 255, 0.1) 0%, rgba(0, 100, 200, 0.1) 100%); padding: 20px; border-radius: 12px; border: 2px solid rgba(0, 153, 255, 0.3); text-align: center;'>
            <h3 style='color: #0099ff; margin: 0;'>💪 {material2}</h3>
            <p style='color: #a0a0a0; margin: 10px 0 0 0;'>{mat2['category']}</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    st.markdown("<h4 style='color: #00d4ff;'>📊 Property Comparison Table</h4>", unsafe_allow_html=True)
    
    comparison_data = {
        'Property': ['💪 Strength (MPa)', '⚖️ Weight (g/cm³)', '💰 Cost ($)', '🔥 Max Temp (°C)', 
                     '🛡️ Corrosion (1-10)', '💎 Hardness (1-10)', '📐 Ductility (1-10)', 
                     '🌡️ Thermal (W/mK)', '⚡ Electrical Cond.', '🏷️ Category'],
        material1: [f"{mat1['strength']:.0f}", f"{mat1['weight']:.2f}", f"${mat1['cost']:.0f}", 
                    f"{mat1['temp_limit']:.0f}", f"{mat1['corrosion']:.0f}", f"{mat1['hardness']:.0f}",
                    f"{mat1['ductility']:.0f}", f"{mat1['thermal_conductivity']:.1f}", 
                    f"{mat1['electrical_conductivity']:.0f}", mat1['category']],
        material2: [f"{mat2['strength']:.0f}", f"{mat2['weight']:.2f}", f"${mat2['cost']:.0f}", 
                    f"{mat2['temp_limit']:.0f}", f"{mat2['corrosion']:.0f}", f"{mat2['hardness']:.0f}",
                    f"{mat2['ductility']:.0f}", f"{mat2['thermal_conductivity']:.1f}", 
                    f"{mat2['electrical_conductivity']:.0f}", mat2['category']]
    }
    
    comp_df = pd.DataFrame(comparison_data)
    st.dataframe(comp_df, use_container_width=True, hide_index=True)
    
    
    st.divider()
    st.markdown("<h4 style='color: #00d4ff;'>📈 Visual Radar Comparison</h4>", unsafe_allow_html=True)
    
    col_chart1, col_chart2 = st.columns(2, gap="large")
    
    with col_chart1:
        st.markdown(f"<h4 style='text-align: center; color: #00d4ff;'>{material1}</h4>", unsafe_allow_html=True)
        props = ['Strength', 'Weight', 'Corrosion', 'Hardness', 'Ductility']
        vals1 = [
            min(mat1['strength'] / 100, 10),
            10 - mat1['weight'],
            mat1['corrosion'],
            mat1['hardness'],
            mat1['ductility']
        ]
        
        fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(projection='polar'), facecolor='#0f1419')
        fig.patch.set_facecolor('#0f1419')
        angles = np.linspace(0, 2 * np.pi, len(props), endpoint=False).tolist()
        vals1_plot = vals1 + [vals1[0]]
        angles_plot = angles + [angles[0]]
        
        ax.plot(angles_plot, vals1_plot, 'o-', linewidth=3, color='#00d4ff', label=material1)
        ax.fill(angles_plot, vals1_plot, alpha=0.25, color='#00d4ff')
        ax.set_xticks(angles)
        ax.set_xticklabels(props, color='#e0e0e0')
        ax.set_ylim(0, 10)
        ax.grid(True, color='#00d4ff33')
        ax.set_facecolor('#1a1f2e')
        st.pyplot(fig, use_container_width=True)
    
    with col_chart2:
        st.markdown(f"<h4 style='text-align: center; color: #0099ff;'>{material2}</h4>", unsafe_allow_html=True)
        vals2 = [
            min(mat2['strength'] / 100, 10),
            10 - mat2['weight'],
            mat2['corrosion'],
            mat2['hardness'],
            mat2['ductility']
        ]
        
        fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(projection='polar'), facecolor='#0f1419')
        fig.patch.set_facecolor('#0f1419')
        vals2_plot = vals2 + [vals2[0]]
        
        ax.plot(angles_plot, vals2_plot, 'o-', linewidth=3, color='#0099ff', label=material2)
        ax.fill(angles_plot, vals2_plot, alpha=0.25, color='#0099ff')
        ax.set_xticks(angles)
        ax.set_xticklabels(props, color='#e0e0e0')
        ax.set_ylim(0, 10)
        ax.grid(True, color='#0099ff33')
        ax.set_facecolor('#1a1f2e')
        st.pyplot(fig, use_container_width=True)


# ============================================================

# ============================================================
with tab4:
    st.markdown("""
    <div style='background: linear-gradient(135deg, rgba(0, 212, 255, 0.1) 0%, rgba(0, 153, 255, 0.1) 100%); padding: 20px; border-radius: 12px; border: 1px solid rgba(0, 212, 255, 0.3); margin-bottom: 20px;'>
        <h3 style='color: #00d4ff; margin-top: 0;'>💡 Materials by Use Case</h3>
        <p>Pre-configured recommendations for common applications</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 2], gap="large")
    
    with col1:
        st.markdown("<h4 style='color: #00d4ff;'>🎯 Select Use Case</h4>", unsafe_allow_html=True)
        usecase = st.radio("", [
            "🚀 Aerospace",
            "🏥 Medical",
            "🌊 Marine",
            "🔥 High-Temperature",
            "📦 Lightweight",
            "💵 Budget"
        ], label_visibility="collapsed")
        usecase = usecase.split(" ", 1)[1]
    
    with col2:
        usecase_descriptions = {
            "Aerospace": "🚀 High strength-to-weight ratio, excellent temperature resistance (500°C+), optimal for aircraft structures",
            "Medical": "🏥 High corrosion resistance, biocompatible materials, sterilizable and body-safe",
            "Marine": "🌊 Excellent corrosion resistance, saltwater durability, long service life in harsh conditions",
            "High-Temperature": "🔥 Can withstand 800°C+ without degradation, extreme thermal stability",
            "Lightweight": "📦 Density under 3 g/cm³, perfect for portable and mobile applications",
            "Budget": "💵 Cost-effective options under $50, best value-for-money materials"
        }
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, rgba(0, 212, 255, 0.1) 0%, rgba(0, 153, 255, 0.1) 100%); padding: 15px; border-radius: 10px; border: 1px solid rgba(0, 212, 255, 0.3);'>
            <p style='color: #e0e0e0; margin: 0;'>{usecase_descriptions[usecase]}</p>
        </div>
        """, unsafe_allow_html=True)
    
    
    usecase_df = get_recommendations_by_usecase(usecase)
    
    st.divider()
    
    
    if usecase == "Aerospace":
        usecase_df = usecase_df.sort_values('strength', ascending=False)
    elif usecase == "Medical":
        usecase_df = usecase_df.sort_values('corrosion', ascending=False)
    elif usecase == "Marine":
        usecase_df = usecase_df.sort_values('corrosion', ascending=False)
    elif usecase == "High-Temperature":
        usecase_df = usecase_df.sort_values('temp_limit', ascending=False)
    elif usecase == "Lightweight":
        usecase_df = usecase_df.sort_values('weight')
    elif usecase == "Budget":
        usecase_df = usecase_df.sort_values('cost')
    
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, rgba(0, 255, 100, 0.1) 0%, rgba(0, 200, 100, 0.1) 100%); padding: 15px; border-radius: 10px; border: 1px solid rgba(0, 255, 100, 0.3); margin-bottom: 20px;'>
        <h4 style='color: #00ff64; margin: 0;'>✅ {len(usecase_df)} Recommended Materials</h4>
    </div>
    """, unsafe_allow_html=True)
    
    for idx, (_, row) in enumerate(usecase_df.head(10).iterrows(), 1):
        st.markdown(f"""
        <div class="material-card">
            <h4>#{idx} {row['name']} 🏆</h4>
            <p style='margin: 10px 0;'><strong style='color: #00d4ff;'>{row['category']}</strong> • <strong style='color: #00ff64;'>${row['cost']:.0f}</strong></p>
            <p style='color: #a0a0a0; margin: 0;'>{row['use_cases']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        prop_col1, prop_col2, prop_col3, prop_col4 = st.columns(4)
        with prop_col1:
            st.metric("💪 Strength", f"{row['strength']:.0f} MPa", border=True)
        with prop_col2:
            st.metric("⚖️ Weight", f"{row['weight']:.2f} g/cm³", border=True)
        with prop_col3:
            st.metric("🔥 Temp", f"{row['temp_limit']:.0f}°C", border=True)
        with prop_col4:
            st.metric("🛡️ Corrosion", f"{row['corrosion']:.0f}/10", border=True)
        
        st.divider()

# ============================================================

# ============================================================
with tab5:
    st.markdown("""
    <div style='background: linear-gradient(135deg, rgba(0, 212, 255, 0.1) 0%, rgba(0, 153, 255, 0.1) 100%); padding: 20px; border-radius: 12px; border: 1px solid rgba(0, 212, 255, 0.3); margin-bottom: 20px;'>
        <h3 style='color: #00d4ff; margin-top: 0;'>📊 Material Analytics Dashboard</h3>
        <p>Comprehensive insights and trends across the material database</p>
    </div>
    """, unsafe_allow_html=True)
    
    
    stat1, stat2, stat3, stat4 = st.columns(4)
    with stat1:
        st.metric("📊 Avg Strength", f"{df['strength'].mean():.0f} MPa", delta="Range: 50-800", border=True)
    with stat2:
        st.metric("💰 Avg Cost", f"${df['cost'].mean():.0f}", delta="Range: $5-$300", border=True)
    with stat3:
        st.metric("🔥 Heat Champ", f"{df.loc[df['temp_limit'].idxmax(), 'name']}", delta=f"{df['temp_limit'].max():.0f}°C", border=True)
    with stat4:
        st.metric("🛡️ Corrosion Champ", f"{df.loc[df['corrosion'].idxmax(), 'name']}", delta=f"{df['corrosion'].max():.0f}/10", border=True)
    
    
    st.divider()
    st.markdown("<h4 style='color: #00d4ff;'>📈 Strength vs Weight Analysis</h4>", unsafe_allow_html=True)
    
    col_chart1, col_chart2 = st.columns(2, gap="large")
    
    with col_chart1:
        st.markdown("<p style='text-align: center; color: #00d4ff; font-weight: bold;'>💪 Strength vs Weight by Category</p>", unsafe_allow_html=True)
        fig, ax = plt.subplots(figsize=(8, 5), facecolor='#0f1419')
        fig.patch.set_facecolor('#0f1419')
        
        colors = {'Metal': '#00d4ff', 'Composite': '#0099ff', 'Polymer': '#00ff64', 'Ceramic': '#ffaa00'}
        for category in df['category'].unique():
            cat_data = df[df['category'] == category]
            ax.scatter(cat_data['weight'], cat_data['strength'], label=category, s=100, alpha=0.7, color=colors.get(category, '#00d4ff'))
        
        ax.set_xlabel("Weight (g/cm³)", color='#e0e0e0', fontsize=10)
        ax.set_ylabel("Strength (MPa)", color='#e0e0e0', fontsize=10)
        ax.legend(loc='best', facecolor='#1a1f2e', edgecolor='#00d4ff4d')
        ax.grid(True, alpha=0.2, color='#00d4ff33')
        ax.set_facecolor('#1a1f2e')
        ax.tick_params(colors='#e0e0e0')
        st.pyplot(fig, use_container_width=True)
    
    with col_chart2:
        st.markdown("<p style='text-align: center; color: #00d4ff; font-weight: bold;'>💰 Cost vs Strength (Colored by Temp)</p>", unsafe_allow_html=True)
        fig, ax = plt.subplots(figsize=(8, 5), facecolor='#0f1419')
        fig.patch.set_facecolor('#0f1419')
        
        scatter = ax.scatter(df['strength'], df['cost'], c=df['temp_limit'], cmap='plasma', s=100, alpha=0.7, edgecolors='#00d4ff4d', linewidth=1)
        ax.set_xlabel("Strength (MPa)", color='#e0e0e0', fontsize=10)
        ax.set_ylabel("Cost ($)", color='#e0e0e0', fontsize=10)
        cbar = plt.colorbar(scatter, ax=ax, label="Max Temp (°C)")
        cbar.set_label("Max Temp (°C)", color='#e0e0e0')
        cbar.ax.tick_params(colors='#e0e0e0')
        ax.grid(True, alpha=0.2, color='#00d4ff33')
        ax.set_facecolor('#1a1f2e')
        ax.tick_params(colors='#e0e0e0')
        st.pyplot(fig, use_container_width=True)
    
    st.divider()
    st.markdown("<h4 style='color: #00d4ff;'>🔥 Distribution Analysis</h4>", unsafe_allow_html=True)
    
    col_chart3, col_chart4 = st.columns(2, gap="large")
    
    with col_chart3:
        st.markdown("<p style='text-align: center; color: #00d4ff; font-weight: bold;'>🔥 Temperature Resistance by Category</p>", unsafe_allow_html=True)
        fig, ax = plt.subplots(figsize=(8, 5), facecolor='#0f1419')
        fig.patch.set_facecolor('#0f1419')
        
        categories = df['category'].unique()
        temp_by_cat = [df[df['category'] == cat]['temp_limit'].values for cat in categories]
        bp = ax.boxplot(temp_by_cat, tick_labels=categories, patch_artist=True)
        
        for patch in bp['boxes']:
            patch.set_facecolor('#00d4ff')
            patch.set_alpha(0.6)
        for whisker in bp['whiskers']:
            whisker.set_color('#00d4ff80')
        for cap in bp['caps']:
            cap.set_color('#00d4ff80')
        for median in bp['medians']:
            median.set_color('#00ff64')
            median.set_linewidth(2)
        
        ax.set_ylabel("Max Temperature (°C)", color='#e0e0e0', fontsize=10)
        ax.tick_params(colors='#e0e0e0', axis='x', rotation=45)
        ax.tick_params(colors='#e0e0e0')
        ax.grid(True, alpha=0.2, color='#00d4ff33', axis='y')
        ax.set_facecolor('#1a1f2e')
        st.pyplot(fig, use_container_width=True)
    
    with col_chart4:
        st.markdown("<p style='text-align: center; color: #00d4ff; font-weight: bold;'>🧬 Property Correlation Matrix</p>", unsafe_allow_html=True)
        corr_cols = ['strength', 'weight', 'cost', 'temp_limit', 'corrosion', 'hardness']
        corr_matrix = df[corr_cols].corr()
        
        fig, ax = plt.subplots(figsize=(8, 6), facecolor='#0f1419')
        fig.patch.set_facecolor('#0f1419')
        
        im = ax.imshow(corr_matrix, cmap='coolwarm', aspect='auto', vmin=-1, vmax=1)
        
        
        ax.set_xticks(np.arange(len(corr_cols)))
        ax.set_yticks(np.arange(len(corr_cols)))
        ax.set_xticklabels(corr_cols, rotation=45, ha='right', color='#e0e0e0')
        ax.set_yticklabels(corr_cols, color='#e0e0e0')
        
        
        for i in range(len(corr_cols)):
            for j in range(len(corr_cols)):
                text = ax.text(j, i, f'{corr_matrix.iloc[i, j]:.2f}',
                              ha="center", va="center", color="white", fontsize=10, fontweight='bold')
        
        cbar = plt.colorbar(im, ax=ax, label='Correlation')
        cbar.set_label('Correlation', color='#e0e0e0')
        cbar.ax.tick_params(colors='#e0e0e0')
        ax.set_facecolor('#1a1f2e')
        plt.tight_layout()
        st.pyplot(fig, use_container_width=True)
    
    st.divider()
    st.markdown("<h4 style='color: #00d4ff;'>📋 Full Material Database</h4>", unsafe_allow_html=True)
    st.dataframe(df, use_container_width=True, hide_index=True)
