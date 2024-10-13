import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

## create_monthly_orders_df
def create_monthly_orders_df(df):
    monthly_orders_df = df.resample(rule="M", on="transaction_timestamp").agg({
        "order_id": "nunique",
        "price": "sum"
    })
    monthly_orders_df = monthly_orders_df.reset_index()
    monthly_orders_df.rename(columns={
        "order_id": "order_count",
        "price": "revenue"
    }, inplace=True)

    return monthly_orders_df

## create_sum_order_items_df
def create_sum_order_items_df(df):
    sum_order_items_df = df.groupby("product_category_name").count_order_id.sum().sort_values(ascending=False).reset_index()
    return sum_order_items_df 

all_df = pd.read_csv("all_data.csv")

## Mengurutkan Dataframe berdasarkan tanggal pesanan
datetime_columns = ["transaction_timestamp", 
                    "order_approved_at", 
                    "order_delivered_carrier_date", 
                    "order_delivered_customer_date",
                    "order_estimated_delivery_date",
                    "shipping_limit_date"
                ]
all_df.sort_values(by="transaction_timestamp", inplace=True)
all_df.reset_index(inplace=True)

for column in datetime_columns:
    all_df[column] = pd.to_datetime(all_df[column])

## Membuat komponen filter
min_date = all_df["transaction_timestamp"].min()
max_date = all_df["transaction_timestamp"].max()

with st.sidebar:
    ### Menambahkan logo
    st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")

    ### Mengambil start_date dan end_date dari date_input
    start_date, end_date = st.date_input(
        label="Rentang Waktu",
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

## Menyimpan data terfilter
main_df = all_df[(all_df["transaction_timestamp"] >= str(start_date)) &
                 (all_df["transaction_timestamp"] <= str(end_date))]

## Memanggil helper function
monthly_orders_df = create_monthly_orders_df(main_df)
sum_order_items = create_sum_order_items_df(main_df)

## Melengkapi Dashboard
# Visualisasi Pertanyaan 1
st.header("Dashboard Proyek Analisis Data :sparkles:")

st.subheader("Monthly Orders")

col1, col2 = st.columns(2)

with col1:
    total_orders = monthly_orders_df.order_count.sum()
    st.metric("Total Orders", value=total_orders)

with col2:
    total_revenue = format_currency(monthly_orders_df.revenue.sum(), "AUD", locale='es_CO') 
    st.metric("Total Revenue", value=total_revenue)

fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    monthly_orders_df["transaction_timestamp"],
    monthly_orders_df["order_count"],
    marker='o', 
    linewidth=2,
    color="#90CAF9"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)

st.pyplot(fig)

# Visualisasi Pertanyaan 2
st.subheader("Best & Worst Performing Product")

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(35, 15))
 
colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
 
sns.barplot(
    x="count_order_id", 
    y="product_category_name", 
    data=sum_order_items.head(5), 
    palette=colors, 
    ax=ax[0]
)
ax[0].set_ylabel(None)
ax[0].set_xlabel("Number of Sales", fontsize=30)
ax[0].set_title("Best Performing Product", loc="center", fontsize=50)
ax[0].tick_params(axis='y', labelsize=35)
ax[0].tick_params(axis='x', labelsize=30)
 
sns.barplot(
    x="count_order_id", 
    y="product_category_name", 
    data=sum_order_items.sort_values(by="count_order_id", ascending=True).head(5), 
    palette=colors, 
    ax=ax[1]
)
ax[1].set_ylabel(None)
ax[1].set_xlabel("Number of Sales", fontsize=30)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_title("Worst Performing Product", loc="center", fontsize=50)
ax[1].tick_params(axis='y', labelsize=35)
ax[1].tick_params(axis='x', labelsize=30)
 
st.pyplot(fig)