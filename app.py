import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.io as pio

# Better chart theme
pio.templates.default = "plotly_dark"

# Page setup
st.set_page_config(
    page_title="Airbnb Market Intelligence Dashboard",
    layout="wide"
)

st.title("Airbnb Market Intelligence Dashboard")
st.markdown(
"Interactive analytics for pricing trends, demand patterns, and geographic distribution."
)

#Load Data 

df = pd.read_csv("Airbnb_Open_Data.csv", low_memory=False)

# Data Cleaning

df["price"] = df["price"].replace(r"[\$,]", "", regex=True)
df["price"] = pd.to_numeric(df["price"], errors="coerce")

df["number of reviews"] = pd.to_numeric(df["number of reviews"], errors="coerce")
df["availability 365"] = pd.to_numeric(df["availability 365"], errors="coerce")

df = df[
    (df["price"].notna()) &
    (df["number of reviews"].notna()) &
    (df["availability 365"].notna()) &
    (df["availability 365"] >= 0)
]

# Sidebar Filters 

st.sidebar.header("Filters")

room_type = st.sidebar.selectbox(
    "Select Room Type",
    df["room type"].dropna().unique()
)

price_range = st.sidebar.slider(
    "Select Price Range",
    int(df["price"].min()),
    int(df["price"].max()),
    (100, 800)
)

filtered_df = df[
    (df["room type"] == room_type) &
    (df["price"] >= price_range[0]) &
    (df["price"] <= price_range[1])
]

#  KPI Metrics 

col1, col2, col3, col4 = st.columns(4)

col1.metric("📊 Total Listings", len(filtered_df))
col2.metric("💰 Avg Price", f"${filtered_df['price'].mean():.2f}")
col3.metric("⭐ Avg Reviews", round(filtered_df["number of reviews"].mean(), 2))
col4.metric("📅 Avg Availability", round(filtered_df["availability 365"].mean(), 2))

st.divider()
st.markdown("## 📌 Executive Summary")

st.info("""
🔹 Entire homes generate the highest revenue potential  
🔹 Mid-range pricing ($300–$700) drives maximum demand  
🔹 Manhattan dominates premium listings  
🔹 Opportunity: Optimize pricing in mid-tier segments for higher occupancy  
""")

# Pricing Insights 

st.header("💰 Revenue Analysis")

colA, colB = st.columns(2)

with colA:

    fig_price = px.box(
        filtered_df,
        x="room type",
        y="price",
        color="room type",
        title="Price Distribution by Room Type",
        color_discrete_sequence=px.colors.qualitative.Bold
    )

    st.plotly_chart(fig_price, width="stretch")


with colB:

    avg_price_location = (
        filtered_df.groupby("neighbourhood group")["price"]
        .mean()
        .reset_index()
        .sort_values("price", ascending=False)
    )

    fig_location_price = px.bar(
        avg_price_location,
        x="neighbourhood group",
        y="price",
        color="price",
        title="Average Price by Neighborhood",
        color_continuous_scale="Turbo"
    )

    st.plotly_chart(fig_location_price, width="stretch")

#  Demand Insights 

st.header("📈 Customer Demand Behavior")

scatter_df = filtered_df.dropna(
    subset=["number of reviews", "price", "availability 365"]
)

fig_demand = px.scatter(
    scatter_df,
    x="number of reviews",
    y="price",
    size="availability 365",
    color="room type",
    hover_data=["neighbourhood group"],
    title="Demand vs Price Relationship",
    color_discrete_sequence=px.colors.qualitative.Set2
)

st.plotly_chart(fig_demand, width="stretch")

#  Revenue Opportunity 
st.header("Revenue Opportunity Analysis")

revenue_df = (
    filtered_df.groupby("neighbourhood group")
    .agg(
        avg_price=("price","mean"),
        demand=("number of reviews","mean")
    )
    .reset_index()
)

fig_revenue = px.scatter(
    revenue_df,
    x="demand",
    y="avg_price",
    size="avg_price",
    color="neighbourhood group",
    title="Revenue Opportunity Matrix"
)

st.plotly_chart(fig_revenue, width="stretch")

# Supply Analysis 

st.header("🏙 Market Supply Distribution")

supply_data = filtered_df["neighbourhood group"].value_counts().reset_index()
supply_data.columns = ["Neighborhood","Listings"]

fig_supply = px.bar(
    supply_data,
    x="Neighborhood",
    y="Listings",
    color="Listings",
    title="Airbnb Listings by Neighborhood",
    color_continuous_scale="Plasma"
)

st.plotly_chart(fig_supply, width="stretch")

# Market Share 

st.header("Market Share of Listings")

fig_market = px.pie(
    supply_data,
    names="Neighborhood",
    values="Listings",
    hole=0.45,
    title="Airbnb Market Share by Neighborhood",
    color_discrete_sequence=px.colors.qualitative.Bold
)

st.plotly_chart(fig_market, width="stretch")

# Geographic Distribution 

st.header("🌍 Geographic Intelligence")

map_df = filtered_df[["lat","long","price"]].dropna()

fig_map = px.scatter_map(
    map_df,
    lat="lat",
    lon="long",
    color="price",
    size="price",
    zoom=9,
    title="Airbnb Listing Locations"
)

st.plotly_chart(fig_map, width="stretch")

# Business Insights 

st.header("📊 Key Business Insights")

st.markdown("""
### 🔍 Key Findings

• Entire home listings consistently command **premium pricing**, indicating higher revenue potential compared to other room types.  

• **Manhattan and Brooklyn dominate the market**, showing strong supply concentration and higher competitive intensity.  

• Listings priced in the **$300–$700 range achieve the highest engagement**, suggesting optimal pricing for demand capture.  

• Several neighborhoods exhibit **high demand with moderate pricing**, highlighting opportunities for revenue optimization.  


### 🚀 Strategic Recommendations

• Focus on **mid-range pricing strategies** to balance occupancy and revenue generation.  

• Use **dynamic pricing models** in high-demand locations to maximize returns.  

• In competitive markets, differentiate listings through **amenities, reviews, and positioning**.  

• Target high-review neighborhoods as they indicate **consistent and reliable customer demand**.  
""")