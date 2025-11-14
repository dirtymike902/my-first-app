import streamlit as st

# Constants for tax brackets and rates (2025)
FEDERAL_BRACKETS = [
    (57375, 0.145), (114750, 0.205), (177882, 0.260), (253414, 0.290), (float('inf'), 0.330)
]
FEDERAL_BPA = 16129
FEDERAL_LOWEST_RATE = 0.145

NS_BRACKETS = [(30507, 0.0879), (61015, 0.1495), (95883, 0.1667), (154650, 0.1750), (float('inf'), 0.210)]
NS_BPA = 11744
NS_LOWEST_RATE = 0.0879
NS_CODE = "NS"

AB_BRACKETS = [(60000, 0.08), (151234, 0.10), (181481, 0.12), (241974, 0.13), (362961, 0.14), (float('inf'), 0.15)]
AB_BPA = 22323
AB_LOWEST_RATE = 0.08
AB_CODE = "AB"

CPP_EXEMPTION = 3500
CPP_YMPE = 71300
CPP_YAMPE = 81200
CPP_RATE1 = 0.0595
CPP_RATE2 = 0.04

EI_MAX_INSURABLE = 65700
EI_RATE = 0.0164

ANNUAL_HOURS = 2080

# Cleaned CSS: Fixed invalid selectors (e.g., removed broken .st-emotion-cache-*), ensured valid syntax
st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Permanent+Marker&display=swap" rel="stylesheet">
    <style>
    .stApp {
        background: linear-gradient(135deg, #FF0000 0%, #FFFFFF 50%, #C8102E 100%) !important;
        color: #333333 !important;
    }
    body { color: #333333 !important; }
    .main-title { color: #8B4513 !important; font-family: 'Arial', sans-serif; text-align: center; font-size: 2.5em; }
    .crooked-clock { display: inline-block; transform: rotate(-15deg); margin-right: 5px; }
    .money-bag { display: inline-block; transform: rotate(5deg); margin-left: 10px; font-size: 1.2em; }
    .subtitle { color: #8B4513 !important; text-align: center; font-size: 1.2em; margin-top: -10px; }
    .logo {
        font-family: 'Permanent Marker', cursive; font-size: 1.5em; background-color: #FFD700;
        color: #8B4513 !important; border-radius: 15px; padding: 8px 12px; display: inline-block;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.3); transform: rotate(-2deg);
    }
    .section-header { color: #34495e !important; font-weight: bold; }
    .metric-label { font-size: 16px !important; color: #333333 !important; }
    .metric-value { font-size: 20px !important; color: #27ae60 !important; }
    .warning-metric .metric-value { color: #e74c3c !important; }
    
    /* Unified dark/light mode & mobile overrides */
    @media (prefers-color-scheme: dark), (max-width: 768px) {
        .stApp, body { background: linear-gradient(135deg, #FF0000 0%, #FFFFFF 50%, #C8102E 100%) !important; color: #333333 !important; }
        .main, .sidebar { background-color: #f0f4f8 !important; color: #333333 !important; }
        .stSidebar { background-color: #f0f4f8 !important; color: #333333 !important; }
        .stSidebar label, .stSidebar h1, .stSidebar h2, .stSidebar h3, .stSidebar p, .stSidebar span { color: #333333 !important; opacity: 1 !important; font-weight: 500 !important; }
        .main-title, .subtitle, .section-header, .logo { color: #8B4513 !important; }
        /* Sidebar inputs: Force contrast for mobile/iOS */
        .stSidebar input[type="number"], .stSidebar [role="combobox"], .stSidebar select, .stSidebar option {
            color: #ffffff !important; -webkit-text-fill-color: #ffffff !important;
            background-color: rgba(0,0,0,0.5) !important;
        }
        [data-testid="stMarkdown"] *, [data-testid="stText"] *, h1, h2, h3, p, span, div { color: #333333 !important; }
        .css-1d391kg, .css-1inbwe5, .css-1v3b6i6 { color: #333333 !important; }
    }
    .stButton > button { background-color: #3498db; color: white; border-radius: 5px; }
    .stButton > button:hover { background-color: #2980b9; }
    </style>
""", unsafe_allow_html=True)

def calculate_progressive_tax(income, brackets):
    """Calculate progressive tax based on brackets: list of (upper_limit, rate)."""
    tax = 0.0
    prev_limit = 0.0
    for limit, rate in brackets:
        if income > limit:
            tax += (limit - prev_limit) * rate
            prev_limit = limit
        else:
            tax += (income - prev_limit) * rate
            return tax
    # Handle income exceeding last bracket if infinite
    if brackets and brackets[-1][0] == float('inf'):
        tax += (income - prev_limit) * brackets[-1][1]
    return tax

def federal_tax(income):
    """Federal tax after basic personal amount credit."""
    gross_tax = calculate_progressive_tax(income, FEDERAL_BRACKETS)
    credit = FEDERAL_LOWEST_RATE * FEDERAL_BPA
    return max(gross_tax - credit, 0)

def prov_tax(income, province):
    """Provincial tax after basic personal amount credit. Returns (tax, code)."""
    if province == "Nova Scotia":
        brackets, bpa, lowest_rate, code = NS_BRACKETS, NS_BPA, NS_LOWEST_RATE, NS_CODE
    else:  # Alberta
        brackets, bpa, lowest_rate, code = AB_BRACKETS, AB_BPA, AB_LOWEST_RATE, AB_CODE
    
    gross_tax = calculate_progressive_tax(income, brackets)
    credit = lowest_rate * bpa
    return max(gross_tax - credit, 0), code

def calculate_cpp(gross):
    """CPP contributions: First and second tier."""
    pensionable1 = max(gross - CPP_EXEMPTION, 0)
    cpp1 = min(pensionable1, CPP_YMPE - CPP_EXEMPTION) * CPP_RATE1
    cpp2 = 0
    if gross > CPP_YMPE:
        second_tier = min(gross - CPP_YMPE, CPP_YAMPE - CPP_YMPE)
        cpp2 = second_tier * CPP_RATE2
    return cpp1 + cpp2

def calculate_ei(gross):
    """EI premiums."""
    return min(gross, EI_MAX_INSURABLE) * EI_RATE

# App UI
st.markdown("<h1 class='main-title'><span class='crooked-clock'>🕒</span> Time Well Spent <span class='money-bag'>💰</span></h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>By - <span class='logo'>Dirty Mike</span></p>", unsafe_allow_html=True)

st.write("""
This app helps you understand how much time you need to work to afford your purchases, after accounting for taxes and deductions.
**Assumptions:** Single filer, no other deductions/credits, 2080 working hours/year.
""")

# Sidebar
with st.sidebar:
    st.header("Your Details")
    province = st.selectbox("Province", ["Nova Scotia", "Alberta"], index=0)
    hourly_wage = st.number_input("Gross Hourly Wage ($)", min_value=0.0, value=25.0, step=0.01)
    purchase = st.number_input("Purchase Amount ($)", min_value=0.0, value=100.0, step=0.01)
    calculate_button = st.button("Calculate")

st.markdown(f"<p style='text-align: center; color: #7f8c8d !important;'>For {province}, Canada (2025 rates)</p>", unsafe_allow_html=True)

if calculate_button and hourly_wage > 0:
    annual_gross = hourly_wage * ANNUAL_HOURS
    fed = federal_tax(annual_gross)
    prov, prov_code = prov_tax(annual_gross, province)
    cpp = calculate_cpp(annual_gross)
    ei = calculate_ei(annual_gross)
    total_deductions = fed + prov + cpp + ei
    net_annual = annual_gross - total_deductions
    net_hourly = net_annual / ANNUAL_HOURS
    
    # Results
    st.header("Your Income Breakdown")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Annual Gross Income", f"${annual_gross:,.2f}")
        st.metric("Net Annual Income", f"${net_annual:,.2f}", delta_color="inverse")
    with col2:
        st.metric("Net Hourly Rate", f"${net_hourly:,.2f}")
    
    with st.expander("View Detailed Deductions"):
        col3, col4 = st.columns(2)
        with col3:
            with st.container():  # Wrap for warning styling
                st.metric("Federal Tax", f"${fed:,.2f}")
                st.metric(f"Provincial Tax ({prov_code})", f"${prov:,.2f}")
        with col4:
            with st.container():
                st.metric("CPP Contribution", f"${cpp:,.2f}")
                st.metric("EI Premium", f"${ei:,.2f}")
        st.metric("Total Deductions", f"${total_deductions:,.2f}")
    
    if purchase > 0:
        hours_needed = purchase / net_hourly
        hours = int(hours_needed)
        minutes = int((hours_needed * 60) % 60)
        st.header("Time to Afford Your Purchase")
        st.success(f"To afford **${purchase:,.2f}**, you need to work **{hours} hours and {minutes} minutes**. ⏰")
        st.snow()
        st.markdown("<div style='text-align: center; font-size: 3em; margin: 10px 0;'>💵💰💎🍁</div>", unsafe_allow_html=True)
    else:
        st.success("Free purchase! 🎉 No work needed.")
else:
    st.info("Enter your hourly wage and purchase amount in the sidebar, then click 'Calculate' to see results.")
