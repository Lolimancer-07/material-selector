"""
Dark Theme CSS Styling Module
Professional dark-themed design system
"""

DARK_THEME_CSS = """
    <style>
        * {
            font-family: 'Segoe UI', Roboto, 'Helvetica Neue', sans-serif;
        }
        
        /* Main Background - Deep Dark */
        [data-testid="stAppViewContainer"] {
            background-color: #0d1117;
        }
        
        .main {
            background-color: #0d1117;
        }
        
        /* Text Colors */
        h1, h2, h3, h4, h5, h6 {
            color: #58a6ff;
            font-weight: 900;
            letter-spacing: -0.5px;
        }
        
        h1 {
            font-size: 3.2em !important;
            color: #79c0ff;
            margin-bottom: 10px;
        }
        
        h2 {
            border-bottom: 2px solid #58a6ff;
            padding-bottom: 10px;
            color: #79c0ff;
        }
        
        h3 {
            color: #58a6ff;
            font-weight: 700;
        }
        
        p, span, label {
            color: #c9d1d9;
            line-height: 1.6;
        }
        
        /* Cards & Containers */
        [data-testid="stMetricContainer"] {
            background-color: #161b22;
            border: 1px solid #30363d;
            border-radius: 8px;
            padding: 16px;
        }
        
        .metric-card {
            background: linear-gradient(135deg, #161b22 0%, #0d1117 100%);
            border: 1px solid #30363d;
            border-left: 4px solid #58a6ff;
            border-radius: 8px;
            padding: 20px;
            margin: 12px 0;
        }
        
        /* Tabs */
        .stTabs [data-baseweb="tab-list"] {
            background-color: #0d1117;
            gap: 8px;
        }
        
        .stTabs [data-baseweb="tab"] {
            background-color: #161b22;
            border: 1px solid #30363d;
            border-radius: 6px;
            color: #c9d1d9;
            font-weight: 600;
            padding: 10px 16px;
        }
        
        .stTabs [data-baseweb="tab"]:hover {
            background-color: #21262d;
            border-color: #58a6ff;
            color: #79c0ff;
        }
        
        .stTabs [aria-selected="true"] [data-baseweb="tab"] {
            background-color: #58a6ff;
            color: #0d1117;
            border-color: #58a6ff;
        }
        
        /* Buttons */
        .stButton > button {
            background-color: #238636 !important;
            color: #ffffff !important;
            border: 1px solid #2ea043;
            border-radius: 6px;
            font-weight: 600;
            transition: all 0.2s ease;
        }
        
        .stButton > button:hover {
            background-color: #2ea043 !important;
            border-color: #3fb950;
            box-shadow: 0 0 20px rgba(88, 166, 255, 0.3);
        }
        
        /* Inputs */
        input, select, textarea {
            background-color: #0d1117 !important;
            border: 1px solid #30363d !important;
            color: #c9d1d9 !important;
            border-radius: 6px !important;
            padding: 8px 12px !important;
        }
        
        input:focus, select:focus, textarea:focus {
            background-color: #161b22 !important;
            border-color: #58a6ff !important;
            box-shadow: 0 0 0 3px rgba(88, 166, 255, 0.1) !important;
        }
        
        input::placeholder {
            color: #6e7681;
        }
        
        /* Alerts & Boxes */
        .stInfo {
            background-color: #0f3d8b;
            border: 1px solid #1f6feb;
            border-radius: 6px;
            color: #79c0ff;
            padding: 16px;
        }
        
        .stSuccess {
            background-color: #033701;
            border: 1px solid #238636;
            border-radius: 6px;
            color: #3fb950;
            padding: 16px;
        }
        
        .stWarning {
            background-color: #5c310f;
            border: 1px solid #d29922;
            border-radius: 6px;
            color: #d29922;
            padding: 16px;
        }
        
        .stError {
            background-color: #6b0f1f;
            border: 1px solid #da3633;
            border-radius: 6px;
            color: #f85149;
            padding: 16px;
        }
        
        /* Dataframe */
        .stDataFrame {
            background-color: #0d1117;
        }
        
        [role="gridcell"] {
            background-color: #161b22 !important;
            color: #c9d1d9;
            border-color: #30363d;
        }
        
        /* Divider */
        .stDivider {
            border-top: 1px solid #30363d;
            margin: 20px 0;
        }
        
        /* Sidebar */
        [data-testid="stSidebar"] {
            background-color: #161b22;
            border-right: 1px solid #30363d;
        }
        
        [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
            color: #c9d1d9;
        }
        
        /* Expand */
        .streamlit-expanderHeader {
            background-color: #161b22 !important;
            border: 1px solid #30363d !important;
            color: #79c0ff !important;
        }
        
        /* Sliders */
        [role="slider"] {
            background-color: #30363d !important;
        }
        
        /* Scrollbar */
        ::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }
        
        ::-webkit-scrollbar-track {
            background: #0d1117;
        }
        
        ::-webkit-scrollbar-thumb {
            background: #30363d;
            border-radius: 4px;
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: #6e7681;
        }
        
        /* Custom Classes */
        .dark-card {
            background-color: #161b22;
            border: 1px solid #30363d;
            border-radius: 8px;
            padding: 20px;
            margin: 16px 0;
        }
        
        .stat-value {
            color: #58a6ff;
            font-size: 2.5em;
            font-weight: 900;
            margin: 8px 0;
        }
        
        .stat-label {
            color: #8b949e;
            font-size: 0.9em;
            font-weight: 600;
        }
        
        /* Transitions */
        * {
            transition: all 0.2s ease;
        }
    </style>
"""

def apply_dark_theme():
    """Apply dark theme to Streamlit app"""
    import streamlit as st
    st.markdown(DARK_THEME_CSS, unsafe_allow_html=True)
