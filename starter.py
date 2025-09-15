import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# Page Configuration
st.set_page_config(page_title="HorizonOne", layout="wide")

# --- Header ---
st.title("HorizonOne")
st.subheader("Grow and Protect Your Wealth as an Expatriate in Qatar")
st.subheader("While Investing Back Home, From Qatar")

st.markdown("---")


# --- User Profile Sidebar ---
st.sidebar.header("Your Profile")
nationality = st.sidebar.selectbox("Select Your Nationality", ["Indian", "Filipino (Coming Soon)", "British (Coming Soon)", "South African (Coming Soon)"])

if "Coming Soon" in nationality:
    st.sidebar.warning("This feature is coming soon!")
    st.stop()

# --- Investment Strategy Sidebar ---
st.sidebar.header("Investment Strategy")
risk_profile = st.sidebar.radio("Choose Your Risk Profile", ( "High Risk", "Medium Risk","Low Risk"))

st.sidebar.text_area("Describe your Investing Goals")  # Approx. 1,000 USD
# --- Data Dictionaries ---

# Asset Mix Data
asset_mix_data = {
    "Low Risk": {"Equities": 20, "Bonds": 70, "Cash": 10},
    "Medium Risk": {"Equities": 50, "Bonds": 45, "Cash": 5},
    "High Risk": {"Equities": 75, "Bonds": 15, "Alternatives": 10}
}
selected_asset_mix = asset_mix_data[risk_profile]
asset_labels = list(selected_asset_mix.keys())
asset_values = list(selected_asset_mix.values())

# Country Exposure Data
country_exposure_data = {
    "Low Risk": {"USA": 45, "Developed Markets (Ex-USA)": 30, "Qatar/GCC": 15, "India": 10},
    "Medium Risk": {"USA": 40, "India": 30, "Developed Markets (Ex-USA)": 20, "Qatar/GCC": 10},
    "High Risk": {"India": 40, "USA": 30, "Emerging Markets (Ex-India)": 25, "Qatar/GCC": 5}
}
selected_country_mix = country_exposure_data[risk_profile]
country_labels = list(selected_country_mix.keys())
country_values = list(selected_country_mix.values())


# --- Updated Portfolio Performance Data Generation ---
@st.cache_data
def generate_performance_data(risk_profile):
    np.random.seed(0)
    years = pd.to_datetime(pd.date_range(start='2015-01-01', end='2025-01-01', freq='Y'))
    initial_investment = 36500  # Approx. 10,000 USD in QAR
    
    # India Tax Info (as of 2025)
    LTCG_TAX_RATE = 0.125  # 12.5%
    LTCG_EXEMPTION_INR = 125000 
    QAR_TO_INR_RATE = 22.8 # Approximate conversion rate for exemption
    LTCG_EXEMPTION_QAR = LTCG_EXEMPTION_INR / QAR_TO_INR_RATE

    if risk_profile == "Low Risk":
        returns = np.random.normal(0.05, 0.08, len(years))
    elif risk_profile == "Medium Risk":
        returns = np.random.normal(0.08, 0.15, len(years))
    else: # High Risk
        returns = np.random.normal(0.12, 0.25, len(years))

    portfolio_qatar = [initial_investment]
    portfolio_home = [initial_investment]
    
    for r in returns[:-1]:
        # Qatar Portfolio (No Tax)
        last_val_qatar = portfolio_qatar[-1]
        new_val_qatar = last_val_qatar * (1 + r)
        portfolio_qatar.append(new_val_qatar)

        # Home Country Portfolio (with LTCG Tax)
        last_val_home = portfolio_home[-1]
        new_val_home_pre_tax = last_val_home * (1 + r)
        gain = new_val_home_pre_tax - last_val_home

        taxable_gain = 0
        if gain > LTCG_EXEMPTION_QAR:
            taxable_gain = gain - LTCG_EXEMPTION_QAR
        
        tax_paid = taxable_gain * LTCG_TAX_RATE
        new_val_home_post_tax = new_val_home_pre_tax - tax_paid
        portfolio_home.append(new_val_home_post_tax)

    return pd.DataFrame({
        'Year': years, 
        'Portfolio Value (Qatar)': portfolio_qatar,
        'Portfolio Value (Home Country)': portfolio_home
    })

performance_df = generate_performance_data(risk_profile)


# --- Main Page Visualization Layout ---
st.header(f"Sample '{risk_profile}' Portfolio")
col1, col2 = st.columns(2)

# Column 1: Asset Mix Visualization
with col1:
    st.subheader("Asset Mix")
    fig_asset_mix = go.Figure(data=[go.Pie(labels=asset_labels, values=asset_values, hole=.4, marker_colors=['#004f9b', '#3b8fe3', '#a3c9f2', '#c7dcf7'])])
    fig_asset_mix.update_layout(margin=dict(l=20, r=20, t=30, b=20))
    st.plotly_chart(fig_asset_mix, use_container_width=True)

# Column 2: Country Exposure Visualization
with col2:
    st.subheader("Geographic Exposure")
    fig_country_mix = go.Figure(data=[go.Pie(labels=country_labels, values=country_values, hole=.4, marker_colors=['#006a4e', '#ff9933', '#138808', '#cccccc'])])
    fig_country_mix.update_layout(margin=dict(l=20, r=20, t=30, b=20))
    st.plotly_chart(fig_country_mix, use_container_width=True)

# Full Width: Portfolio Performance Visualization
st.subheader("The Advantage of Investing from Qatar")
fig_performance = go.Figure()

# Add Qatar Trace
fig_performance.add_trace(go.Scatter(
    x=performance_df['Year'], 
    y=performance_df['Portfolio Value (Qatar)'], 
    mode='lines+markers', 
    name='Growth in Qatar (0% Tax)',
    line=dict(color="red")
))

# Add Home Country Trace
fig_performance.add_trace(go.Scatter(
    x=performance_df['Year'], 
    y=performance_df['Portfolio Value (Home Country)'], 
    mode='lines+markers', 
    name='Growth in Home Country (with 12.5% Tax)'
))

fig_performance.update_layout(
    title_text='Qatar vs. Home Country: The Impact of 0% Capital Gains Tax',
    xaxis_title='Year',
    yaxis_title='Portfolio Value (QAR)',
    yaxis_tickformat=',.0f',
    yaxis_ticksuffix=' QAR',
    legend_title_text='Portfolio Scenario'
)
st.plotly_chart(fig_performance, use_container_width=True)
st.caption("The 'Home Country' portfolio simulates the effect of a 12.5% long-term capital gains tax on annual gains above a set threshold, based on India's 2025 tax regulations. This is for illustrative purposes only.")


# --- Marketing Sections ---
st.markdown("---")
st.header("Smart Features to Build Your Wealth")

m_col1, m_col2 = st.columns(2)

with m_col1:
    st.markdown("""
    <div style="background-color:#f0f2f6; padding: 20px; border-radius: 10px; height: 100%;">
    <div style="display: flex; align-items: center; margin-bottom: 10px;">
    <div style="font-size: 3em; margin-right: 20px;">🇮🇳</div>
    <div>
    <h4 style="margin: 0;">Invest Back Home, From Qatar</h4>
    <p style="margin: 0;">Earning in Qatar but want to invest in India's growth? HorizonOne makes it simple to allocate part of your portfolio to Indian assets, connecting your long-term wealth goals to your home country's economy.</p>
    </div>
    </div>
    </div>
    """, unsafe_allow_html=True)

with m_col2:
    st.markdown("""
    <div style="background-color:#f0f2f6; padding: 20px; border-radius: 10px; height: 100%;">
    <div style="display: flex; align-items: center; margin-bottom: 10px;">
    <div style="font-size: 3em; margin-right: 20px;">⚙️</div>
    <div>
    <h4 style="margin: 0;">Put Your Investments on Autopilot</h4>
    <p style="margin: 0;">Set up recurring deductions directly from your salary. No hassle, no remembering to invest—just consistent, automated growth for your future.</p>
    </div>
    </div>
    </div>
    """, unsafe_allow_html=True)


# --- Why Invest in Qatar Section ---
st.markdown("---")
st.header("Why Investing from Qatar is Advantageous")

st.markdown("""
<div style="display: flex; align-items: center; margin-bottom: 20px;">
<div style="font-size: 3em; margin-right: 20px;">🛡️</div>
<div>
<h4 style="margin: 0;">Stable Currency Environment</h4>
<p>The Qatari Riyal's peg to the US Dollar provides a stable foundation for your investments, protecting your wealth from currency fluctuations and simplifying financial planning.</p>
</div>
</div>
<div style="display: flex; align-items: center;">
<div style="font-size: 3em; margin-right: 20px;">🌴</div>
<div>
<h4 style="margin: 0;">Tax-Free Growth</h4>
<p>Qatar's zero personal income tax policy means your investments grow unburdened by taxes on capital gains or dividends, maximizing your potential returns, as illustrated in the chart above.</p>
</div>
</div>
""", unsafe_allow_html=True)

st.button("Contact Us to Get Started", type="primary")