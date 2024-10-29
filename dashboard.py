import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set_theme(style='dark')

## create_monthly_trend_df
def create_monthly_trend_df(df):
    monthly_trend_df = df.groupby(pd.Grouper(key="date", freq="M")).agg({"total_users":"sum"}).sort_index()
    monthly_trend.index = monthly_trend.index.strftime("%b %Y")

    monthly_trend = monthly_trend.reset_index()

    return monthly_trend_df

## create_seasonal_df
def create_seasonal_df(df):
    seasonal_df = df.groupby(by=["month", "season"]).agg({"total_users":"sum"}).sort_index()
    return seasonal_df 

## create_peak_hour_df
def create_peak_hour_df(df):
    peak_hour = df.groupby(by="hour_interval").agg({"total_users":"sum"}).sort_index()
    
    peak_hour = peak_hour.reset_index()
    
    peak_hour_sorted = peak_hour.sort_values(by="total_users", ascending=False)

    return peak_hour_sorted

all_df = pd.read_csv("all_data.csv")

## Filter 
min_date = all_df["date"].min()
max_date = all_df["date"].max()

with st.sidebar:
    ### Add Logo
    st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")

    ### Take start_date and end_date from date_input
    start_date, end_date = st.date_input(
        label="Date Range",
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

## Store filtered data
main_df = all_df[(all_df["date"] >= str(start_date)) &
                 (all_df["date"] <= str(end_date))]

## Use helper function
monthly_trend_df = create_monthly_trend_df(main_df)
seasonal_df = create_seasonal_df(main_df)
peak_hour_df = create_peak_hour_df(main_df)

# Question 1 
st.header("Bike Sharing Dashboard :sparkles:")

st.subheader("Monthly Trend")

col1, col2 = st.columns(2)

with col1:
    casual_users = monthly_trend_df.casual.sum()
    st.metric("Casual Users", value=casual_users)

with col2:
    registered_users = monthly_trend_df.registered.sum()
    st.metric("Registered Users", value=registered_users)

trend_fig, ax = plt.subplots(figsize=(10, 5))

ax.plot(
    monthly_trend_df["date"], 
    monthly_trend_df["total_users"], 
    marker="o",
    linestyle="-",
    linewidth=2,
    color="#4682B4" 
)

max_index = monthly_trend_df["total_users"].idxmax()
ax.scatter(monthly_trend_df["date"].iloc[max_index], monthly_trend_df["total_users"].iloc[max_index],
            color="green",
            s=100,
            edgecolors="green",
            zorder=5,
            label="Peak")

ax.axhline(monthly_trend_df["total_users"].mean(), 
            color="red", 
            linestyle="--",
            linewidth=1,
            label="Average",
)

ax.axvline(monthly_trend_df["date"].iloc[max_index], 
            color="grey", 
            linestyle=":",
            linewidth=1)

ax.set_title(
    "Monthly Trend of Total Users in 2011 - 2012", 
    loc="center",
    pad=10,
    fontsize=20,
    fontweight="bold"
)

ax.tick_params(axis="x", rotation=45, labelsize=10)
ax.tick_params(axis="y", labelsize=10)

yticks = ax.get_yticks()
ax.set_yticks(yticks)
ax.set_yticklabels([f"{int(x/1000)}K" for x in yticks])

ax.set_ylabel("Number of Users")

ax.grid(axis="y", which="both", linestyle="--", alpha=0.5)
ax.legend(loc="upper left")

st.pyplot(trend_fig)

# Question 2 
st.subheader("Most Popular Season for Cycling")

season_fig, ax = plt.subplots(figsize=(10, 5))

max_value = seasonal_df["total_users"].max() 

colors = ["#4682B4" if value == max_value else "grey" for value in seasonal_df["total_users"]]

sns.barplot(
    x="total_users", 
    y="season", 
    data=seasonal_df,
    order=seasonal_df["season"],
    palette=colors
)

xticks = ax.get_xticks()
ax.set_xticks(xticks)
ax.set_xticklabels([f"{int(x/1000)}K" for x in xticks])

plt.title("Most Popular Season for Cycling", 
          loc="center", 
          fontsize=15,
          fontweight="bold",
          pad=10
)

plt.ylabel(None)
plt.xlabel("Number of Users")
 
st.pyplot(season_fig)

# Question 3
st.subheader("Peak Hour")

peak_hour_fig, ax = plt.subplots(nrows=1, figsize=(10, 5))

mean_users = peak_hour_df["total_users"].mean()

colors_hour = ["#4682B4" if value > mean_users else "grey" for value in peak_hour_df["total_users"]]

for i, (hour_interval, total_users) in enumerate(zip(peak_hour_df["hour_interval"], peak_hour_df["total_users"])):
    ax.bar(hour_interval, total_users, color=colors_hour[i], width=0.95)

ax.axhline(mean_users, 
            color="red", 
            linestyle="--",
            linewidth=1,
            label="Average",
)

yticks = ax.get_yticks()
ax.set_yticks(yticks)
ax.set_yticklabels([f"{int(x/1000)}K" for x in yticks])

ax.set_title("Peak Hour", 
          loc="center", 
          fontsize=15,
          fontweight="bold",
          pad=10
)

ax.tick_params(axis="x", rotation=45)
ax.set_xlabel("Hour Interval")
ax.set_ylabel("Number of Users")

ax.legend(loc="upper left")

st.pyplot(peak_hour_fig)