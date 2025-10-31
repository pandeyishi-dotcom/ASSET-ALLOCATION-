import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# ---------------------------------------------------
# 🎯 PAGE CONFIG
# ---------------------------------------------------
st.set_page_config(page_title="Smart Asset Allocator", page_icon="💰", layout="wide")

st.title("💰 Smart Asset Allocation & Return Simulator")
st.caption("Diversify your investments and see projected returns based on age, risk, and horizon.")

# ---------------------------------------------------
# 🧠 USER INPUTS
# ---------------------------------------------------
col1, col2, col3 = st.columns(3)

with col1:
    age = st.slider("Select Your Age", 20, 70, 30)

with col2:
    risk = st.selectbox("Select Risk Profile", ["High", "Moderate", "Low"])

with col3:
    total_investment = st.number_input("Enter Total Investment (₹)", min_value=10000, step=10000, value=500000)

st.markdown("---")

# ---------------------------------------------------
# 📈 ASSET ALLOCATION FUNCTION
# ---------------------------------------------------
def allocate_assets(age, risk):
    assets = [
        "Large Cap Equity", "Mid/Small Cap Equity", "Debt Funds", "Gold ETF",
        "REITs/InvITs", "International Equity", "Cash/Liquid", "Govt Bonds",
        "Commodities", "Crypto (Regulated)", "Index Funds", "Hybrid Funds",
        "Thematic Funds", "Corporate Bonds"
    ]

    # Default weights (High Risk)
    weights = np.array([20, 18, 10, 8, 5, 10, 2, 5, 4, 3, 5, 3, 4, 3])

    if risk == "Moderate":
        weights = np.array([18, 12, 18, 8, 5, 8, 5, 8, 3, 0, 5, 5, 3, 2])
    elif risk == "Low":
        weights = np.array([10, 5, 25, 10, 5, 5, 10, 15, 3, 0, 5, 5, 1, 1])

    # Age adjustment (older investors => safer allocation)
    adjust = max(0, (age - 25) / 100)
    conservative = np.array([5, 3, 25, 10, 5, 3, 10, 20, 2, 0, 5, 4, 2, 6])
    weights = weights * (1 - adjust) + adjust * conservative
    weights = np.round(weights / weights.sum() * 100, 2)

    df = pd.DataFrame({"Asset Class": assets, "Allocation (%)": weights})
    return df

# ---------------------------------------------------
# 💹 EXPECTED RETURN FUNCTION
# ---------------------------------------------------
def expected_returns_table():
    return {
        "Large Cap Equity": 10,
        "Mid/Small Cap Equity": 13,
        "Debt Funds": 7,
        "Gold ETF": 6,
        "REITs/InvITs": 8,
        "International Equity": 9,
        "Cash/Liquid": 4,
        "Govt Bonds": 6,
        "Commodities": 8,
        "Crypto (Regulated)": 15,
        "Index Funds": 9,
        "Hybrid Funds": 8,
        "Thematic Funds": 11,
        "Corporate Bonds": 7
    }

# ---------------------------------------------------
# 🧮 GENERATE ALLOCATION + RETURNS
# ---------------------------------------------------
df = allocate_assets(age, risk)
returns_map = expected_returns_table()
df["Expected Return (%)"] = df["Asset Class"].map(returns_map)
df["Amount (₹)"] = np.round((df["Allocation (%)"] / 100) * total_investment, 0)

# Projected values (compound returns)
df["1-Year Projection (₹)"] = np.round(df["Amount (₹)"] * (1 + df["Expected Return (%)"] / 100), 0)
df["5-Year Projection (₹)"] = np.round(df["Amount (₹)"] * ((1 + df["Expected Return (%)"] / 100) ** 5), 0)

# ---------------------------------------------------
# 📊 DISPLAY ALLOCATION TABLE
# ---------------------------------------------------
st.subheader("📊 Recommended Portfolio Allocation & Return Forecast")

colA, colB = st.columns([1.4, 1])

with colA:
    st.dataframe(df, hide_index=True, use_container_width=True)

with colB:
    fig = px.pie(df, names="Asset Class", values="Allocation (%)", 
                 title="Portfolio Distribution", hole=0.4)
    st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------
# 📈 SUMMARY METRICS
# ---------------------------------------------------
st.markdown("---")
st.subheader("📈 Portfolio Summary")

total_1y = df["1-Year Projection (₹)"].sum()
total_5y = df["5-Year Projection (₹)"].sum()
gain_1y = total_1y - total_investment
gain_5y = total_5y - total_investment

col1, col2, col3 = st.columns(3)
col1.metric("Total Investment", f"₹{int(total_investment):,}")
col2.metric("Projected Value (1 Year)", f"₹{int(total_1y):,}", f"+₹{int(gain_1y):,}")
col3.metric("Projected Value (5 Years)", f"₹{int(total_5y):,}", f"+₹{int(gain_5y):,}")

# ---------------------------------------------------
# 🧭 ALLOCATION PHILOSOPHY
# ---------------------------------------------------
st.markdown("---")
st.subheader("🧭 Allocation Philosophy")

if risk == "High":
    st.info("""
    - Aggressive growth strategy with major equity exposure.  
    - Focused on long-term compounding through diversified equity themes.  
    - Small allocation to gold, bonds, and crypto for balance and optionality.  
    """)
elif risk == "Moderate":
    st.info("""
    - Balanced strategy between equity and debt.  
    - Seeks steady growth with limited drawdowns.  
    - Includes exposure to gold, hybrid, and REITs for stability.  
    """)
else:
    st.info("""
    - Conservative allocation for capital preservation.  
    - Higher share in bonds, debt, and gold.  
    - Minimal risk assets ensure predictable compounding.  
    """)

# ---------------------------------------------------
# 🕒 FOOTER
# ---------------------------------------------------
st.markdown("---")
st.caption("© 2025 Smart Asset Allocator | Projected returns are estimates based on average market data. Not financial advice.")
