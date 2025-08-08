import streamlit as st 
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from datetime import datetime

# Load the dataset
df = pd.read_csv("nigeria_inflation.csv")
df.rename(columns={"observation_date": "Date", "FPCPITOTLZGNGA": "CPI"}, inplace=True)
df["Date"] = pd.to_datetime(df["Date"])
df.sort_values("Date", inplace=True)

# Set page config
st.set_page_config(page_title="Inflation Impact Simulator", layout="wide")

# Sidebar - About section
with st.sidebar:
    st.markdown("""
    <h2>📊 Inflation Impact Simulator</h2>
    <p style='font-size:16px;'>Understand how inflation has affected your spending power in Nigeria over the last decade.</p>
    <h4> What is CPI?</h4>
    <p style='font-size:16px;'>The Consumer Price Index (CPI) tracks changes in the average prices of goods and services over time. A rising CPI indicates inflation — your money buys less than before.</p>
    <h4>📊 Understanding the CPI Trend</h4>
    <p style='font-size:16px;'>
    Over the last 10 years, Nigeria’s CPI has shown a steady upward trend. This means prices of everyday goods and services have been consistently rising.
    <br><br>
    - A rising CPI = inflation = reduced purchasing power.<br>
    - In Nigeria, this trend reflects the effects of naira devaluation, increased import costs, and fuel prices.<br>
    - For instance, what ₦1,000 bought 10 years ago may now cost over ₦4,000.<br>
    - A higher CPI over time means the value of your money in the past was greater than today.
    </p>

    <h4> Bag of Rice Example</h4>
    <div style='font-size:15px;'>
    Imagine you buy a <strong>bag of rice</strong> today for ₦60,000.<br><br>
    The simulator may show this equals ₦12,500 in the year 2000 based on CPI.<br><br>
    But real market records might show a bag cost ₦2,500 in 2000. Why the difference?<br><br>
    <strong>CPI</strong> is not about the actual price of rice—it's about how <em>money’s value</em> changes across many products.<br>
    It answers: "What was ₦60,000 worth back then, based on general price changes?"<br><br>
    ✔️ <i>Use this to understand inflation’s effect on purchasing power, not exact product prices.</i>
    </div>
    """, unsafe_allow_html=True)

# Welcome Message
st.markdown("""
<h1 style='text-align: center; font-size: 36px;'>🇳🇬 Nigerian Inflation Impact Simulator</h1>
<h3 style='text-align: center; font-size: 20px;'>👋 Welcome! Discover how inflation has shaped the value of money in Nigeria using CPI data.</h3>
""", unsafe_allow_html=True)

# Show 10-year average CPI change
latest_cpi = df["CPI"].iloc[-1]
ten_years_ago = df["Date"].max() - pd.DateOffset(years=10)
closest_past = df[df["Date"] <= ten_years_ago]["CPI"]
if not closest_past.empty:
    past_cpi = closest_past.iloc[-1]
else:
    past_cpi = df["CPI"].iloc[0]

cpi_change = ((latest_cpi - past_cpi) / past_cpi) * 100
st.metric("10-Year Average Inflation Rate", f"{cpi_change:.2f}%")

# CPI Trend chart
st.subheader("📈 Inflation Trend (CPI-Based)")
fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(df["Date"], df["CPI"], color="darkgreen")
ax.set_xlabel("Date")
ax.set_ylabel("CPI")
ax.set_title("CPI Trend Over Time", fontsize=14)
ax.grid(True)
ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'{int(x):,}'))
st.pyplot(fig)

# Category-wise spending input with subcategory dropdowns
st.markdown("<h2 style='margin-top:30px;'>🛒 Predict Today's Value Compared to a Past Year</h2>", unsafe_allow_html=True)
st.markdown("<p style='font-size:16px;'>Estimate how much your money could buy in a selected past year by entering your current spending.</p>", unsafe_allow_html=True)

# Year selection
years = df["Date"].dt.year.unique().tolist()
years.sort(reverse=True)
comparison_year = st.selectbox("Select a year to compare with", years[1:], index=years.index(datetime.now().year - 10))

# Get CPI for comparison year
if comparison_year in df["Date"].dt.year.values:
    past_cpi_year = df[df["Date"].dt.year == comparison_year]["CPI"].mean()
else:
    st.error("Selected comparison year is not available in the dataset.")

# Subcategory dropdowns and inputs
category_inputs = {}

categories = {
    "Food": ["Bag of Rice", "Bread", "Chicken", "Yam", "Beans"],
    "Transport": ["Fuel", "Public Transport", "Taxi"],
    "Housing": ["Rent", "Maintenance", "Mortgage"],
    "Clothing": ["Casual Wear", "Formal Wear", "Shoes"],
    "Education": ["Tuition", "Books", "Stationery"],
    "Health": ["Drugs", "Hospital Bills", "Insurance"],
    "Electronics": ["Phone", "Laptop", "TV", "Tablet"]
}

col1, col2, col3 = st.columns(3)
with col1:
    for cat in ["Food", "Transport"]:
        sub = st.selectbox(f"Select a subcategory for {cat}", categories[cat], key=f"{cat}_sub")
        val = st.number_input(f"{cat} - {sub}", min_value=0.0, value=10000.0, step=100.0, key=f"{cat}_input")
        category_inputs[f"{cat} ({sub})"] = val

with col2:
    for cat in ["Housing", "Clothing"]:
        sub = st.selectbox(f"Select a subcategory for {cat}", categories[cat], key=f"{cat}_sub")
        val = st.number_input(f"{cat} - {sub}", min_value=0.0, value=10000.0, step=100.0, key=f"{cat}_input")
        category_inputs[f"{cat} ({sub})"] = val

with col3:
    for cat in ["Education", "Health", "Electronics"]:
        sub = st.selectbox(f"Select a subcategory for {cat}", categories[cat], key=f"{cat}_sub")
        val = st.number_input(f"{cat} - {sub}", min_value=0.0, value=10000.0, step=100.0, key=f"{cat}_input")
        category_inputs[f"{cat} ({sub})"] = val

# Prediction
if st.button(" Predict Past Value"):
    total_today = sum(category_inputs.values())
    total_past = (total_today * past_cpi_year) / latest_cpi

    st.success(f"That amount had the value of approximately ₦{total_past:,.2f} in {comparison_year}.")

    st.markdown("""
    #### 💡 What This Means
    CPI has increased from {:.0f} to {:.0f} between {} and {}.  
    This means ₦{:,} today had the buying power of ₦{:,.2f} in {}.

    In simple terms:
    > Prices have more than doubled in the last decade — a reflection of Nigeria’s inflation challenges.
    """.format(
        past_cpi_year,
        latest_cpi,
        comparison_year,
        df["Date"].max().strftime('%Y'),
        int(total_today),
        total_past,
        comparison_year
    ))

    # Show per-category past values
    st.subheader(" Breakdown by Category")
    for category, amount in category_inputs.items():
        old_value = amount * past_cpi_year / latest_cpi
        st.markdown(f"- **{category}**: ₦{amount:,.2f} today ≈ ₦{old_value:,.2f} in {comparison_year}")

    # Bar chart comparison
    st.subheader("Spending Comparison: Today vs Past")
    past_values = [amount * past_cpi_year / latest_cpi for amount in category_inputs.values()]
    labels = list(category_inputs.keys())
    fig2, ax2 = plt.subplots()
    bar_width = 0.35
    x = range(len(labels))
    ax2.bar(x, list(category_inputs.values()), width=bar_width, label="Today", color="gray")
    ax2.bar([i + bar_width for i in x], past_values, width=bar_width, label=f"{comparison_year}")
    ax2.set_xticks([i + bar_width / 2 for i in x])
    ax2.set_xticklabels(labels, rotation=45, ha="right")
    ax2.set_ylabel("₦ Value")
    ax2.set_title("Monthly Spending Comparison")
    ax2.legend()
    ax2.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'{int(x):,}'))
    st.pyplot(fig2)

# Recommendations
st.subheader("Recommendations")
st.markdown("""
- Review your savings plan regularly to factor in inflation.
- Invest in inflation-resistant assets like real estate, stocks, or commodities.
- Diversify your income sources to cushion against inflation shocks.
- Monitor economic policies and global trends that affect inflation in Nigeria.
- Use budgeting apps to track the real value of your expenses over time.
""")
