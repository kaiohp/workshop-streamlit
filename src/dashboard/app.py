import time

import pandas as pd
import plotly.express as px
import streamlit as st

from src.consumer.main import consume
from src.producer.main import regions, vendors

st.set_page_config(
    page_title="Workshop Streamlit - Real Time Dashboard",
    page_icon="📈",
    layout="wide",
)


@st.cache_data
def get_data():
    return pd.read_csv(
        "data/orders.csv",
        dtype={"region": "category", "vendor": "category"},
        parse_dates=["order_date"],
    )


df = get_data()


st.title("Workshop Streamlit - Real Time Dashboard")

with st.sidebar:
    st.header("Filters")
    vendor_filter = st.multiselect("Vendors", vendors)
    region_filter = st.multiselect("Regions", regions)

charts_placeholder = st.empty()

while True:

    with charts_placeholder.container():
        quantity, itens_sold, ticket, total = st.columns(4)

        quantity.metric(
            label="Orders",
            value=f"{len(df):,}",
        )

        itens_sold.metric(
            label="Items Sold",
            value=f"{df["quantity"].sum():,}",
        )

        ticket.metric(
            label="Average Ticket",
            value=f"R$ {df['total'].mean():,.2f}",
        )

        total.metric(
            label="Total Sold",
            value=f"R$ {df['total'].sum():,.2f}",
        )

        region_sales, vendor_sales = st.columns(2)

        with region_sales:
            st.subheader("Orders by Region")
            st.bar_chart(df, x="region", y="total")

        with vendor_sales:
            st.subheader("Orders by Vendor")
            st.bar_chart(df, x='vendor', y='total')


        st.subheader("Orders by Date")
        line_data = df.groupby(by=["order_date"])["total"].sum().reset_index().sort_values(by="order_date")
        line_fig = px.line(line_data, x="order_date", y="total")
        st.plotly_chart(line_fig, use_container_width=True)

        st.markdown("Detailed Data View")

        st.dataframe(df.iloc[::-1])

        new_order = consume()
        new_order_df = pd.DataFrame([new_order])
        new_order_df["order_date"] = pd.to_datetime(new_order_df["order_date"])
        df = pd.concat([df, new_order_df], ignore_index=True)
        time.sleep(1)
