import streamlit as st
import requests
from PIL import Image
from io import BytesIO

# Function to load image from URL
@st.cache_data
def load_image(url):
    try:
        response = requests.get(url)
        img = Image.open(BytesIO(response.content))
        return img
    except:
        return None

# Import Google Fonts for cool sticker font
st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Permanent+Marker&display=swap" rel="stylesheet">
""", unsafe_allow_html=True)

# Custom CSS for styling
st.markdown("""
    <style>
    .stApp {
        background-color: #f0f4f8 !important;
        color: #333333 !important;
    }
    body {
        color: #333333 !important;
    }
    .main-title {
        color: #8B4513 !important;
        font-family: 'Arial', sans-serif;
        text-align: center;
        font-size: 2.5em;
    }
    .crooked-clock {
        display: inline-block;
        transform: rotate(-15deg);
        margin-right: 5px;
    }
    .money-bag {
        display: inline-block;
        transform: rotate(5deg);
        margin-left: 10px;
        font-size: 1.2em;
    }
    .subtitle {
        color: #8B4513 !important;
        text-align: center;
        font-size: 1.2em;
        margin-top: -10px;
    }
    .logo {
        font-family: 'Permanent Marker', cursive;
        font-size: 1.5em;
        background-color: #FFD700;
        color: #8B4513 !important;
        border-radius: 15px;
        padding: 8px 12px;
        display: inline-block;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.3);
        transform: rotate(-2deg); /* Slight tilt for sticker vibe */
    }
    .section-header {
        color: #34495e !important;
        font-weight: bold;
    }
    .metric-label {
        font-size: 16px !important;
        color: #333333 !important;
    }
    .metric-value {
        font-size: 20px !important;
        color: #27ae60 !important;
    }
    /* Money-themed metrics: Green for positive (like cash), Gold/Yellow for gross/net */
    .metric-container .stMetric > label {
        color: #333333 !important;
    }
    .metric-container .stMetric > div > div {
        background: linear-gradient(135deg, #27ae60 0%, #2ecc71 100%) !important; /* Green gradient for money feel */
        color: #ffffff !important;
        border-radius: 8px !important;
        padding: 10px !important;
        box-shadow: 0 4px 8px rgba(39, 174, 96, 0.3) !important;
    }
    .metric-container .stMetric > div > div .metric-value {
        color: #ffffff !important; /* White text on green bg for contrast */
        text-shadow: 1px 1px 2px rgba(0,0,0,0.5) !important;
    }
    /* Gold theme for gross income (shiny!) */
    .stMetric:has(> div:contains("Gross")) .stMetric > div > div {
        background: linear-gradient(135deg, #f39c12 0%, #e67e22 100%) !important; /* Gold/orange gradient */
        box-shadow: 0 4px 8px rgba(243, 156, 18, 0.4) !important;
    }
    /* Warning metrics: Red tint but with money edge */
    .warning-metric .stMetric > div > div {
        background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%) !important;
        box-shadow: 0 4px 8px rgba(231, 76, 60, 0.3) !important;
    }
    .warning-metric .metric-value {
        color: #ffffff !important;
    }
    /* Shine effect: Add a subtle glow to key elements */
    .logo::after {
        content: '';
        position: absolute;
        top: -2px;
        left: -2px;
        right: -2px;
        bottom: -2px;
        background: linear-gradient(45deg, #FFD700, #FFA500, #FFD700);
        border-radius: 17px;
        z-index: -1;
        animation: shine 2s infinite;
        opacity: 0.7;
    }
    @keyframes shine {
        0% { opacity: 0.7; transform: scale(1); }
        50% { opacity: 1; transform: scale(1.02); }
        100% { opacity: 0.7; transform: scale(1); }
    }
    /* Force light theme and dark text on iOS/mobile dark mode */
    @media (prefers-color-scheme: dark) {
        .stApp {
            background-color: #f0f4f8 !important;
            color: #333333 !important;
        }
        body {
            background-color: #f0f4f8 !important;
            color: #333333 !important;
        }
        .main, .sidebar {
            background-color: #f0f4f8 !important;
            color: #333333 !important;
        }
        .stSidebar {
            background-color: #f0f4f8 !important;
            color: #333333 !important;
        }
        .stSidebar label {
            color: #333333 !important;
            font-weight: 500 !important;
            opacity: 1 !important;
        }
        .stSidebar .stMarkdown {
            color: #333333 !important;
        }
        .stSidebar h1, .stSidebar h2, .stSidebar h3, .stSidebar p, .stSidebar span {
            color: #333333 !important;
        }
        h1, h2, h3, p, span, div {
            color: #333333 !important;
        }
        .main-title {
            color: #8B4513 !important;
        }
        .subtitle {
            color: #8B4513 !important;
        }
        .section-header {
            color: #34495e !important;
        }
        .logo {
            color: #8B4513 !important;
        }
        .metric-label, .metric-value {
            color: inherit !important;
        }
        /* Target Streamlit-specific elements */
        [data-testid="stMarkdown"] *, [data-testid="stText"] *, [data-testid="stException"] * {
            color: #333333 !important;
        }
        .st-emotion-cache-* {
            color: #333333 !important;
        }
        /* Sidebar input labels specifically */
        .stSidebar [data-testid="column"] label, .stSidebar [data-testid="stNumberInput"] label {
            color: #333333 !important;
            opacity: 1 !important;
        }
        /* Override metrics in dark mode */
        .metric-container .stMetric > div > div {
            background: linear-gradient(135deg, #27ae60 0%, #2ecc71 100%) !important;
            color: #ffffff !important;
        }
        .stMetric:has(> div:contains("Gross")) .stMetric > div > div {
            background: linear-gradient(135deg, #f39c12 0%, #e67e22 100%) !important;
        }
    }
    /* Mobile-specific tweaks for iOS Safari */
    @media (max-width: 768px) {
        .stApp {
            background-color: #f0f4f8 !important;
            color: #333333 !important;
        }
        body {
            -webkit-text-size-adjust: 100% !important;
            color: #333333 !important;
        }
        .stSidebar {
            color: #333333 !important;
        }
        .stSidebar label {
            color: #333333 !important;
            opacity: 1 !important;
        }
    }
    .stButton>button {
        background-color: #3498db;
        color: white;
        border-radius: 5px;
    }
    .stButton>button:hover {
        background-color: #2980b9;
    }
    </style>
""", unsafe_allow_html=True)

def calculate_progressive_tax(income, brackets):
    """
    Calculate progressive tax based on brackets.
    brackets: list of tuples (upper_limit, rate)
    """
    tax = 0.0
    prev_limit = 0.0
    for limit, rate in brackets:
        if income > limit:
            tax += (limit - prev_limit) * rate
            prev_limit = limit
        else:
            tax += (income - prev_limit) * rate
            break
    else:
        # For the last bracket if income > last limit
        if brackets[-1][0] == float('inf'):
            tax += (income - prev_limit) * brackets[-1][1]
    return tax

def federal_tax(income):
    brackets = [
        (57375, 0.145),
        (114750, 0.205),
        (177882, 0.260),
        (253414, 0.290),
        (float('inf'), 0.330)
    ]
    gross_tax = calculate_progressive_tax(income, brackets)
    # Basic personal amount credit
    bpa_fed = 16129
    credit = 0.145 * bpa_fed  # At lowest rate
    return max(gross_tax - credit, 0)

def ns_tax(income):
    brackets = [
        (30507, 0.0879),
        (61015, 0.1495),
        (95883, 0.1667),
        (154650, 0.1750),
        (float('inf'), 0.210)
    ]
    gross_tax = calculate_progressive_tax(income, brackets)
    # Basic personal amount credit
    bpa_ns = 11744
    credit = 0.0879 * bpa_ns  # At lowest rate
    return max(gross_tax - credit, 0)

def calculate_cpp(gross):
    exemption = 3500
    ympe = 71300
    yampe = 81200
    # First tier
    pensionable1 = max(gross - exemption, 0)
    cpp1 = min(pensionable1, ympe - exemption) * 0.0595
    # Second tier
    cpp2 = 0
    if gross > ympe:
        second_tier = min(gross - ympe, yampe - ympe)
        cpp2 = second_tier * 0.04
    return cpp1 + cpp2

def calculate_ei(gross):
    max_insurable = 65700
    rate = 0.0164
    return min(gross, max_insurable) * rate

# Streamlit app
st.markdown("<h1 class='main-title'><span class='crooked-clock'>🕒</span> Time Well Spent <span class='money-bag'>💰</span></h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>By - <span class='logo'>Dirty Mike</span></p>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #7f8c8d !important;'>For Nova Scotia, Canada (2025 rates)</p>", unsafe_allow_html=True)

# Add thematic images
col_img1, col_img2 = st.columns(2)
with col_img1:
    time_img = load_image("https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=300&h=200&fit=crop")  # Clock/hourglass for time
    if time_img:
        st.image(time_img, caption="Time is Money", use_column_width=True)
with col_img2:
    money_img = load_image("https://images.unsplash.com/photo-1560472354-b33ff0c44a43?w=300&h=200&fit=crop")  # Gold coins/money stack
    if money_img:
        st.image(money_img, caption="Stack That Cash", use_column_width=True)

st.write("""
This app helps you understand how much time you need to work to afford your purchases, after accounting for taxes and deductions.
**Assumptions:** Single filer, no other deductions/credits, 2080 working hours/year.
""")

# Sidebar for inputs
with st.sidebar:
    st.header("Your Details")
    hourly_wage = st.number_input("Gross Hourly Wage ($)", min_value=0.0, value=25.0, step=0.01, help="Enter your pre-tax hourly pay rate.")
    purchase = st.number_input("Purchase Amount ($)", min_value=0.0, value=100.0, step=0.01, help="Enter the cost of the item you want to buy.")
    calculate_button = st.button("Calculate")

if calculate_button and hourly_wage > 0:
    annual_gross = hourly_wage * 2080
    
    fed = federal_tax(annual_gross)
    prov = ns_tax(annual_gross)
    cpp = calculate_cpp(annual_gross)
    ei = calculate_ei(annual_gross)
    total_deductions = fed + prov + cpp + ei
    net_annual = annual_gross - total_deductions
    net_hourly = net_annual / 2080 if annual_gross > 0 else 0
    
    # Display results
    st.header("Your Income Breakdown")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Annual Gross Income", f"${annual_gross:,.2f}", help="Based on 2080 hours/year")
        st.metric("Net Annual Income", f"${net_annual:,.2f}", delta_color="inverse", help="After all deductions")
    with col2:
        st.metric("Net Hourly Rate", f"${net_hourly:,.2f}", help="Your effective take-home pay per hour")
    
    with st.expander("View Detailed Deductions"):
        col3, col4 = st.columns(2)
        with col3:
            st.markdown("<div class='warning-metric'>", unsafe_allow_html=True)
            st.metric("Federal Tax", f"${fed:,.2f}")
            st.metric("Provincial Tax (NS)", f"${prov:,.2f}")
            st.markdown("</div>", unsafe_allow_html=True)
        with col4:
            st.markdown("<div class='warning-metric'>", unsafe_allow_html=True)
            st.metric("CPP Contribution", f"${cpp:,.2f}")
            st.metric("EI Premium", f"${ei:,.2f}")
            st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("<div class='warning-metric'>", unsafe_allow_html=True)
        st.metric("Total Deductions", f"${total_deductions:,.2f}")
        st.markdown("</div>", unsafe_allow_html=True)
    
    if purchase > 0 and net_hourly > 0:
        hours_needed = purchase / net_hourly
        total_minutes = hours_needed * 60
        hours = int(hours_needed)
        minutes = int(total_minutes % 60)
        st.header("Time to Afford Your Purchase")
        st.success(f"To afford **${purchase:,.2f}**, you need to work **{hours} hours and {minutes} minutes**. ⏰")
        st.snow()  # Changed to snowflakes for a different celebratory effect!
else:
    st.info("Enter your hourly wage and purchase amount in the sidebar, then click 'Calculate' to see results.")
