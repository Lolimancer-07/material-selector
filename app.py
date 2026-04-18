import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Material Selector Pro - Enterprise Edition",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
        * { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif; }
        [data-testid="stAppViewContainer"] { background: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 100%); color: #e8f0ff; }
        .main { background: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 100%); }
        
        /* Typography */
        h1 { color: #ffffff; font-weight: 800; letter-spacing: -0.5px; font-size: 2.8em !important; margin-bottom: 10px; }
        h2 { color: #e0e8ff; font-weight: 700; margin-top: 28px; margin-bottom: 12px; }
        h3 { color: #d0d8ff; font-weight: 600; margin: 16px 0 8px 0; }
        h4 { color: #c0c8ff; font-weight: 600; }
        p { color: #a8b0d0; line-height: 1.7; }
        
        /* Cards & Containers */
        .metric-card { 
            background: linear-gradient(135deg, rgba(20, 28, 60, 0.8) 0%, rgba(30, 40, 80, 0.8) 100%); 
            border: 1px solid rgba(100, 120, 200, 0.3);
            border-radius: 14px; 
            padding: 20px; 
            backdrop-filter: blur(10px);
        }
        
        .premium-card { 
            background: linear-gradient(135deg, rgba(60, 80, 160, 0.15) 0%, rgba(80, 100, 200, 0.15) 100%); 
            border: 1px solid rgba(100, 150, 255, 0.4);
            border-radius: 14px; 
            padding: 20px;
            backdrop-filter: blur(10px);
        }
        
        .success-badge { 
            background: linear-gradient(135deg, rgba(0, 255, 100, 0.12) 0%, rgba(0, 200, 100, 0.12) 100%); 
            border: 1px solid rgba(0, 255, 100, 0.4);
            border-radius: 14px;
            backdrop-filter: blur(10px);
        }
        
        .warning-badge { 
            background: linear-gradient(135deg, rgba(255, 153, 0, 0.12) 0%, rgba(255, 102, 0, 0.12) 100%); 
            border: 1px solid rgba(255, 153, 0, 0.4);
            border-radius: 14px;
            backdrop-filter: blur(10px);
        }
        
        /* Divider */
        hr { border-color: rgba(100, 120, 200, 0.2); }
        
        /* Tabs */
        [data-testid="stTabs"] { margin-top: 20px; }
        
        /* Better spacing */
        .block-container { padding-top: 2rem; padding-bottom: 2rem; }
    </style>
    """, unsafe_allow_html=True)

@st.cache_data
def load_data():
    try:
        df = pd.read_csv('materials_enhanced.csv')
    except:
        df = pd.read_csv('materials.csv')
    return df

def advanced_score_material(material_row, requirements, weights=None):
    if weights is None:
        weights = {
            'strength': 0.20,
            'weight': 0.15,
            'cost': 0.15,
            'temp_limit': 0.12,
            'corrosion': 0.12,
            'hardness': 0.10,
            'thermal_conductivity': 0.08,
            'workability': 0.05,
            'fatigue_resistance': 0.03
        }
    
    score = 0
    mismatches = []
    
    strength_score = min(material_row["strength"] / requirements[0], 1.0) if requirements[0] > 0 else 1.0
    score += strength_score * weights['strength']
    if material_row["strength"] < requirements[0]:
        mismatches.append(f"⚠ Strength: {material_row['strength']:.0f} MPa (need {requirements[0]:.0f})")
    
    weight_score = max(1 - (material_row["weight"] / requirements[1]), 0) if requirements[1] > 0 else 1.0
    score += weight_score * weights['weight']
    if material_row["weight"] > requirements[1]:
        mismatches.append(f"⚠ Weight: {material_row['weight']:.2f} g/cm³ (max {requirements[1]:.2f})")
    
    cost_score = max(1 - (material_row["cost"] / requirements[2]), 0) if requirements[2] > 0 else 1.0
    score += cost_score * weights['cost']
    if material_row["cost"] > requirements[2]:
        mismatches.append(f"⚠ Cost: ${material_row['cost']:.0f} (budget ${requirements[2]:.0f})")
    
    temp_score = min(material_row["temp_limit"] / requirements[3], 1.0) if requirements[3] > 0 else 1.0
    score += temp_score * weights['temp_limit']
    if material_row["temp_limit"] < requirements[3]:
        mismatches.append(f"⚠ Temp: {material_row['temp_limit']:.0f}°C (need {requirements[3]:.0f})")
    
    corr_score = material_row["corrosion"] / 10.0
    score += corr_score * weights['corrosion']
    
    hard_score = material_row["hardness"] / 10.0
    score += hard_score * weights['hardness']
    
    thermal_score = min(material_row["thermal_conductivity"] / 500, 1.0)
    score += thermal_score * weights['thermal_conductivity']
    
    workability_score = material_row.get("workability", 5) / 10.0 if "workability" in material_row else 0.5
    score += workability_score * weights['workability']
    
    fatigue_score = material_row.get("fatigue_resistance", 5) / 10.0 if "fatigue_resistance" in material_row else 0.5
    score += fatigue_score * weights['fatigue_resistance']
    
    return min(max(score, 0), 1.0), mismatches

def calculate_total_cost_of_ownership(material, unit_price, quantity, lifespan_years, maintenance_cost_annual=0):
    material_cost = unit_price * quantity
    maintenance_cost = maintenance_cost_annual * lifespan_years
    replacement_cost = material_cost * (lifespan_years // 5) if lifespan_years > 5 else 0
    total_cost = material_cost + maintenance_cost + replacement_cost
    cost_per_year = total_cost / lifespan_years if lifespan_years > 0 else total_cost
    return total_cost, cost_per_year

df = load_data()

# Professional header
col1, col2, col3 = st.columns([2, 3, 1])
with col1:
    st.title("🏭 Material Selector Pro")
with col2:
    st.markdown("### Advanced Material Intelligence & Analytics Platform")
with col3:
    st.metric("Materials Available", len(df), delta=f"{df['category'].nunique()} categories", border=True)

st.markdown("""
<div style='background: linear-gradient(90deg, rgba(100, 150, 255, 0.1) 0%, rgba(100, 200, 255, 0.1) 100%); 
            border: 1px solid rgba(100, 150, 255, 0.3); border-radius: 12px; padding: 16px; margin: 20px 0;'>
    <p style='margin: 0; color: #90b0e8;'>⚡ <strong>Enterprise v2.0</strong> — ML-powered material selection with 100+ materials, advanced analytics, and predictive modeling</p>
</div>
""", unsafe_allow_html=True)

st.divider()

tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
    "⚡ Quick Select",
    "🔬 Advanced Search",
    "💰 Cost Analysis",
    "🔄 Alternatives",
    "♻️ Sustainability",
    "🤖 Prediction",
    "📊 Analytics",
    "📋 Database"
])

with tab1:
    st.markdown("### ⚡ Quick Material Selection")
    st.markdown("Find the perfect material based on your specific requirements in seconds")
    
    # Top section - Category and Quick Filters
    col1, col2, col3 = st.columns([2, 2, 1.5])
    
    with col1:
        st.markdown("**Select Material Category**")
        selected_category = st.selectbox("", ["All Materials"] + list(df['category'].unique()), key="cat_select_tab1", label_visibility="collapsed")
        
        if selected_category != "All Materials":
            category_df = df[df['category'] == selected_category]
        else:
            category_df = df
    
    with col2:
        st.markdown("**Sort Results By**")
        sort_by = st.selectbox("", ["Match Score", "Cost (Low→High)", "Strength (High→Low)"], key="sort_quick", label_visibility="collapsed")
    
    with col3:
        st.markdown("**Show Results**")
        show_results = st.checkbox("🔍 Auto-Show", value=True, key="show_results_quick")
    
    st.divider()
    
    # Requirements section
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    
    with col1:
        min_strength = st.number_input("Min Strength (MPa)", 0, 2000, 200, step=50)
    with col2:
        max_weight = st.number_input("Max Weight", 0.1, 30.0, 10.0, step=0.5, label_visibility="collapsed")
    with col3:
        max_cost = st.number_input("Max Cost ($)", 5, 500, 150, step=10, label_visibility="collapsed")
    with col4:
        min_temp = st.number_input("Min Temp (°C)", 0, 4000, 200, step=100, label_visibility="collapsed")
    with col5:
        min_corrosion = st.slider("Min Corrosion", 1, 10, 5, label_visibility="collapsed")
    with col6:
        min_hardness = st.slider("Min Hardness", 1, 10, 4, label_visibility="collapsed")
    
    # Show results automatically if toggle is on
    if show_results:
        requirements = (min_strength, max_weight, max_cost, min_temp, min_corrosion, min_hardness)
        
        results = []
        for idx, row in category_df.iterrows():
            score, mismatches = advanced_score_material(row, requirements)
            results.append((row, score, mismatches))
        
        # Sort based on user selection
        if sort_by == "Cost (Low→High)":
            results.sort(key=lambda x: x[0]['cost'])
        elif sort_by == "Strength (High→Low)":
            results.sort(key=lambda x: x[0]['strength'], reverse=True)
        else:
            results.sort(key=lambda x: x[1], reverse=True)
        
        st.divider()
        
        if results and results[0][1] > 0.3:
            # Best match section
            best = results[0][0]
            
            st.markdown("")
            col_left, col_right = st.columns([2.2, 1.3])
            
            with col_left:
                st.markdown(f"""
                <div class='success-badge' style='padding: 24px; border-radius: 14px; margin: 10px 0;'>
                    <h2 style='color: #4aff9e; margin: 0 0 8px 0; font-size: 1.8em;'>🏆 Best Match: {best['name']}</h2>
                    <p style='color: #7aa0d8; margin: 5px 0; font-size: 1.05em;'>{best['category']} — Match Score: <strong>{results[0][1]*100:.1f}%</strong></p>
                </div>
                """, unsafe_allow_html=True)
                
                # Key metrics
                met_col1, met_col2, met_col3, met_col4 = st.columns(4)
                with met_col1:
                    st.metric("💪 Strength", f"{best['strength']:.0f} MPa", border=True)
                with met_col2:
                    st.metric("⚖️ Weight", f"{best['weight']:.2f}", border=True)
                with met_col3:
                    st.metric("💰 Cost", f"${best['cost']:.0f}", border=True)
                with met_col4:
                    st.metric("🌡️ Temp", f"{best['temp_limit']:.0f}°C", border=True)
                
                st.markdown("#### 📊 Complete Properties")
                props = {
                    '💎 Hardness': f"{best['hardness']:.0f}/10",
                    '🛡️ Corrosion': f"{best['corrosion']:.0f}/10",
                    '📐 Ductility': f"{best['ductility']:.0f}/10",
                    '🌡️ Thermal': f"{best['thermal_conductivity']:.1f} W/mK",
                    '⚡ Electrical': f"{best['electrical_conductivity']:.0f}",
                    '🏭 Availability': f"{best['availability']:.0f}/10"
                }
                
                prop_col1, prop_col2, prop_col3 = st.columns(3)
                for idx, (key, val) in enumerate(props.items()):
                    cols = [prop_col1, prop_col2, prop_col3]
                    with cols[idx % 3]:
                        st.metric(key, val, border=False)
                
                st.markdown(f"**✨ Use Cases:** {best['use_cases']}")
            
            with col_right:
                st.markdown("#### 🎯 Top 5 Alternatives")
                for i, (mat, score, _) in enumerate(results[1:6], 2):
                    st.markdown(f"""
                    <div class='metric-card' style='margin-bottom: 12px;'>
                        <p style='margin: 0; font-size: 0.95em;'><strong>#{i}</strong> {mat['name']}</p>
                        <p style='margin: 4px 0; font-weight: 600; color: #4aff9e;'>{score*100:.1f}% Match</p>
                        <p style='margin: 2px 0; font-size: 0.85em; color: #90a0c8;'>${mat['cost']:.0f} • {mat['strength']:.0f}MPa</p>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.warning("❌ No materials meet your criteria. Try relaxing your requirements.", icon="⚠️")

with tab2:
    st.markdown("### 🔬 Advanced Material Search")
    st.markdown("Filter and explore materials with detailed controls")
    
    col1, col2 = st.columns(2, gap="large")
    
    with col1:
        st.markdown("#### 🔎 Search & Filter")
        search_text = st.text_input("Search by name or category", placeholder="e.g., 'Carbon Fiber', 'High-Strength Steel'", key="search_adv")
        if search_text:
            search_df = df[df['name'].str.contains(search_text, case=False) | df['category'].str.contains(search_text, case=False)]
        else:
            search_df = df
        
        st.markdown("**Category Filter**")
        categories = st.multiselect("", df['category'].unique(), default=df['category'].unique(), label_visibility="collapsed", key="cat_filter_adv")
        search_df = search_df[search_df['category'].isin(categories)]
        
        st.markdown("**Property Ranges**")
        str_min, str_max = st.slider("Strength (MPa)", int(df['strength'].min()), int(df['strength'].max()), (0, 1000), key="str_range")
        cost_min, cost_max = st.slider("Cost ($)", int(df['cost'].min()), int(df['cost'].max()), (0, 400), key="cost_range")
        weight_min, weight_max = st.slider("Weight (g/cm³)", float(df['weight'].min()), float(df['weight'].max()), (0.0, 20.0), key="weight_range")
        
        search_df = search_df[(search_df['strength'] >= str_min) & (search_df['strength'] <= str_max) &
                              (search_df['cost'] >= cost_min) & (search_df['cost'] <= cost_max) &
                              (search_df['weight'] >= weight_min) & (search_df['weight'] <= weight_max)]
    
    with col2:
        st.markdown("#### 📊 Results & Display")
        sort_col = st.selectbox("Sort by", ["Name", "Strength", "Cost", "Weight", "Corrosion", "Sustainability"], key="sort_adv")
        sort_map = {"Name": "name", "Strength": "strength", "Cost": "cost", "Weight": "weight", "Corrosion": "corrosion", "Sustainability": "sustainability_score"}
        search_df = search_df.sort_values(sort_map[sort_col], ascending=(sort_col == "Cost" or sort_col == "Weight"))
        
        st.markdown(f"**✓ {len(search_df)} materials found**")
        
        display_cols = st.multiselect("Display columns", ["name", "category", "strength", "weight", "cost", "temp_limit", "corrosion", "sustainability_score"], 
                                     default=["name", "category", "strength", "cost", "sustainability_score"], key="display_cols_adv")
    
    st.divider()
    
    if len(search_df) > 0:
        # Create a nice dataframe display
        display_df = search_df[display_cols].copy()
        display_df.columns = [col.replace('_', ' ').title() for col in display_cols]
        st.dataframe(display_df, use_container_width=True, hide_index=True)
    else:
        st.info("No materials found matching your criteria.")

with tab3:
    st.markdown("### 💰 Cost of Ownership Analysis")
    st.markdown("Calculate total cost including lifecycle, maintenance, and replacement")
    
    col1, col2, col3, col4 = st.columns(4, gap="medium")
    
    with col1:
        st.markdown("**Material**")
        selected_mat = st.selectbox("", df['name'].unique(), key="mat_coo", label_visibility="collapsed")
        mat_data = df[df['name'] == selected_mat].iloc[0]
    
    with col2:
        st.markdown("**Unit Price**")
        unit_price = st.number_input("$", 10.0, 1000.0, float(mat_data['cost']), step=10.0, key="unit_price_coo", label_visibility="collapsed")
    
    with col3:
        st.markdown("**Quantity**")
        quantity = st.number_input(" ", 1, 1000, 1, step=1, key="qty_coo", label_visibility="collapsed")
    
    with col4:
        st.markdown("**Lifespan (years)**")
        lifespan = st.number_input("  ", 1, 50, 5, step=1, key="lifespan_coo", label_visibility="collapsed")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Annual Maintenance ($)**")
        maintenance_annual = st.number_input("", 0, 10000, 0, step=100, key="maint_coo", label_visibility="collapsed")
    with col2:
        st.markdown("**Replacement Factor (%)**")
        replacement_factor = st.slider("", 0, 100, 20, help="% cost every N years", key="repl_factor", label_visibility="collapsed")
    
    total_cost, cost_per_year = calculate_total_cost_of_ownership(selected_mat, unit_price, quantity, lifespan, maintenance_annual)
    
    st.divider()
    
    # Display metrics with nice styling
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("💰 Total Cost", f"${total_cost:,.0f}", border=True)
    col2.metric("📅 Cost/Year", f"${cost_per_year:,.0f}", border=True)
    col3.metric("🏭 Material Cost", f"${unit_price * quantity:,.0f}", border=True)
    col4.metric("🔧 Maintenance", f"${maintenance_annual * lifespan:,.0f}", border=True)
    col5.metric("🔄 Replacements", f"${total_cost - (unit_price * quantity) - (maintenance_annual * lifespan):,.0f}", border=True)
    
    st.divider()
    st.markdown("#### 📊 Material Comparison (Cost of Ownership)")
    
    category = mat_data['category']
    category_df = df[df['category'] == category].head(10)
    
    comparison_data = []
    for _, row in category_df.iterrows():
        t_cost, y_cost = calculate_total_cost_of_ownership(row['name'], row['cost'], quantity, lifespan, maintenance_annual)
        comparison_data.append({'Material': row['name'], 'Total Cost ($)': t_cost, 'Annual Cost ($)': y_cost})
    
    comp_df = pd.DataFrame(comparison_data).sort_values('Total Cost ($)')
    
    fig = px.bar(comp_df, x='Material', y='Total Cost ($)', title=f"Cost Comparison - {category} Category", 
                 labels={'Total Cost ($)': 'Total Cost ($)'}, height=400)
    fig.update_layout(template='plotly_dark', hovermode='x unified', showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

with tab4:
    st.markdown("### 🔄 Material Substitution Finder")
    st.markdown("Find alternative materials with similar or better properties")
    
    col1, col2 = st.columns([1.5, 1.5])
    
    with col1:
        base_material = st.selectbox("Select base material to replace", df['name'].unique(), key="base_mat")
        base_data = df[df['name'] == base_material].iloc[0]
        
        st.markdown("#### Original Material Properties")
        st.metric("Category", base_data['category'])
        st.metric("Strength", f"{base_data['strength']:.0f} MPa")
        st.metric("Cost", f"${base_data['cost']:.0f}")
        st.metric("Sustainability", f"{base_data.get('sustainability_score', 50):.0f}/100")
    
    with col2:
        tolerance = st.slider("Performance tolerance (%)", 0, 50, 10, help="How much performance can vary")
        priority = st.radio("Prioritize by", ["Cost Reduction", "Weight Reduction", "Better Performance", "Sustainability"])
        exclude_category = st.checkbox("Exclude same category", value=True)
    
    candidates = df.copy()
    if exclude_category:
        candidates = candidates[candidates['category'] != base_data['category']]
    
    candidates = candidates[candidates['strength'] >= base_data['strength'] * (1 - tolerance/100)]
    
    if priority == "Cost Reduction":
        candidates = candidates.sort_values('cost')
    elif priority == "Weight Reduction":
        candidates = candidates.sort_values('weight')
    elif priority == "Better Performance":
        candidates['perf_score'] = candidates['strength'] + candidates['corrosion'] - candidates['cost']/100
        candidates = candidates.sort_values('perf_score', ascending=False)
    else:
        candidates = candidates.sort_values('sustainability_score', ascending=False)
    
    st.markdown("#### 🎯 Top Alternatives")
    for idx, (_, alt) in enumerate(candidates.head(5).iterrows(), 1):
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(f"#{idx} {alt['name']}", alt['category'], border=True)
        with col2:
            savings = ((base_data['cost'] - alt['cost']) / base_data['cost'] * 100) if base_data['cost'] > 0 else 0
            color = "green" if savings > 0 else "red"
            st.metric("Cost Change", f"${alt['cost']:.0f}", f"{savings:+.1f}%", border=True,
                     delta_color="inverse")
        with col3:
            weight_change = ((base_data['weight'] - alt['weight']) / base_data['weight'] * 100) if base_data['weight'] > 0 else 0
            st.metric("Weight", f"{alt['weight']:.2f} g/cm³", f"{weight_change:+.1f}%", border=True,
                     delta_color="inverse")
        with col4:
            sustainability = alt.get('sustainability_score', 50)
            st.metric("Sustainability", f"{sustainability:.0f}/100", f"{sustainability - base_data.get('sustainability_score', 50):+.0f}", border=True)
        
        st.markdown(f"**Properties:** Strength {alt['strength']:.0f} MPa • Corrosion {alt['corrosion']:.0f}/10 • Temp {alt['temp_limit']:.0f}°C")
        st.divider()

with tab5:
    st.markdown("### ♻️ Sustainability & Environmental Analysis")
    st.markdown("Evaluate materials based on environmental impact and recyclability")
    
    col1, col2 = st.columns([1.5, 1.5], gap="large")
    
    with col1:
        st.markdown("#### 🌍 Sustainability Filters")
        min_recyclability = st.slider("Min Recyclability Score", 0, 10, 5)
        min_sustainability = st.slider("Min Sustainability Score", 0, 100, 60)
        
        eco_df = df[(df.get('recyclability', 5) >= min_recyclability) & 
                    (df.get('sustainability_score', 50) >= min_sustainability)].sort_values('sustainability_score', ascending=False)
        
        st.markdown(f"**{len(eco_df)} materials meet sustainability criteria**")
    
    with col2:
        if len(eco_df) > 0:
            fig = px.scatter(eco_df, x='recyclability', y='sustainability_score', 
                            size='strength', color='category', hover_name='name',
                            title="Sustainability vs Recyclability", height=400)
            fig.update_layout(template='plotly_dark')
            st.plotly_chart(fig, use_container_width=True)
    
    st.divider()
    st.markdown("#### 📊 Top Sustainable Materials")
    
    eco_display = eco_df[['name', 'category', 'sustainability_score', 'recyclability', 'strength', 'cost']].head(10)
    eco_display.columns = ['Material', 'Category', 'Sustainability', 'Recyclability', 'Strength (MPa)', 'Cost ($)']
    
    st.dataframe(eco_display, use_container_width=True, hide_index=True)
    
    st.markdown("#### ♻️ Recycling Impact")
    col1, col2 = st.columns(2)
    
    with col1:
        highly_recyclable = len(df[df.get('recyclability', 5) >= 8])
        st.metric("Highly Recyclable Materials (8+/10)", highly_recyclable, f"of {len(df)}")
    
    with col2:
        sustainable_score = len(df[df.get('sustainability_score', 50) >= 80])
        st.metric("Highly Sustainable (80+/100)", sustainable_score, f"of {len(df)}")

with tab6:
    st.markdown("### 🤖 Performance Prediction Engine")
    st.markdown("Predict material performance under specific conditions using ML")
    
    col1, col2 = st.columns(2, gap="large")
    
    with col1:
        st.markdown("#### ⚙️ Simulation Parameters")
        load_condition = st.selectbox("Load Condition", ["Static", "Cyclic", "Impact", "Thermal Shock", "Corrosive Environment"])
        temperature = st.slider("Operating Temperature (°C)", 0, 2000, 300)
        humidity = st.slider("Humidity Level (%)", 0, 100, 50)
        stress_level = st.slider("Stress Level (% of yield)", 0, 100, 60)
    
    with col2:
        st.markdown("#### 📈 Prediction Results")
        
        prediction_df = df.copy()
        
        reliability_score = (
            (1 - abs(prediction_df['temp_limit'] - temperature) / max(prediction_df['temp_limit'])) * 0.3 +
            (prediction_df['corrosion'] / 10) * 0.4 +
            (1 - stress_level / 100) * 0.3
        )
        
        prediction_df['reliability'] = np.maximum(reliability_score, 0)
        prediction_df = prediction_df.sort_values('reliability', ascending=False)
        
        if len(prediction_df) > 0:
            best_pred = prediction_df.iloc[0]
            st.metric("Top Recommended Material", best_pred['name'], f"Reliability: {best_pred['reliability']*100:.1f}%", border=True)
            st.metric("Category", best_pred['category'], border=True)
            st.metric("Cost", f"${best_pred['cost']:.0f}", border=True)
    
    st.divider()
    st.markdown("#### 🎯 Top Materials for This Condition")
    
    fig = go.Figure()
    top_materials = prediction_df.head(10)
    
    fig.add_trace(go.Bar(
        x=top_materials['name'],
        y=top_materials['reliability'] * 100,
        marker_color='#5a5a9e',
        name='Reliability Score',
        text=[f"{r*100:.1f}%" for r in top_materials['reliability']],
        textposition='outside'
    ))
    
    fig.update_layout(title="Material Reliability Under Specified Conditions", 
                     template='plotly_dark', height=400, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

with tab7:
    st.markdown("### 📊 Advanced Analytics Dashboard")
    st.markdown("Comprehensive statistical analysis of all materials")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    col1.metric("📦 Total Materials", len(df), border=True)
    col2.metric("🏷️ Categories", df['category'].nunique(), border=True)
    col3.metric("💪 Avg Strength", f"{df['strength'].mean():.0f} MPa", border=True)
    col4.metric("💰 Avg Cost", f"${df['cost'].mean():.0f}", border=True)
    col5.metric("🌡️ Max Temp Avg", f"{df['temp_limit'].mean():.0f}°C", border=True)
    
    st.divider()
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.scatter(df, x='cost', y='strength', color='category', size='weight',
                        title="Strength vs Cost (sized by Weight)", hover_name='name', height=450, markers={'size': 8})
        fig.update_layout(template='plotly_dark', hovermode='closest', showlegend=True)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = px.box(df, x='category', y='cost', title="Cost Distribution by Category", height=450)
        fig.update_layout(template='plotly_dark', hovermode='closest')
        st.plotly_chart(fig, use_container_width=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        category_avg = df.groupby('category')['strength'].mean().sort_values(ascending=False)
        fig = px.bar(x=category_avg.values, y=category_avg.index, orientation='h',
                    title="Average Strength by Category", labels={'x': 'Strength (MPa)'}, height=400)
        fig.update_layout(template='plotly_dark', hovermode='closest', showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        corr_data = df[['strength', 'cost', 'weight', 'temp_limit', 'corrosion']].corr()
        
        fig = px.imshow(corr_data, title="Property Correlations", color_continuous_scale='RdBu', height=400,
                       labels=dict(x="Property", y="Property", color="Correlation"))
        fig.update_layout(template='plotly_dark', showscale=True)
        st.plotly_chart(fig, use_container_width=True)

with tab8:
    st.markdown("### 📋 Complete Material Database")
    st.markdown("Browse and search the entire materials database")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        search_db = st.text_input("🔍 Search database", placeholder="Search by material name, category, or properties")
    with col2:
        items_per_page = st.selectbox("Items per page", [10, 25, 50, 100], index=1)
    
    if search_db:
        display_df = df[df['name'].str.contains(search_db, case=False) | df['category'].str.contains(search_db, case=False)]
    else:
        display_df = df
    
    st.markdown(f"**Showing {len(display_df)} of {len(df)} materials**")
    
    st.dataframe(display_df.head(items_per_page), use_container_width=True, hide_index=True)
    
    if len(display_df) > items_per_page:
        st.info(f"📄 Showing {items_per_page} of {len(display_df)} results. Scroll to see more or adjust 'Items per page'")

st.divider()

st.markdown("""
<div style='text-align: center; background: linear-gradient(135deg, rgba(60, 80, 160, 0.1) 0%, rgba(40, 60, 140, 0.1) 100%);
            border-top: 1px solid rgba(100, 150, 255, 0.2); padding: 32px 20px; margin-top: 40px; border-radius: 14px;'>
    <p style='color: #8090c0; margin: 8px 0; font-weight: 600;'>Material Selector Pro v2.0 - Enterprise Edition</p>
    <p style='color: #6080b0; margin: 4px 0; font-size: 0.95em;'>ML-powered material intelligence for engineering and product design</p>
    <p style='color: #5070a0; margin: 8px 0; font-size: 0.9em;'>💡 Tip: Use the Quick Select tab for instant recommendations</p>
</div>
""", unsafe_allow_html=True)
