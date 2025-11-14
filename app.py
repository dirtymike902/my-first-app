import streamlit as st

# Custom CSS for styling
st.markdown("""
    <style>
    .stApp {
        background-color: #f0f4f8;
    }
    .main-title {
        color: #2c3e50;
        font-family: 'Arial', sans-serif;
        text-align: center;
    }
    .section-header {
        color: #34495e;
        font-weight: bold;
    }
    .metric-label {
        font-size: 16px !important;
    }
    .metric-value {
        font-size: 20px !important;
        color: #27ae60;
    }
    .warning-metric .metric-value {
        color: #e74c3c;
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
st.markdown("<h1 class='main-title'>🕒 Time Well Spent by Dirty Mike</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #7f8c8d;'>For Nova Scotia, Canada (2025 rates)</p>", unsafe_allow_html=True)

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
    
    fed
