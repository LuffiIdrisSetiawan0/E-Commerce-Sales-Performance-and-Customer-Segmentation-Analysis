import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load Dataset
monthly_sales = pd.read_csv('monthly_sales.csv')
product_summary = pd.read_csv('product_summary.csv')
city_sales = pd.read_csv('city_sales.csv')
new_customers_trend = pd.read_csv('new_customers_trend.csv')

# Set Streamlit page config
st.set_page_config(page_title="E-commerce Dashboard", layout="wide")

# Dashboard Title
st.title("📊 E-commerce Sales Dashboard")

# Sidebar Peringatan
st.sidebar.header("Filter Data")
st.sidebar.markdown("⚠ **Perubahan tanggal hanya memengaruhi visualisasi Sales Performance dan Monthly New Customer Growth**.")

# Sidebar Tanggal
st.sidebar.header("Filter Data")
start_date = st.sidebar.date_input("Start Date", pd.to_datetime('2017-01-01'))
end_date = st.sidebar.date_input("End Date", pd.to_datetime('2018-08-31'))

# Konversi filter ke string period
start_period = pd.to_datetime(start_date).strftime('%Y-%m')
end_period = pd.to_datetime(end_date).strftime('%Y-%m')

# Filter data berdasarkan periode
monthly_sales_filtered = monthly_sales[(monthly_sales['year_month'] >= start_period) & 
                                       (monthly_sales['year_month'] <= end_period)]
new_customers_filtered = new_customers_trend[(new_customers_trend['year_month'] >= start_period) & 
                                             (new_customers_trend['year_month'] <= end_period)]

# Layout
tab1, tab2, tab3 = st.tabs(["📈 Sales Performance", "📦 Product Insights", "📍 Customer Insights"])

# ===================== TAB 1: Sales Performance =====================

with tab1:
    st.subheader("Monthly Total Revenue")
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(monthly_sales_filtered['year_month'], monthly_sales_filtered['total_revenue'], 
            marker='o', color='#87CEEB', label='Total Revenue (BRL)')

    # Highlight Peak Month
    peak_month = monthly_sales_filtered.loc[monthly_sales_filtered['total_revenue'].idxmax()]
    ax.scatter(peak_month['year_month'], peak_month['total_revenue'], 
               color='#FF5733', s=120, zorder=5, label='Peak Revenue')

    ax.set_xticks(monthly_sales_filtered['year_month'])
    ax.set_xticklabels(monthly_sales_filtered['year_month'], rotation=45)
    ax.set_ylabel("Total Revenue (BRL)")
    ax.set_title("Monthly Total Revenue - Delivered Orders Only")
    plt.yticks(ticks=plt.yticks()[0], labels=[f'R${int(y):,}' for y in plt.yticks()[0]])
    ax.legend()
    plt.box(False)
    ax.grid(axis='x', linestyle='--', alpha=0.7)
    st.pyplot(fig)

    st.subheader("Monthly Total Orders")
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(monthly_sales_filtered['year_month'], monthly_sales_filtered['total_orders'], 
            marker='o', color='#87CEEB', label='Total Orders')

    peak_orders_month = monthly_sales_filtered.loc[monthly_sales_filtered['total_orders'].idxmax()]
    ax.scatter(peak_orders_month['year_month'], peak_orders_month['total_orders'], 
               color='#FF5733', s=120, zorder=5, label='Peak Orders')

    ax.set_xticks(monthly_sales_filtered['year_month'])
    ax.set_xticklabels(monthly_sales_filtered['year_month'], rotation=45)
    ax.set_ylabel("Total Orders")
    ax.set_title("Monthly Total Orders - Delivered Orders Only")
    ax.legend()
    plt.box(False)
    ax.grid(axis='x', linestyle='--', alpha=0.7)
    st.pyplot(fig)

# ===================== TAB 2: Product Insights =====================

with tab2:
    st.subheader("Top 10 Product Categories by Revenue")
    top10_revenue = product_summary.sort_values(by='total_revenue', ascending=False).head(10)

    fig, ax = plt.subplots(figsize=(12, 6))
    colors = ['#FF5733' if i == 0 else '#87CEEB' for i in range(len(top10_revenue))]
    bars = ax.barh(top10_revenue['product_category_name_english'], top10_revenue['total_revenue'], color=colors)

    ax.set_xlabel("Total Revenue (BRL)")
    ax.set_title("Top 10 Product Categories by Revenue")
    ax.invert_yaxis()
    plt.box(False)

    for bar in bars:
        ax.text(bar.get_width(), bar.get_y() + bar.get_height() / 2,
                f'R${bar.get_width():,.0f}', va='center', ha='left', fontsize=9)

    st.pyplot(fig)

    st.subheader("Top 10 Product Categories by Total Items Sold")
    top10_items = product_summary.sort_values(by='total_items_sold', ascending=False).head(10)

    fig, ax = plt.subplots(figsize=(12, 6))
    colors = ['#FF5733' if i == 0 else '#87CEEB' for i in range(len(top10_items))]
    bars = ax.barh(top10_items['product_category_name_english'], top10_items['total_items_sold'], color=colors)

    ax.set_xlabel("Total Items Sold")
    ax.set_title("Top 10 Product Categories by Total Items Sold")
    ax.invert_yaxis()
    plt.box(False)

    for bar in bars:
        ax.text(bar.get_width(), bar.get_y() + bar.get_height() / 2,
                f'{int(bar.get_width()):,}', va='center', ha='left', fontsize=9)

    st.pyplot(fig)

# ===================== TAB 3: Customer Insights =====================

with tab3:
    st.subheader("Top Cities by Total Orders")
    top10_cities = city_sales.sort_values(by='total_orders', ascending=False).head(10)

    fig, ax = plt.subplots(figsize=(12, 6))
    colors = ['#FF5733' if i == 0 else '#87CEEB' for i in range(len(top10_cities))]
    bars = ax.barh(top10_cities['customer_city'], top10_cities['total_orders'], color=colors)

    ax.set_xlabel("Total Orders")
    ax.set_title("Top 10 Cities by Total Orders")
    ax.invert_yaxis()
    plt.box(False)

    for bar in bars:
        ax.text(bar.get_width(), bar.get_y() + bar.get_height() / 2,
                f'{int(bar.get_width()):,}', va='center', ha='left', fontsize=9)

    st.pyplot(fig)


    st.subheader("Top Cities 15 by Total Orders Clustering")
    city_sales_sorted = city_sales.sort_values(by='total_orders', ascending=False).head(15)

    color_map = {
        'Low': 'skyblue',
        'Medium': 'orange',
        'High': 'tomato',
    }

    colors = city_sales_sorted['order_category'].map(color_map)

    fig, ax = plt.subplots(figsize=(12, 6))
    bars = plt.barh(city_sales_sorted['customer_city'], city_sales_sorted['total_orders'], color=colors)

    ax.set_xlabel('Total Orders', fontsize=12, labelpad=10)
    ax.set_title('Top Cities 15 by Total Orders Clustering', fontsize=14, weight='bold', pad=15)
    plt.gca().invert_yaxis()

    for bar in bars:
        plt.text(bar.get_width(), bar.get_y() + bar.get_height()/2, 
                f'{bar.get_width():,}', 
                va='center', ha='left', fontsize=9)

    plt.box(False)
    st.pyplot(fig)
    
    
    st.subheader("Monthly New Customer Growth")
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(new_customers_filtered['year_month'], new_customers_filtered['new_customers'], 
            marker='o', color='#87CEEB', label='New Customers (Count)')

    peak_new_customers = new_customers_filtered.loc[new_customers_filtered['new_customers'].idxmax()]
    ax.scatter(peak_new_customers['year_month'], peak_new_customers['new_customers'], 
               color='#FF5733', s=120, zorder=5, label='Customer Growth Tertinggi')

    ax.set_xticks(new_customers_filtered['year_month'])
    ax.set_xticklabels(new_customers_filtered['year_month'], rotation=45)
    ax.set_ylabel("New Customers")
    ax.set_title("Monthly New Customer Growth")
    ax.legend()
    ax.grid(axis='x', linestyle='--', alpha=0.7)
    plt.box(False)

    st.pyplot(fig)

# Footer
st.caption("📊 Dashboard E-commerce Sales | Created by Luffi Idris Setiawan")
