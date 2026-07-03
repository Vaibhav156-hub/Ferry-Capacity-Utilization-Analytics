import streamlit as st
import pandas as pd
import numpy as np

import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Ferry Capacity Utilization Dashboard",
    page_icon="🚢",
    layout="wide"
)

# ---------------- CSS ----------------

st.markdown("""
<style>

.main{
background-color:#f8f9fa;
}

h1,h2,h3{
color:#003566;
}

[data-testid="stMetricValue"]{
font-size:28px;
font-weight:bold;
color:#1d3557;
}

.css-1d391kg{
background:#003566;
}

</style>

""",unsafe_allow_html=True)

# ---------------- Load Data ----------------

@st.cache_data
def load_data():

    df=pd.read_csv("final_ferry_dataset.csv")

    df["Timestamp"]=pd.to_datetime(df["Timestamp"])

    return df

df=load_data()

# ---------------- Sidebar ----------------

st.sidebar.image(
"https://img.icons8.com/color/96/ferry.png",
width=80
)

st.sidebar.title("Navigation")

page=st.sidebar.radio(

"Select Module",

[
"🏠 Home",
"📊 KPI Dashboard",
"📈 Activity Analysis",
"⏰ Time Analysis",
"🌦 Seasonal Analysis",
"🚦 Operational Analysis",
"📉 Correlation",
"📋 Dataset Explorer",
"📄 Business Insights"

]

)

# ---------------- Filters ----------------

st.sidebar.markdown("---")

years=sorted(df["Year"].unique())

selected_year=st.sidebar.multiselect(

"Year",

years,

default=years

)

season=sorted(df["Season"].unique())

selected_season=st.sidebar.multiselect(

"Season",

season,

default=season

)

filtered=df[
(df["Year"].isin(selected_year))&
(df["Season"].isin(selected_season))
]

# ---------------- HOME ----------------

if page=="🏠 Home":

    st.title("🚢 Ferry Capacity Utilization & Operational Efficiency Analytics System")

    st.markdown("""

This dashboard analyzes Toronto Island Ferry ticket activity from **2015–2025**.

It helps identify:

- Capacity Utilization
- Congestion Periods
- Idle Capacity
- Seasonal Demand
- Operational Efficiency
- Passenger Activity Trends

""")

    col1,col2,col3,col4=st.columns(4)

    col1.metric(
        "Total Records",
        len(filtered)
    )

    col2.metric(
        "Years",
        filtered["Year"].nunique()
    )

    col3.metric(
        "Total Sales",
        format(filtered["Sales Count"].sum(),",")
    )

    col4.metric(
        "Total Redemption",
        format(filtered["Redemption Count"].sum(),",")
    )

    st.markdown("---")

    daily=filtered.groupby("Timestamp")["Total Activity Load"].sum().reset_index()

    fig=px.line(

        daily,

        x="Timestamp",

        y="Total Activity Load",

        title="Overall Ferry Activity Timeline"

    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ---------------- KPI ----------------

elif page=="📊 KPI Dashboard":

    st.title("📊 Key Performance Indicators")

    c1,c2,c3,c4=st.columns(4)

    c1.metric(
        "Total Sales",
        format(filtered["Sales Count"].sum(),",")
    )

    c2.metric(
        "Total Redemption",
        format(filtered["Redemption Count"].sum(),",")
    )

    c3.metric(
        "Total Activity",
        format(filtered["Total Activity Load"].sum(),",")
    )

    c4.metric(
        "Average OLI",
        round(filtered["Operational Load Index"].mean(),2)
    )

    st.markdown("---")

    c5,c6,c7,c8=st.columns(4)

    congestion=round(

        filtered["Congestion"].mean()*100,

        2

    )

    idle=round(

        filtered["Idle Capacity"].mean()*100,

        2

    )

    c5.metric(
        "Congestion %",
        str(congestion)+"%"
    )

    c6.metric(
        "Idle Capacity %",
        str(idle)+"%"
    )

    peak_hour=filtered.groupby("Hour")["Total Activity Load"].mean().idxmax()

    c7.metric(
        "Peak Hour",
        str(peak_hour)+":00"
    )

    peak_day=filtered.groupby("Day_Name")["Total Activity Load"].mean().idxmax()

    c8.metric(
        "Peak Day",
        peak_day
    )

    st.markdown("---")

    monthly=filtered.groupby("Month_Name")["Total Activity Load"].sum().reset_index()

    order=[
    "January","February","March","April","May","June",
    "July","August","September","October","November","December"
    ]

    monthly["Month_Name"]=pd.Categorical(
        monthly["Month_Name"],
        order
    )

    monthly=monthly.sort_values("Month_Name")

    fig=px.bar(

        monthly,

        x="Month_Name",

        y="Total Activity Load",

        color="Total Activity Load"

    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )
    # ==========================
# ACTIVITY ANALYSIS
# ==========================

elif page=="📈 Activity Analysis":

    st.title("📈 Activity Analysis")

    activity = filtered.groupby("Hour")["Total Activity Load"].mean().reset_index()

    fig = px.line(
        activity,
        x="Hour",
        y="Total Activity Load",
        markers=True,
        title="Average Activity by Hour"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    day = filtered.groupby("Day_Name")["Total Activity Load"].mean().reset_index()

    order = [
        "Monday","Tuesday","Wednesday",
        "Thursday","Friday","Saturday","Sunday"
    ]

    day["Day_Name"] = pd.Categorical(day["Day_Name"], order)

    day = day.sort_values("Day_Name")

    fig = px.bar(
        day,
        x="Day_Name",
        y="Total Activity Load",
        color="Total Activity Load",
        title="Average Activity by Day"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    monthly = filtered.groupby("Month_Name")["Total Activity Load"].mean().reset_index()

    months = [
        "January","February","March","April","May","June",
        "July","August","September","October","November","December"
    ]

    monthly["Month_Name"] = pd.Categorical(monthly["Month_Name"], months)

    monthly = monthly.sort_values("Month_Name")

    fig = px.area(
        monthly,
        x="Month_Name",
        y="Total Activity Load",
        title="Monthly Activity Trend"
    )

    st.plotly_chart(fig, use_container_width=True)

# ==========================
# TIME ANALYSIS
# ==========================

elif page=="⏰ Time Analysis":

    st.title("⏰ Time Based Analysis")

    col1,col2=st.columns(2)

    hourly_sales = filtered.groupby("Hour")["Sales Count"].sum().reset_index()

    fig = px.bar(
        hourly_sales,
        x="Hour",
        y="Sales Count",
        color="Sales Count",
        title="Hourly Ticket Sales"
    )

    col1.plotly_chart(fig,use_container_width=True)

    hourly_redemption = filtered.groupby("Hour")["Redemption Count"].sum().reset_index()

    fig = px.line(
        hourly_redemption,
        x="Hour",
        y="Redemption Count",
        markers=True,
        title="Hourly Ticket Redemption"
    )

    col2.plotly_chart(fig,use_container_width=True)

    st.markdown("---")

    band = filtered.groupby("Time Band")["Total Activity Load"].mean().reset_index()

    order = ["Morning","Afternoon","Evening","Night"]

    band["Time Band"] = pd.Categorical(
        band["Time Band"],
        order
    )

    band = band.sort_values("Time Band")

    fig = px.bar(
        band,
        x="Time Band",
        y="Total Activity Load",
        color="Time Band",
        title="Activity by Time Band"
    )

    st.plotly_chart(fig,use_container_width=True)

# ==========================
# SEASONAL ANALYSIS
# ==========================

elif page=="🌦 Seasonal Analysis":

    st.title("🌦 Seasonal Analysis")

    season = filtered.groupby("Season")["Total Activity Load"].mean().reset_index()

    fig = px.pie(
        season,
        names="Season",
        values="Total Activity Load",
        hole=0.4,
        title="Season Wise Activity"
    )

    st.plotly_chart(fig,use_container_width=True)

    st.markdown("---")

    weekend = filtered.groupby("Weekend")["Total Activity Load"].mean().reset_index()

    weekend["Weekend"] = weekend["Weekend"].replace({
        True:"Weekend",
        False:"Weekday"
    })

    fig = px.bar(
        weekend,
        x="Weekend",
        y="Total Activity Load",
        color="Weekend",
        title="Weekend vs Weekday Activity"
    )

    st.plotly_chart(fig,use_container_width=True)
    # ==========================
# OPERATIONAL ANALYSIS
# ==========================

elif page=="🚦 Operational Analysis":

    st.title("🚦 Operational Efficiency Analysis")

    col1,col2=st.columns(2)

    congestion=filtered["Congestion"].value_counts().reset_index()
    congestion.columns=["Status","Count"]

    congestion["Status"]=congestion["Status"].replace({
        1:"Congestion",
        0:"Normal"
    })

    fig=px.pie(
        congestion,
        names="Status",
        values="Count",
        hole=0.45,
        title="Congestion Distribution"
    )

    col1.plotly_chart(fig,use_container_width=True)

    idle=filtered["Idle Capacity"].value_counts().reset_index()
    idle.columns=["Status","Count"]

    idle["Status"]=idle["Status"].replace({
        1:"Idle",
        0:"Active"
    })

    fig=px.pie(
        idle,
        names="Status",
        values="Count",
        hole=0.45,
        title="Idle Capacity Distribution"
    )

    col2.plotly_chart(fig,use_container_width=True)

    st.markdown("---")

    activity=filtered.groupby("Activity Category")["Total Activity Load"].mean().reset_index()

    fig=px.bar(
        activity,
        x="Activity Category",
        y="Total Activity Load",
        color="Activity Category",
        title="Activity Categories"
    )

    st.plotly_chart(fig,use_container_width=True)

    st.markdown("---")

    fig=px.histogram(
        filtered,
        x="Operational Load Index",
        nbins=40,
        title="Operational Load Index Distribution"
    )

    st.plotly_chart(fig,use_container_width=True)

# ==========================
# CORRELATION
# ==========================

elif page=="📉 Correlation":

    st.title("📉 Correlation Analysis")

    corr=filtered.select_dtypes(include="number").corr()

    fig=px.imshow(
        corr,
        text_auto=".2f",
        aspect="auto",
        color_continuous_scale="RdBu_r"
    )

    st.plotly_chart(fig,use_container_width=True)

# ==========================
# DATA EXPLORER
# ==========================

elif page=="📋 Dataset Explorer":

    st.title("📋 Dataset Explorer")

    st.write("Dataset Shape:",filtered.shape)

    st.dataframe(filtered)

    st.markdown("---")

    st.subheader("Dataset Statistics")

    st.dataframe(filtered.describe())

    csv=filtered.to_csv(index=False).encode("utf-8")

    st.download_button(
        "📥 Download Filtered Dataset",
        csv,
        "Filtered_Ferry_Data.csv",
        "text/csv"
    )

# ==========================
# BUSINESS INSIGHTS
# ==========================

elif page=="📄 Business Insights":

    st.title("📄 Business Insights & Recommendations")

    st.subheader("Key Insights")

    st.success("""
✔ Peak passenger activity occurs during specific hours of the day.

✔ Operational load changes significantly across seasons.

✔ Congestion is concentrated in a limited number of intervals.

✔ Idle-capacity periods indicate opportunities for operational optimization.

✔ Historical data supports evidence-based scheduling decisions.
""")

    st.subheader("Recommendations")

    st.info("""
• Increase ferry frequency during peak hours.

• Reduce services during sustained idle periods.

• Optimize staffing based on seasonal demand.

• Continuously monitor Operational Load Index (OLI).

• Develop predictive models for passenger demand forecasting.
""")

    st.markdown("---")

    st.subheader("Project Summary")

    st.write("""
The Ferry Capacity Utilization & Operational Efficiency Analytics System
uses historical ticket sales and redemption data to evaluate operational
performance, identify congestion and idle-capacity periods, and support
data-driven decision-making for ferry scheduling and resource allocation.
""")

    st.markdown("---")

    st.caption("Developed using Python • Streamlit • Plotly • Pandas")
    