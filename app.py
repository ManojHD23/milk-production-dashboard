import streamlit as st
import pandas as pd
import os

# File path to the enhanced CSV
data_path = "anomaly_with_profit_loss.csv"
plots_dir = "anomaly_plots"

# Load data
df = pd.read_csv(data_path)

# Sidebar
st.sidebar.title("🧮 Filter Societies")

# 🔹 1. Filter by Impact Type
impact_filter = st.sidebar.selectbox(
    "Filter by Impact Type",
    options=["All", "Profit", "Loss"]
)

# 🔹 2. Filter by Trend Rank
rank_limit = st.sidebar.slider("Limit to Top N Ranked Societies", 1, 20, 20)

# Apply filters
filtered_df = df.copy()
if impact_filter != "All":
    filtered_df = filtered_df[filtered_df["Impact Type"] == impact_filter]

filtered_df = filtered_df.sort_values(by="Trend Adherence Rank").head(rank_limit)

# 🔹 3. Society selection (from filtered list)
selected_society = st.sidebar.selectbox("Select Society to View", filtered_df['Society'].unique())

# Extract selected society info
soc_data = filtered_df[filtered_df['Society'] == selected_society].iloc[0]

# Title
st.title(f"📈 {selected_society} - Milk Production Analysis")

# KPI Cards
col1, col2, col3 = st.columns(3)
col1.metric("📦 Latest Production", f"{int(soc_data['Latest Production']):,} litres")
col2.metric("📊 Rolling Mean", f"{int(soc_data['Rolling Mean']):,} litres")
col3.metric("📉 Z-score", f"{soc_data['Z-score']:.2f}")

col4, col5, col6 = st.columns(3)
col4.metric("💸 Profit/Loss", f"₹{int(soc_data['Estimated Profit/Loss (INR)']):,}")
col5.metric("📌 Impact Type", soc_data['Impact Type'])
col6.metric("🏅 Trend Rank", int(soc_data['Trend Adherence Rank']))

# Show plot (if exists)
plot_path = os.path.join(plots_dir, f"{selected_society.replace(' ', '_')}_anomaly_plot.png")
if os.path.exists(plot_path):
    st.image(plot_path, caption=f"{selected_society} - Trend vs Deviation", use_container_width=True)
else:
    st.warning("⚠️ Plot not found.")

# 🔹 Download filtered data
st.subheader("📋 Filtered Society Summary")
st.dataframe(filtered_df.reset_index(drop=True))

csv = filtered_df.to_csv(index=False)
st.download_button("📥 Download Filtered Data as CSV", csv, "filtered_society_data.csv", "text/csv")

