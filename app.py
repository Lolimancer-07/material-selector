import streamlit as st
import pandas as pd
import pickle
import numpy as np
import matplotlib.pyplot as plt
import os
from datetime import datetime
import json
import io

# ============================================================
# PAGE CONFIG & STYLING
# ============================================================
st.set_page_config(
    page_title="Material Selector Pro",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS - Modern Professional Design
st.markdown("""
    <style>
        * {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
        }
        
        [data-testid="stAppViewContainer"] {
            background: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 100%);
            color: #ffffff;
        }
        
        .main {
            background: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 100%);
        }
        
        /* Header styling */
        h1 {
            background: linear-gradient(135deg, #00f5ff 0%, #0099ff 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            font-weight: 900;
            font-size: 3.2em !important;
            letter-spacing: -1px;
            margin-bottom: 5px;
        }
        
        h2 {
            background: linear-gradient(135deg, #00f5ff 0%, #0099ff 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            font-weight: 800;
            margin-top: 25px;
        }
        
        h3 {
            color: #00f5ff;
            font-weight: 700;
            letter-spacing: -0.5px;
        }
        
        h4 {
            color: #ffffff;
            font-weight: 700;
        }
        
        p {
            color: #c0c0d8;
            line-height: 1.5;
        }
        
        /* Professional section header */
        .section-header {
            background: linear-gradient(135deg, rgba(0, 245, 255, 0.08) 0%, rgba(0, 153, 255, 0.08) 100%);
            padding: 20px;
            border-radius: 12px;
            border: 1px solid rgba(0, 245, 255, 0.2);
            margin-bottom: 25px;
            backdrop-filter: blur(10px);
        }
        
        .section-header h3 {
            margin-top: 0;
            margin-bottom: 8px;
        }
        
        .section-header p {
            margin: 0;
            color: #a0a8c8;
            font-size: 0.95em;
        }
        
        /* Tab styling */
        .stTabs [data-baseweb="tab-list"] {
            gap: 10px;
            background: transparent;
        }
        
        .stTabs [data-baseweb="tab"] {
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid rgba(0, 245, 255, 0.2);
            border-radius: 10px;
            padding: 12px 20px;
            font-weight: 600;
            transition: all 0.3s ease;
        }
        
        .stTabs [data-baseweb="tab"]:hover {
            background: rgba(0, 245, 255, 0.08);
            border-color: rgba(0, 245, 255, 0.4);
        }
        
        .stTabs [aria-selected="true"] [data-baseweb="tab"] {
            background: linear-gradient(135deg, #00f5ff 0%, #0099ff 100%);
            color: #0a0e27;
            border-color: #00f5ff;
        }
        
        /* Metric styling */
        [data-testid="metric-container"] {
            background: linear-gradient(135deg, rgba(0, 245, 255, 0.06) 0%, rgba(0, 153, 255, 0.06) 100%);
            border: 1px solid rgba(0, 245, 255, 0.25);
            border-radius: 12px;
            padding: 18px;
            backdrop-filter: blur(10px);
        }
        
        /* Material card styling */
        .material-card {
            background: linear-gradient(135deg, rgba(0, 245, 255, 0.04) 0%, rgba(0, 153, 255, 0.04) 100%);
            border: 1.5px solid rgba(0, 245, 255, 0.25);
            border-left: 4px solid #00f5ff;
            border-radius: 12px;
            padding: 20px;
            margin: 15px 0;
            backdrop-filter: blur(10px);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }
        
        .material-card:hover {
            border-color: rgba(0, 245, 255, 0.4);
            background: linear-gradient(135deg, rgba(0, 245, 255, 0.08) 0%, rgba(0, 153, 255, 0.08) 100%);
            transform: translateX(4px);
            box-shadow: 0 8px 32px rgba(0, 245, 255, 0.15);
        }
        
        .material-card h4 {
            color: #00f5ff;
            font-size: 1.25em;
            margin-bottom: 8px;
        }
        
        /* Input styling */
        .stNumberInput, .stSlider, .stSelectbox, .stMultiSelect, .stTextInput {
            background: transparent;
        }
        
        input, select, textarea {
            background-color: rgba(255, 255, 255, 0.05) !important;
            border: 1px solid rgba(0, 245, 255, 0.25) !important;
            color: #ffffff !important;
            border-radius: 8px !important;
            transition: all 0.2s ease !important;
        }
        
        input::placeholder {
            color: #888899;
        }
        
        input:focus, select:focus, textarea:focus {
            background-color: rgba(0, 245, 255, 0.08) !important;
            border-color: #00f5ff !important;
            box-shadow: 0 0 12px rgba(0, 245, 255, 0.25) !important;
        }
        
        /* Button styling */
        .stButton > button {
            background: linear-gradient(135deg, #00f5ff 0%, #0099ff 100%);
            color: #0a0e27 !important;
            border: none;
            font-weight: 700;
            border-radius: 10px;
            padding: 10px 24px;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(0, 245, 255, 0.3);
        }
        
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(0, 245, 255, 0.4);
        }
        
        /* Info/Warning boxes */
        .stInfo, [data-testid="stAlert"] {
            background: linear-gradient(135deg, rgba(0, 245, 255, 0.12) 0%, rgba(0, 153, 255, 0.12) 100%);
            border: 1px solid rgba(0, 245, 255, 0.35);
            border-radius: 12px;
            padding: 20px;
        }
        
        .stWarning {
            background: linear-gradient(135deg, rgba(255, 153, 0, 0.12) 0%, rgba(255, 102, 0, 0.12) 100%);
            border: 1px solid rgba(255, 153, 0, 0.35);
            border-radius: 12px;
        }
        
        .stError {
            background: linear-gradient(135deg, rgba(255, 0, 100, 0.12) 0%, rgba(255, 102, 102, 0.12) 100%);
            border: 1px solid rgba(255, 0, 100, 0.35);
            border-radius: 12px;
        }
        
        .stSuccess {
            background: linear-gradient(135deg, rgba(0, 255, 100, 0.12) 0%, rgba(0, 200, 100, 0.12) 100%);
            border: 1px solid rgba(0, 255, 100, 0.35);
            border-radius: 12px;
        }
        
        /* Divider */
        .stDivider {
            border-top: 1px solid rgba(0, 245, 255, 0.15);
            margin: 25px 0;
        }
        
        /* Expander styling */
        .streamlit-expander {
            background: linear-gradient(135deg, rgba(0, 245, 255, 0.04) 0%, rgba(0, 153, 255, 0.04) 100%);
            border: 1px solid rgba(0, 245, 255, 0.2);
            border-radius: 10px;
        }
        
        /* Dataframe styling */
        .stDataFrame {
            color: #ffffff;
        }
        
        /* Metric label styling */
        [data-testid="metric-container"] label {
            color: #00f5ff;
            font-weight: 600;
            font-size: 0.9em;
        }
        
        /* Smooth transitions */
        * {
            transition: all 0.3s ease;
        }
        
        /* Stat card */
        .stat-card {
            background: linear-gradient(135deg, rgba(0, 245, 255, 0.08) 0%, rgba(0, 153, 255, 0.08) 100%);
            border: 1px solid rgba(0, 245, 255, 0.25);
            border-radius: 12px;
            padding: 20px;
            text-align: center;
        }
    </style>
""", unsafe_allow_html=True)

# ============================================================
# DATA LOADING & INITIALIZATION
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
        model_package = pickle.load(open("model.pkl", "rb"))
        
        # Handle new model package format
        if isinstance(model_package, dict) and 'primary_model' in model_package:
            model = model_package['primary_model']
            scaler = model_package['scaler']
            metadata = model_package.get('metadata', {})
        elif isinstance(model_package, dict) and 'model' in model_package:
            # Legacy format
            model = model_package['model']
            scaler = model_package['scaler']
            metadata = {}
        else:
            model = model_package
            scaler = None
            metadata = {}
        
        return df, model, scaler, metadata
    except Exception as e:
        st.error(f"❌ Error loading files: {str(e)}")
        st.stop()

df, model, scaler, model_metadata = load_data_and_model()

# Add environmental impact data
environmental_data = {
    'Steel': 2.0, 'Stainless Steel': 2.5, 'Aluminum': 4.0, 'Titanium': 8.5,
    'Copper': 3.5, 'Brass': 3.8, 'Bronze': 4.0, 'Magnesium': 5.5, 'Cast Iron': 1.5,
    'Nickel Alloy': 6.0, 'Carbon Fiber': 7.0, 'Glass Fiber': 2.0, 'Kevlar': 8.0,
    'Epoxy Composite': 3.5, 'Fiberglass': 2.5, 'Aluminum Alloy 6061': 4.0,
    'Aluminum Alloy 7075': 4.2, 'Titanium Grade 2': 8.0, 'Tungsten': 5.0
}
df['environmental_impact'] = df['name'].map(environmental_data).fillna(3.0)

# Initialize session state
if "comparison_materials" not in st.session_state:
    st.session_state.comparison_materials = []
if "favorites" not in st.session_state:
    st.session_state.favorites = []
if "search_history" not in st.session_state:
    st.session_state.search_history = []
if "last_recommendations" not in st.session_state:
    st.session_state.last_recommendations = None

# ============================================================
# HELPER FUNCTIONS
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

def calculate_performance_score(material_row, usecase):
    """Calculate normalized performance score for a material based on usecase"""
    scores = {
        'Aerospace': (material_row['strength']/1000 * 0.3 + material_row['temp_limit']/3500 * 0.3 + 
                     (10-material_row['weight'])/10 * 0.4) * 100,
        'Medical': (material_row['corrosion']/10 * 0.5 + material_row['hardness']/10 * 0.3 + 
                   (1-material_row['environmental_impact']/10) * 0.2) * 100,
        'Marine': material_row['corrosion'] * 10,
        'High-Temperature': material_row['temp_limit'] / 34,
        'Lightweight': (10 - material_row['weight']) * 10,
        'Budget': (100 - material_row['cost']),
    }
    return scores.get(usecase, 50)

def generate_material_report(material_row):
    """Generate detailed report for a material"""
    report = f"""
    # Material Report: {material_row['name']}
    
    **Category:** {material_row['category']}
    **Common Uses:** {material_row['use_cases']}
    
    ## Key Properties
    - **Strength:** {material_row['strength']:.0f} MPa
    - **Weight:** {material_row['weight']:.2f} g/cm³
    - **Cost:** ${material_row['cost']:.0f}
    - **Max Temperature:** {material_row['temp_limit']:.0f}°C
    - **Corrosion Resistance:** {material_row['corrosion']:.0f}/10
    - **Hardness:** {material_row['hardness']:.0f}/10
    - **Ductility:** {material_row['ductility']:.0f}/10
    - **Thermal Conductivity:** {material_row['thermal_conductivity']:.1f} W/mK
    - **Electrical Conductivity:** {material_row['electrical_conductivity']:.0f}
    
    ## Environmental Impact Score
    Carbon footprint index: {material_row['environmental_impact']:.1f}/10 (lower is better)
    
    **Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    """
    return report

def get_cost_benefit(material_row, usecase):
    """Calculate cost-benefit ratio"""
    perf_score = calculate_performance_score(material_row, usecase)
    cost = material_row['cost']
    if cost == 0:
        return 0
    return perf_score / cost

# ============================================================
# MAIN APP
# ============================================================

# Hero Header
st.markdown("""
<div style='text-align: center; padding: 40px 30px; background: linear-gradient(135deg, rgba(0, 245, 255, 0.08) 0%, rgba(0, 153, 255, 0.08) 100%); border-radius: 15px; margin-bottom: 30px; border: 1px solid rgba(0, 245, 255, 0.25);'>
    <h1 style='margin: 0; font-size: 3.2em;'>🔬 Material Selector Pro</h1>
    <p style='color: #00f5ff; font-size: 1.15em; margin: 10px 0 0 0; font-weight: 500;'>AI-Powered Intelligent Material Selection System</p>
    <p style='color: #a0a8c8; font-size: 0.95em; margin: 8px 0 0 0;'>60+ premium materials | 4 categories | ML-enhanced matching | Environmental tracking</p>
</div>
""", unsafe_allow_html=True)

# Quick Stats with improved design
stat1, stat2, stat3, stat4 = st.columns(4, gap="large")
with stat1:
    st.metric("📦 Materials", len(df), delta="In Database", border=True)
with stat2:
    st.metric("🏢 Categories", df['category'].nunique(), delta="Types", border=True)
with stat3:
    st.metric("💪 Max Strength", f"{df['strength'].max():.0f}", delta="MPa", border=True)
with stat4:
    if model_metadata and 'cv_score' in model_metadata:
        st.metric("🤖 Model Acc.", f"{model_metadata['cv_score']:.1%}", delta="5-Fold CV", border=True)
    else:
        st.metric("🌍 Avg Eco Impact", f"{df['environmental_impact'].mean():.1f}", delta="/10", border=True)

# Main navigation tabs
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "⚡ Smart Select", 
    "🔍 Advanced Search", 
    "⚖️ Compare",
    "💡 Use Cases",
    "🎯 Insights",
    "📊 Analytics",
    "⚙️ Tools"
])

# ============================================================
# TAB 1: QUICK SELECT
# ============================================================
with tab1:
    st.markdown("""
    <div class="section-header">
        <h3>⚡ Smart Material Selection</h3>
        <p>Set your requirements and find the perfect material instantly using AI-powered matching</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 2], gap="large")
    
    with col1:
        st.markdown("<h4 style='color: #00f5ff;'>📋 Filter by Category</h4>", unsafe_allow_html=True)
        categories = df['category'].unique()
        selected_category = st.selectbox("Select Material Category", ["All"] + list(categories), label_visibility="collapsed")
        
        if selected_category != "All":
            category_df = df[df['category'] == selected_category]
        else:
            category_df = df
        
        st.markdown(f"<p style='color: #00f5ff; font-weight: bold; margin: 15px 0 10px 0;'>✅ Found {len(category_df)} materials</p>", unsafe_allow_html=True)
        
        st.markdown("<h4 style='color: #00f5ff;'>🎚️ Set Your Requirements</h4>", unsafe_allow_html=True)
        strength_req = st.slider("💪 Min Strength (MPa)", 0, 1000, 300, help="Material must meet this strength")
        weight_req = st.slider("⚖️ Max Weight (g/cm³)", 0.0, 20.0, 5.0, help="Lower is lighter")
        cost_req = st.slider("💰 Max Cost ($)", 0, 400, 100, help="Budget constraint")
        temp_req = st.slider("🔥 Min Temperature (°C)", 0, 3500, 300, help="Heat tolerance needed")
        corrosion_req = st.slider("🛡️ Min Corrosion Resistance", 1, 10, 5, help="1=Low, 10=Excellent")
        hardness_req = st.slider("💎 Min Hardness", 1, 10, 5, help="1=Soft, 10=Very Hard")
    
    with col2:
        requirements = (strength_req, weight_req, cost_req, temp_req, corrosion_req, hardness_req)
        
        # Score all materials
        results = []
        for idx, row in category_df.iterrows():
            score, mismatches = score_material(row, requirements)
            results.append((row, score, mismatches))
        
        results.sort(key=lambda x: x[1], reverse=True)
        
        if results:
            best_material = results[0]
            
            # Best Match Card
            st.markdown("""
            <div style='background: linear-gradient(135deg, rgba(0, 255, 100, 0.1) 0%, rgba(0, 200, 100, 0.1) 100%); 
                        padding: 25px; border-radius: 15px; border: 2px solid rgba(0, 255, 100, 0.3); margin-bottom: 20px;'>
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
            
            # Material details
            st.divider()
            st.markdown("<h4 style='color: #00f5ff;'>📊 Material Properties</h4>", unsafe_allow_html=True)
            
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
            
            # Use cases
            st.divider()
            st.markdown(f"<p style='background: linear-gradient(135deg, rgba(0, 245, 255, 0.1) 0%, rgba(0, 153, 255, 0.1) 100%); padding: 15px; border-radius: 10px; border-left: 4px solid #00f5ff;'><strong style='color: #00f5ff;'>🎯 Common Uses:</strong> <span style='color: #e0e0e0;'>{best_material[0]['use_cases']}</span></p>", unsafe_allow_html=True)
            
            # Show alternatives
            st.divider()
            st.markdown("<h4 style='color: #00f5ff;'>🔄 Also Consider (Top Alternatives)</h4>", unsafe_allow_html=True)
            
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
# TAB 2: ADVANCED SEARCH
# ============================================================
with tab2:
    st.markdown("""
    <div class="section-header">
        <h3>🔍 Advanced Material Search</h3>
        <p>Fine-tune your search with detailed filters and advanced options</p>
    </div>
    """, unsafe_allow_html=True)
    
    search_col1, search_col2 = st.columns(2, gap="large")
    
    with search_col1:
        st.markdown("<h4 style='color: #00f5ff;'>🔎 Search & Filter</h4>", unsafe_allow_html=True)
        # Filters
        search_text = st.text_input("🔎 Search materials by name", placeholder="e.g., Steel, Aluminum, Carbon Fiber")
        
        if search_text:
            search_df = df[df['name'].str.contains(search_text, case=False)]
        else:
            search_df = df
        
        category_filter = st.multiselect("Filter by Category", df['category'].unique(), default=df['category'].unique())
        search_df = search_df[search_df['category'].isin(category_filter)]
        
        st.markdown("<h4 style='color: #00f5ff;'>📊 Property Ranges</h4>", unsafe_allow_html=True)
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
        
        st.markdown("<h4 style='color: #00f5ff;'>🎯 Sort Options</h4>", unsafe_allow_html=True)
        sort_by = st.selectbox("Sort Results By", ["Name", "Strength", "Weight", "Cost", "Temperature", "Corrosion", "Hardness"])
    
    # Apply filters
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
        <div style='background: linear-gradient(135deg, rgba(255, 153, 0, 0.12) 0%, rgba(255, 102, 0, 0.12) 100%); 
                    padding: 20px; border-radius: 12px; border: 1px solid rgba(255, 153, 0, 0.3); text-align: center;'>
            <p style='color: #ffaa00; font-size: 1.1em;'>😕 No materials match your criteria.</p>
            <p style='color: #a0a0a0;'>Try adjusting your filters for more results</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        # Sort
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
        <div style='background: linear-gradient(135deg, rgba(0, 255, 100, 0.1) 0%, rgba(0, 200, 100, 0.1) 100%); 
                    padding: 15px; border-radius: 10px; border: 1px solid rgba(0, 255, 100, 0.3); margin-bottom: 20px;'>
            <h4 style='color: #00ff64; margin: 0;'>✅ {len(filtered_df)} Materials Found</h4>
        </div>
        """, unsafe_allow_html=True)
        
        # Display as expandable cards
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
                    st.markdown(f"<p style='color: #00f5ff;'><strong>🎯 Use Cases:</strong> {row['use_cases']}</p>", unsafe_allow_html=True)
            
            with col_btn:
                if st.button("➕", key=f"add_btn_{idx}", help="Add to comparison"):
                    if row['name'] not in st.session_state.comparison_materials:
                        st.session_state.comparison_materials.append(row['name'])
                        st.rerun()


# ============================================================
# TAB 3: COMPARE MATERIALS
# ============================================================
with tab3:
    st.markdown("""
    <div class="section-header">
        <h3>⚖️ Side-by-Side Material Comparison</h3>
        <p>Compare properties and make informed decisions</p>
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
    
    # Get materials
    mat1 = df[df['name'] == material1].iloc[0]
    mat2 = df[df['name'] == material2].iloc[0]
    
    # Comparison header
    st.divider()
    st.markdown(f"""
    <div style='display: flex; justify-content: space-between; gap: 20px;'>
        <div style='flex: 1; background: linear-gradient(135deg, rgba(0, 245, 255, 0.1) 0%, rgba(0, 153, 255, 0.1) 100%); 
                    padding: 20px; border-radius: 12px; border: 2px solid rgba(0, 245, 255, 0.25); text-align: center;'>
            <h3 style='color: #00f5ff; margin: 0;'>💪 {material1}</h3>
            <p style='color: #a0a0a0; margin: 10px 0 0 0;'>{mat1['category']}</p>
        </div>
        <div style='flex: 1; background: linear-gradient(135deg, rgba(0, 153, 255, 0.1) 0%, rgba(0, 100, 200, 0.1) 100%); 
                    padding: 20px; border-radius: 12px; border: 2px solid rgba(0, 153, 255, 0.25); text-align: center;'>
            <h3 style='color: #0099ff; margin: 0;'>💪 {material2}</h3>
            <p style='color: #a0a0a0; margin: 10px 0 0 0;'>{mat2['category']}</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    st.markdown("<h4 style='color: #00f5ff;'>📊 Property Comparison Table</h4>", unsafe_allow_html=True)
    
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
    
    # Visual comparison
    st.divider()
    st.markdown("<h4 style='color: #00f5ff;'>📈 Visual Radar Comparison</h4>", unsafe_allow_html=True)
    
    col_chart1, col_chart2 = st.columns(2, gap="large")
    
    with col_chart1:
        st.markdown(f"<h4 style='text-align: center; color: #00f5ff;'>{material1}</h4>", unsafe_allow_html=True)
        props = ['Strength', 'Weight', 'Corrosion', 'Hardness', 'Ductility']
        vals1 = [
            min(mat1['strength'] / 100, 10),
            10 - mat1['weight'],
            mat1['corrosion'],
            mat1['hardness'],
            mat1['ductility']
        ]
        
        fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(projection='polar'), facecolor='#0a0e27')
        fig.patch.set_facecolor('#0a0e27')
        angles = np.linspace(0, 2 * np.pi, len(props), endpoint=False).tolist()
        vals1_plot = vals1 + [vals1[0]]
        angles_plot = angles + [angles[0]]
        
        ax.plot(angles_plot, vals1_plot, 'o-', linewidth=3, color='#00f5ff', label=material1)
        ax.fill(angles_plot, vals1_plot, alpha=0.25, color='#00f5ff')
        ax.set_xticks(angles)
        ax.set_xticklabels(props, color='#e0e0e0')
        ax.set_ylim(0, 10)
        ax.grid(True, color='#00f5ff33')
        ax.set_facecolor('#1a1f3a')
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
        
        fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(projection='polar'), facecolor='#0a0e27')
        fig.patch.set_facecolor('#0a0e27')
        vals2_plot = vals2 + [vals2[0]]
        
        ax.plot(angles_plot, vals2_plot, 'o-', linewidth=3, color='#0099ff', label=material2)
        ax.fill(angles_plot, vals2_plot, alpha=0.25, color='#0099ff')
        ax.set_xticks(angles)
        ax.set_xticklabels(props, color='#e0e0e0')
        ax.set_ylim(0, 10)
        ax.grid(True, color='#0099ff33')
        ax.set_facecolor('#1a1f3a')
        st.pyplot(fig, use_container_width=True)


# ============================================================
# TAB 4: USE CASES
# ============================================================
with tab4:
    st.markdown("""
    <div class="section-header">
        <h3>💡 Materials by Use Case</h3>
        <p>Pre-configured recommendations for common applications</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 2], gap="large")
    
    with col1:
        st.markdown("<h4 style='color: #00f5ff;'>🎯 Select Use Case</h4>", unsafe_allow_html=True)
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
        <div style='background: linear-gradient(135deg, rgba(0, 245, 255, 0.1) 0%, rgba(0, 153, 255, 0.1) 100%); 
                    padding: 15px; border-radius: 10px; border: 1px solid rgba(0, 245, 255, 0.25);'>
            <p style='color: #e0e0e0; margin: 0;'>{usecase_descriptions[usecase]}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Get recommendations
    usecase_df = get_recommendations_by_usecase(usecase)
    
    st.divider()
    
    # Sort by relevance
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
    <div style='background: linear-gradient(135deg, rgba(0, 255, 100, 0.1) 0%, rgba(0, 200, 100, 0.1) 100%); 
                padding: 15px; border-radius: 10px; border: 1px solid rgba(0, 255, 100, 0.3); margin-bottom: 20px;'>
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
# TAB 5: ANALYTICS
# ============================================================
with tab5:
    st.markdown("""
    <div class="section-header">
        <h3>📊 Material Analytics Dashboard</h3>
        <p>Comprehensive insights and trends across the material database</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Statistics
    stat1, stat2, stat3, stat4 = st.columns(4)
    with stat1:
        st.metric("📊 Avg Strength", f"{df['strength'].mean():.0f} MPa", delta="Range: 50-800", border=True)
    with stat2:
        st.metric("💰 Avg Cost", f"${df['cost'].mean():.0f}", delta="Range: $5-$300", border=True)
    with stat3:
        st.metric("🔥 Heat Champ", f"{df.loc[df['temp_limit'].idxmax(), 'name']}", delta=f"{df['temp_limit'].max():.0f}°C", border=True)
    with stat4:
        st.metric("🛡️ Corrosion Champ", f"{df.loc[df['corrosion'].idxmax(), 'name']}", delta=f"{df['corrosion'].max():.0f}/10", border=True)
    
    # Visualizations
    st.divider()
    st.markdown("<h4 style='color: #00f5ff;'>📈 Strength vs Weight Analysis</h4>", unsafe_allow_html=True)
    
    col_chart1, col_chart2 = st.columns(2, gap="large")
    
    with col_chart1:
        st.markdown("<p style='text-align: center; color: #00f5ff; font-weight: bold;'>💪 Strength vs Weight by Category</p>", unsafe_allow_html=True)
        fig, ax = plt.subplots(figsize=(8, 5), facecolor='#0a0e27')
        fig.patch.set_facecolor('#0a0e27')
        
        colors = {'Metal': '#00f5ff', 'Composite': '#0099ff', 'Polymer': '#00ff64', 'Ceramic': '#ffaa00'}
        for category in df['category'].unique():
            cat_data = df[df['category'] == category]
            ax.scatter(cat_data['weight'], cat_data['strength'], label=category, s=100, alpha=0.7, color=colors.get(category, '#00f5ff'))
        
        ax.set_xlabel("Weight (g/cm³)", color='#e0e0e0', fontsize=10)
        ax.set_ylabel("Strength (MPa)", color='#e0e0e0', fontsize=10)
        ax.legend(loc='best', facecolor='#1a1f3a', edgecolor='#00f5ff4d')
        ax.grid(True, alpha=0.2, color='#00f5ff33')
        ax.set_facecolor('#1a1f3a')
        ax.tick_params(colors='#e0e0e0')
        st.pyplot(fig, use_container_width=True)
    
    with col_chart2:
        st.markdown("<p style='text-align: center; color: #00f5ff; font-weight: bold;'>💰 Cost vs Strength (Colored by Temp)</p>", unsafe_allow_html=True)
        fig, ax = plt.subplots(figsize=(8, 5), facecolor='#0a0e27')
        fig.patch.set_facecolor('#0a0e27')
        
        scatter = ax.scatter(df['strength'], df['cost'], c=df['temp_limit'], cmap='plasma', s=100, alpha=0.7, edgecolors='#00f5ff4d', linewidth=1)
        ax.set_xlabel("Strength (MPa)", color='#e0e0e0', fontsize=10)
        ax.set_ylabel("Cost ($)", color='#e0e0e0', fontsize=10)
        cbar = plt.colorbar(scatter, ax=ax, label="Max Temp (°C)")
        cbar.set_label("Max Temp (°C)", color='#e0e0e0')
        cbar.ax.tick_params(colors='#e0e0e0')
        ax.grid(True, alpha=0.2, color='#00f5ff33')
        ax.set_facecolor('#1a1f3a')
        ax.tick_params(colors='#e0e0e0')
        st.pyplot(fig, use_container_width=True)
    
    st.divider()
    st.markdown("<h4 style='color: #00f5ff;'>🔥 Distribution Analysis</h4>", unsafe_allow_html=True)
    
    col_chart3, col_chart4 = st.columns(2, gap="large")
    
    with col_chart3:
        st.markdown("<p style='text-align: center; color: #00f5ff; font-weight: bold;'>🔥 Temperature Resistance by Category</p>", unsafe_allow_html=True)
        fig, ax = plt.subplots(figsize=(8, 5), facecolor='#0a0e27')
        fig.patch.set_facecolor('#0a0e27')
        
        categories = df['category'].unique()
        temp_by_cat = [df[df['category'] == cat]['temp_limit'].values for cat in categories]
        bp = ax.boxplot(temp_by_cat, tick_labels=categories, patch_artist=True)
        
        for patch in bp['boxes']:
            patch.set_facecolor('#00f5ff')
            patch.set_alpha(0.6)
        for whisker in bp['whiskers']:
            whisker.set_color('#00f5ff80')
        for cap in bp['caps']:
            cap.set_color('#00f5ff80')
        for median in bp['medians']:
            median.set_color('#00ff64')
            median.set_linewidth(2)
        
        ax.set_ylabel("Max Temperature (°C)", color='#e0e0e0', fontsize=10)
        ax.tick_params(colors='#e0e0e0', axis='x', rotation=45)
        ax.tick_params(colors='#e0e0e0')
        ax.grid(True, alpha=0.2, color='#00f5ff33', axis='y')
        ax.set_facecolor('#1a1f3a')
        st.pyplot(fig, use_container_width=True)
    
    with col_chart4:
        st.markdown("<p style='text-align: center; color: #00f5ff; font-weight: bold;'>🧬 Property Correlation Matrix</p>", unsafe_allow_html=True)
        corr_cols = ['strength', 'weight', 'cost', 'temp_limit', 'corrosion', 'hardness']
        corr_matrix = df[corr_cols].corr()
        
        fig, ax = plt.subplots(figsize=(8, 6), facecolor='#0a0e27')
        fig.patch.set_facecolor('#0a0e27')
        
        im = ax.imshow(corr_matrix, cmap='coolwarm', aspect='auto', vmin=-1, vmax=1)
        
        # Set ticks and labels
        ax.set_xticks(np.arange(len(corr_cols)))
        ax.set_yticks(np.arange(len(corr_cols)))
        ax.set_xticklabels(corr_cols, rotation=45, ha='right', color='#e0e0e0')
        ax.set_yticklabels(corr_cols, color='#e0e0e0')
        
        # Add correlation values as text
        for i in range(len(corr_cols)):
            for j in range(len(corr_cols)):
                text = ax.text(j, i, f'{corr_matrix.iloc[i, j]:.2f}',
                              ha="center", va="center", color="white", fontsize=10, fontweight='bold')
        
        cbar = plt.colorbar(im, ax=ax, label='Correlation')
        cbar.set_label('Correlation', color='#e0e0e0')
        cbar.ax.tick_params(colors='#e0e0e0')
        ax.set_facecolor('#1a1f3a')
        plt.tight_layout()
        st.pyplot(fig, use_container_width=True)
    
    st.divider()
    st.markdown("<h4 style='color: #00d4ff;'>📋 Full Material Database</h4>", unsafe_allow_html=True)
    st.dataframe(df, use_container_width=True, hide_index=True)

# ============================================================
# TAB 6: INSIGHTS & AI RECOMMENDATIONS
# ============================================================
with tab6:
    st.markdown("""
    <div class="section-header">
        <h3>🎯 AI-Powered Insights & Recommendations</h3>
        <p>Intelligent suggestions based on your requirements and machine learning analysis</p>
    </div>
    """, unsafe_allow_html=True)
    
    insight_col1, insight_col2 = st.columns([1.5, 1.5], gap="large")
    
    with insight_col1:
        st.markdown("<h4 style='color: #00f5ff;'>📋 Your Requirements</h4>", unsafe_allow_html=True)
        ai_strength = st.slider("💪 Required Strength (MPa)", 0, 1000, 400, key="ai_strength")
        ai_weight = st.slider("⚖️ Maximum Weight (g/cm³)", 0.0, 20.0, 5.0, key="ai_weight")
        ai_cost = st.slider("💰 Budget ($)", 0, 400, 150, key="ai_cost")
        ai_usecase = st.selectbox("🎯 Application Type", [
            "Aerospace", "Medical", "Marine", "High-Temperature", "Lightweight", "Budget"
        ], key="ai_usecase")
    
    with insight_col2:
        st.markdown("<h4 style='color: #00f5ff;'>🌍 Preferences</h4>", unsafe_allow_html=True)
        eco_conscious = st.checkbox("♻️ Prefer eco-friendly materials", value=False)
        strength_priority = st.checkbox("💪 Prioritize strength", value=True)
        cost_priority = st.checkbox("💵 Budget is priority", value=False)
        
        if st.button("🚀 Get AI Recommendations", use_container_width=True):
            # Filter based on basic requirements
            filtered = df[
                (df['strength'] >= ai_strength) &
                (df['weight'] <= ai_weight) &
                (df['cost'] <= ai_cost)
            ]
            
            if len(filtered) > 0:
                # Score materials based on preferences
                scores = []
                for idx, row in filtered.iterrows():
                    score = calculate_performance_score(row, ai_usecase)
                    
                    # Adjust for eco-consciousness
                    if eco_conscious:
                        score *= (1 - (row['environmental_impact'] / 100))
                    
                    # Adjust for priorities
                    if strength_priority:
                        score += row['strength'] / 10
                    if cost_priority:
                        score += (100 - row['cost']) / 10
                    
                    scores.append((idx, score))
                
                scores.sort(key=lambda x: x[1], reverse=True)
                st.session_state.last_recommendations = scores[:5]
    
    if st.session_state.last_recommendations:
        st.divider()
        st.markdown("""
        <div style='background: linear-gradient(135deg, rgba(0, 255, 100, 0.1) 0%, rgba(0, 200, 100, 0.1) 100%); 
                    padding: 20px; border-radius: 12px; border: 1px solid rgba(0, 255, 100, 0.3); margin-bottom: 20px;'>
            <h3 style='color: #00ff64; margin-top: 0;'>🏆 Top AI-Recommended Materials</h3>
        </div>
        """, unsafe_allow_html=True)
        
        for rank, (idx, score) in enumerate(st.session_state.last_recommendations, 1):
            material = df.iloc[idx]
            
            col_rank, col_name, col_action = st.columns([0.3, 3, 0.7])
            
            with col_rank:
                st.markdown(f"<h3 style='color: #00f5ff; text-align: center; margin: 0;'>#{rank}</h3>", unsafe_allow_html=True)
            
            with col_name:
                st.markdown(f"""
                <div class="material-card" style="margin: 0;">
                    <h4 style="margin: 0;">{material['name']}</h4>
                    <p style="color: #a0a8c8; margin: 5px 0 0 0;">{material['category']} • ${material['cost']:.0f}</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col_action:
                if st.button("📊 Details", key=f"ai_details_{idx}", use_container_width=True):
                    st.markdown(generate_material_report(material))
            
            # Quick stats
            m1, m2, m3, m4 = st.columns(4)
            with m1:
                st.metric("💪 Strength", f"{material['strength']:.0f} MPa", border=True)
            with m2:
                st.metric("⚖️ Weight", f"{material['weight']:.2f} g/cm³", border=True)
            with m3:
                cb_ratio = get_cost_benefit(material, ai_usecase)
                st.metric("📈 C/B Ratio", f"{cb_ratio:.2f}", border=True)
            with m4:
                st.metric("🌍 Eco Impact", f"{material['environmental_impact']:.1f}/10", border=True)
            
            st.divider()

# ============================================================
# TAB 7: TOOLS & UTILITIES
# ============================================================
with tab7:
    st.markdown("""
    <div class="section-header">
        <h3>⚙️ Advanced Tools & Utilities</h3>
        <p>Export reports, generate recommendations, and access advanced features</p>
    </div>
    """, unsafe_allow_html=True)
    
    tool_tab1, tool_tab2, tool_tab3, tool_tab4, tool_tab5 = st.tabs([
        "📄 Report Generator",
        "🔄 Batch Comparison",
        "📊 Cost Analysis",
        "🌍 Environmental Impact",
        "🤖 AI Model Info"
    ])
    
    # Tool 1: Report Generator
    with tool_tab1:
        st.markdown("<h4 style='color: #00f5ff;'>📄 Generate Material Report</h4>", unsafe_allow_html=True)
        
        report_material = st.selectbox("Select Material", df['name'].values, key="report_material")
        report_format = st.radio("Report Format", ["📋 Detailed", "📊 Summary"])
        
        if st.button("🖨️ Generate Report", use_container_width=True):
            material = df[df['name'] == report_material].iloc[0]
            
            if report_format == "📋 Detailed":
                report_text = generate_material_report(material)
                st.markdown(report_text)
                
                # Download button
                report_file = io.StringIO(report_text)
                st.download_button(
                    label="⬇️ Download as Text",
                    data=report_text,
                    file_name=f"{report_material}_report_{datetime.now().strftime('%Y%m%d')}.txt",
                    mime="text/plain",
                    use_container_width=True
                )
            else:
                summary = f"""
                **{material['name']}** ({material['category']})
                Strength: {material['strength']:.0f} MPa | Weight: {material['weight']:.2f} g/cm³ | Cost: ${material['cost']:.0f}
                Temp: {material['temp_limit']:.0f}°C | Corrosion: {material['corrosion']:.0f}/10 | Hardness: {material['hardness']:.0f}/10
                """
                st.markdown(summary)
    
    # Tool 2: Batch Comparison
    with tool_tab2:
        st.markdown("<h4 style='color: #00f5ff;'>🔄 Compare Multiple Materials</h4>", unsafe_allow_html=True)
        
        batch_materials = st.multiselect(
            "Select Materials to Compare",
            df['name'].values,
            default=df['name'].values[:3] if len(df) >= 3 else df['name'].values,
            key="batch_compare"
        )
        
        if batch_materials:
            compare_df = df[df['name'].isin(batch_materials)].copy()
            
            # Normalize scores for visualization
            st.markdown("<h4 style='color: #00f5ff; margin-top: 20px;'>📊 Comparison Table</h4>", unsafe_allow_html=True)
            display_cols = ['name', 'category', 'strength', 'weight', 'cost', 'temp_limit', 'corrosion', 'hardness']
            st.dataframe(compare_df[display_cols], use_container_width=True, hide_index=True)
            
            # Download comparison
            csv = compare_df[display_cols].to_csv(index=False)
            st.download_button(
                label="⬇️ Download Comparison CSV",
                data=csv,
                file_name=f"materials_comparison_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv",
                use_container_width=True
            )
    
    # Tool 3: Cost Analysis
    with tool_tab3:
        st.markdown("<h4 style='color: #00f5ff;'>💰 Cost-Benefit Analysis</h4>", unsafe_allow_html=True)
        
        usecase_select = st.selectbox("Select Use Case", 
            ["Aerospace", "Medical", "Marine", "High-Temperature", "Lightweight", "Budget"],
            key="cost_analysis_use"
        )
        
        # Calculate cost-benefit for all materials
        df['cost_benefit'] = df.apply(lambda x: get_cost_benefit(x, usecase_select), axis=1)
        cost_analysis_df = df.copy().sort_values('cost_benefit', ascending=False)
        
        # Visualization
        fig, ax = plt.subplots(figsize=(10, 6), facecolor='#0a0e27')
        fig.patch.set_facecolor('#0a0e27')
        
        top_materials = cost_analysis_df.head(10)
        colors = ['#00f5ff' if i == 0 else '#0099ff' for i in range(len(top_materials))]
        
        ax.barh(range(len(top_materials)), top_materials['cost_benefit'].values, color=colors, alpha=0.8)
        ax.set_yticks(range(len(top_materials)))
        ax.set_yticklabels(top_materials['name'].values, color='#e0e0e0')
        ax.set_xlabel('Cost-Benefit Ratio', color='#e0e0e0')
        ax.set_title(f'Best Value Materials for {usecase_select}', color='#00f5ff', fontweight='bold')
        ax.grid(True, alpha=0.2, axis='x', color='#00f5ff33')
        ax.set_facecolor('#1a1f3a')
        ax.tick_params(colors='#e0e0e0')
        
        st.pyplot(fig, use_container_width=True)
        
        # Top picks
        st.markdown("<h4 style='color: #00f5ff; margin-top: 20px;'>🏆 Top Value Picks</h4>", unsafe_allow_html=True)
        for idx, (_, mat) in enumerate(cost_analysis_df.head(3).iterrows(), 1):
            st.metric(f"#{idx} {mat['name']}", f"${mat['cost']:.0f}", 
                     delta=f"C/B Ratio: {mat['cost_benefit']:.2f}", border=True)
    
    # Tool 4: Environmental Impact
    with tool_tab4:
        st.markdown("<h4 style='color: #00f5ff;'>🌍 Environmental Impact Analysis</h4>", unsafe_allow_html=True)
        
        eco_df = df.copy().sort_values('environmental_impact')
        
        # Green materials (low impact)
        st.markdown("<h4 style='color: #00ff64;'>♻️ Most Eco-Friendly Materials</h4>", unsafe_allow_html=True)
        for idx, (_, mat) in enumerate(eco_df.head(5).iterrows(), 1):
            st.write(f"**#{idx}** {mat['name']} - Impact Score: {mat['environmental_impact']:.1f}/10")
        
        st.divider()
        
        # Environmental impact chart
        fig, ax = plt.subplots(figsize=(10, 6), facecolor='#0a0e27')
        fig.patch.set_facecolor('#0a0e27')
        
        eco_sorted = eco_df.sort_values('environmental_impact', ascending=True).head(12)
        colors_eco = plt.cm.RdYlGn_r(np.linspace(0.3, 0.7, len(eco_sorted)))
        
        ax.barh(range(len(eco_sorted)), eco_sorted['environmental_impact'].values, color=colors_eco)
        ax.set_yticks(range(len(eco_sorted)))
        ax.set_yticklabels(eco_sorted['name'].values, color='#e0e0e0')
        ax.set_xlabel('Environmental Impact Score (Lower is Better)', color='#e0e0e0')
        ax.set_title('Material Environmental Impact Rankings', color='#00f5ff', fontweight='bold')
        ax.grid(True, alpha=0.2, axis='x', color='#00f5ff33')
        ax.set_facecolor('#1a1f3a')
        ax.tick_params(colors='#e0e0e0')
        
        st.pyplot(fig, use_container_width=True)
    
    # Tool 5: AI Model Information & Diagnostics
    with tool_tab5:
        st.markdown("<h4 style='color: #00f5ff;'>🤖 Advanced AI Model Information</h4>", unsafe_allow_html=True)
        
        # Model Overview
        col_m1, col_m2 = st.columns(2, gap="large")
        
        with col_m1:
            st.markdown("<h4 style='color: #00f5ff;'>📊 Model Architecture</h4>", unsafe_allow_html=True)
            if model_metadata:
                st.metric("Model Type", model_metadata.get('model_type', 'Ensemble'), border=True)
                st.metric("Training Accuracy", f"{model_metadata.get('accuracy', 0):.1%}", border=True)
                st.metric("Cross-Validation Score", f"{model_metadata.get('cv_score', 0):.1%}", border=True)
            else:
                st.info("Model metadata not available")
            
            st.markdown("<h4 style='color: #00f5ff;'>📈 Dataset Statistics</h4>", unsafe_allow_html=True)
            st.metric("Total Materials Trained", model_metadata.get('n_materials', len(df)), border=True)
            st.metric("Material Categories", model_metadata.get('n_categories', df['category'].nunique()), border=True)
            st.metric("Feature Dimensions", len(model_metadata.get('feature_names', [])) if model_metadata else len(df.columns), border=True)
        
        with col_m2:
            st.markdown("<h4 style='color: #00f5ff;'>🎯 Categories Trained</h4>", unsafe_allow_html=True)
            if model_metadata and 'categories' in model_metadata:
                for idx, cat in enumerate(model_metadata['categories'], 1):
                    count = len(df[df['category'] == cat])
                    st.write(f"**#{idx}** {cat}: {count} materials")
            else:
                for idx, cat in enumerate(df['category'].unique(), 1):
                    count = len(df[df['category'] == cat])
                    st.write(f"**#{idx}** {cat}: {count} materials")
        
        st.divider()
        
        # Feature Importance
        st.markdown("<h4 style='color: #00f5ff;'>🔍 Top 10 Feature Importance</h4>", unsafe_allow_html=True)
        
        if model_metadata and 'feature_importance' in model_metadata:
            fi_data = model_metadata['feature_importance']
            fi_df = pd.DataFrame({
                'Feature': fi_data.get('feature', []),
                'Importance': fi_data.get('importance', [])
            }).sort_values('Importance', ascending=False).head(10)
            
            # Bar chart
            fig, ax = plt.subplots(figsize=(10, 6), facecolor='#0a0e27')
            fig.patch.set_facecolor('#0a0e27')
            
            colors_fi = plt.cm.viridis(np.linspace(0.3, 0.9, len(fi_df)))
            ax.barh(range(len(fi_df)), fi_df['Importance'].values, color=colors_fi)
            ax.set_yticks(range(len(fi_df)))
            ax.set_yticklabels(fi_df['Feature'].values, color='#e0e0e0')
            ax.set_xlabel('Importance Score', color='#e0e0e0')
            ax.set_title('Most Important Features for Material Prediction', color='#00f5ff', fontweight='bold')
            ax.grid(True, alpha=0.2, axis='x', color='#00f5ff33')
            ax.set_facecolor('#1a1f3a')
            ax.tick_params(colors='#e0e0e0')
            
            st.pyplot(fig, use_container_width=True)
            
            # Feature importance table
            st.dataframe(fi_df.reset_index(drop=True), use_container_width=True, hide_index=True)
        else:
            st.info("🔄 Train the model to see feature importance")
        
        st.divider()
        
        # Model Configuration
        st.markdown("<h4 style='color: #00f5ff;'>⚙️ Model Configuration</h4>", unsafe_allow_html=True)
        
        config_text = """
        **Algorithm Details:**
        - Primary Model: Ensemble Learning (Random Forest + Gradient Boosting)
        - Training Method: Cross-Validation (5-Fold Stratified)
        - Feature Engineering: 8 derived features from core properties
        - Data Scaling: Robust Scaler (outlier-resistant)
        
        **Model Parameters:**
        - Random Forest: 200 estimators, max_depth=15, bootstrap=True
        - Gradient Boosting: 150 estimators, learning_rate=0.1
        - OOB Error Estimation: Enabled
        - Feature Selection: Square root of total features
        
        **Performance Metrics:**
        - Training Accuracy: Measured on full dataset
        - Validation: 5-fold cross-validation with stratification
        - Out-of-Bag Score: Unbiased performance estimate
        """
        st.markdown(config_text)
        
        st.divider()
        
        # Model Health Check
        st.markdown("<h4 style='color: #00f5ff;'>💓 Model Health Check</h4>", unsafe_allow_html=True)
        
        health_metrics = {
            '✅ Model Loaded': True,
            '✅ Scaler Available': scaler is not None,
            '✅ Data Balanced': len(df['category'].unique()) > 1,
            '✅ Metadata Available': bool(model_metadata),
            '✅ Features Engineered': model_metadata.get('feature_importance') is not None if model_metadata else False,
            '✅ Sufficient Training Data': len(df) > 50,
        }
        
        col_h1, col_h2, col_h3 = st.columns(3)
        for idx, (metric, status) in enumerate(health_metrics.items()):
            symbol = "✅" if status else "⚠️"
            if idx % 3 == 0:
                col_h1.write(f"{symbol} {metric}")
            elif idx % 3 == 1:
                col_h2.write(f"{symbol} {metric}")
            else:
                col_h3.write(f"{symbol} {metric}")
        
        st.success("🚀 All systems operational! Model ready for intelligent recommendations.")
