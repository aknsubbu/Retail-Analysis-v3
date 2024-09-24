import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def load_data(csv_path):
    df = pd.read_csv(csv_path)
    df['Date'] = pd.to_datetime(df['Date'])
    return df

def create_sales_over_time_chart(df, granularity):
    df_agg = df.groupby(pd.Grouper(key='Date', freq=granularity))['Total_Cost'].sum().reset_index()
    return px.line(df_agg, x='Date', y='Total_Cost', title='Sales Over Time')

def create_sales_forecast_chart(df):
    # This is a placeholder. In a real scenario, you'd implement actual forecasting logic.
    last_date = df['Date'].max()
    future_dates = pd.date_range(start=last_date + pd.Timedelta(days=1), periods=30)
    forecast = pd.DataFrame({'Date': future_dates, 'Forecast': np.random.randint(df['Total_Cost'].min(), df['Total_Cost'].max(), size=30)})
    return px.line(forecast, x='Date', y='Forecast', title='Sales Forecast (Next 30 Days)')

def create_sales_by_category_chart(df):
    category_sales = df.groupby('Product')['Total_Cost'].sum().sort_values(ascending=False).head(10)
    return px.bar(category_sales, title='Top 10 Products by Sales')

def create_customer_category_chart(df):
    category_sales = df.groupby('Customer_Category')['Total_Cost'].sum().reset_index()
    return px.pie(category_sales, values='Total_Cost', names='Customer_Category', title='Sales by Customer Category')

def create_sales_heatmap(df):
    df['DayOfWeek'] = df['Date'].dt.dayofweek
    df['WeekOfYear'] = df['Date'].dt.isocalendar().week
    heatmap_data = df.pivot_table(values='Total_Cost', index='DayOfWeek', columns='WeekOfYear', aggfunc='sum')
    return px.imshow(heatmap_data, title='Sales Heatmap')

def create_payment_methods_chart(df):
    payment_methods = df.groupby('Payment_Method')['Total_Cost'].sum().sort_values(ascending=False)
    return px.bar(payment_methods, title='Sales by Payment Method')

def create_store_type_chart(df):
    store_type_sales = df.groupby('Store_Type')['Total_Cost'].sum().sort_values(ascending=False)
    return px.bar(store_type_sales, title='Sales by Store Type')

def create_seasonal_trends_chart(df):
    seasonal_sales = df.groupby('Season')['Total_Cost'].sum().sort_values(ascending=False)
    return px.bar(seasonal_sales, title='Sales by Season')

def create_discount_analysis_chart(df):
    df['Discount_Group'] = pd.cut(df['Discount_Applied'], bins=[0, 5, 10, 15, 20, 100], labels=['0-5%', '5-10%', '10-15%', '15-20%', '20%+'])
    discount_analysis = df.groupby('Discount_Group')['Total_Cost'].mean().reset_index()
    return px.bar(discount_analysis, x='Discount_Group', y='Total_Cost', title='Average Sale by Discount Range')

def create_promotion_impact_chart(df):
    promotion_impact = df.groupby('Promotion')['Total_Cost'].mean().sort_values(ascending=False)
    return px.bar(promotion_impact, title='Average Sale by Promotion')

def create_city_sales_chart(df):
    city_sales = df.groupby('City')['Total_Cost'].sum().sort_values(ascending=False).head(10)
    return px.bar(city_sales, title='Top 10 Cities by Sales')

def create_customer_purchase_frequency_chart(df):
    purchase_frequency = df.groupby('Customer_Name').size().sort_values(ascending=False).head(20)
    return px.bar(purchase_frequency, title='Top 20 Customers by Purchase Frequency')

def create_average_transaction_value_chart(df):
    df['Month'] = df['Date'].dt.to_period('M')
    avg_transaction_value = df.groupby('Month')['Total_Cost'].mean().reset_index()
    avg_transaction_value['Month'] = avg_transaction_value['Month'].astype(str)
    return px.line(avg_transaction_value, x='Month', y='Total_Cost', title='Average Transaction Value Over Time')