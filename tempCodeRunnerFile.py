import pandas as pd
import numpy as np
from taipy import Gui
from taipy.gui import Markdown, notify, Gui

# Import CSV-based functions
from analysis_functions import (
    load_data, create_sales_over_time_chart, create_sales_forecast_chart,
    create_sales_by_category_chart, create_top_products_chart, create_sales_heatmap,
    create_customer_segmentation_chart, create_customer_lifetime_value_chart,
    create_customer_segment_performance_chart, create_stock_levels_chart,
    create_inventory_turnover_chart, create_product_sales_distribution_chart,
    create_product_profit_margin_chart, create_product_performance_matrix,
    create_seasonal_trends_chart, create_payment_methods_chart,
    create_transaction_value_by_store_type_chart
)

# Import AI-based functions
from ai_functions import (
    RetailDataAnalyzer, ProductAnalysis, CustomerAnalysis, SeasonalAnalysis,
    FinancialAnalysis, TransactionAnalysis, AnomalyDetection, CustomQuestion
)

# Load data
df = load_data('retail_data.csv')

# Initialize AI analyzer
retail_analyzer = RetailDataAnalyzer("retail_data.csv")

# Initialize analysis classes
product_analysis = ProductAnalysis(retail_analyzer)
customer_analysis = CustomerAnalysis(retail_analyzer)
seasonal_analysis = SeasonalAnalysis(retail_analyzer)
financial_analysis = FinancialAnalysis(retail_analyzer)
transaction_analysis = TransactionAnalysis(retail_analyzer)
anomaly_detection = AnomalyDetection(retail_analyzer)
custom_question = CustomQuestion(retail_analyzer)

# Initialize variables
time_granularity = 'D'
selected_date_range = (df['Date'].min(), df['Date'].max())
selected_product_category = df['Product_Category'].iloc[0]
selected_customer_segment = 'All'
ai_insights = ""
user_question = ""
ai_answer = ""

# Create initial charts
sales_over_time_chart = create_sales_over_time_chart(df, time_granularity)
sales_forecast_chart = create_sales_forecast_chart(df)
sales_by_category_chart = create_sales_by_category_chart(df)
top_products_chart = create_top_products_chart(df)
sales_heatmap = create_sales_heatmap(df)
customer_segmentation_chart = create_customer_segmentation_chart(df)
customer_lifetime_value_chart = create_customer_lifetime_value_chart(df)
customer_segment_performance_chart = create_customer_segment_performance_chart(df, selected_customer_segment)
stock_levels_chart = create_stock_levels_chart(df)
inventory_turnover_chart = create_inventory_turnover_chart(df)
product_performance_matrix = create_product_performance_matrix(df)
seasonal_trends_chart = create_seasonal_trends_chart(df)
payment_methods_chart = create_payment_methods_chart(df)
transaction_value_by_store_type_chart = create_transaction_value_by_store_type_chart(df)

# Define the page content
page_md = """
<|container|
# AI-Powered Retail Analysis Dashboard

<|tabs|
## Overview
<|layout|columns=1 1 1 1|gap=1rem|class_name=card|
<|card|
### Total Sales
<|{df['Total_Cost'].sum():,.0f}|text|class_name=big-number|>
|>

<|card|
### Avg Transaction Value
<|{df['Total_Cost'].mean():,.2f}|text|class_name=big-number|>
|>

<|card|
### Total Transactions
<|{len(df):,}|text|class_name=big-number|>
|>

<|card|
### Unique Customers
<|{df['Customer_Name'].nunique():,}|text|class_name=big-number|>
|>
|>

### Time Series Configuration
<|layout|columns=1 1|gap=1rem|class_name=card|
<|{time_granularity}|selector|lov=D;W;M;Y|label=Time Granularity|class_name=fullwidth|>
<|{selected_date_range}|date_range|class_name=fullwidth|>
|>

<|card|
### Sales Over Time
<|{sales_over_time_chart}|chart|>
|>

<|card|
### Sales Forecast
<|{sales_forecast_chart}|chart|>
|>

## Product Analysis
<|layout|columns=1 1|gap=1rem|
<|card|
### Sales by Product Category
<|{sales_by_category_chart}|chart|>
|>

<|card|
### Top 10 Products
<|{top_products_chart}|chart|>
|>
|>

<|card|
### Product Performance Matrix
<|{product_performance_matrix}|chart|>
|>

## Customer Analysis
<|layout|columns=1 1|gap=1rem|
<|card|
### Customer Segmentation
<|{customer_segmentation_chart}|chart|>
|>

<|card|
### Customer Lifetime Value Distribution
<|{customer_lifetime_value_chart}|chart|>
|>
|>

<|card|
### Customer Segment Performance
<|{selected_customer_segment}|selector|lov={['All'] + df['Cluster'].unique().tolist()}|label=Select Segment|class_name=fullwidth|>
<|{customer_segment_performance_chart}|chart|>
|>

## Seasonal Analysis
<|card|
### Seasonal Trends
<|{seasonal_trends_chart}|chart|>
|>

## Financial Analysis
<|card|
### Sales Heatmap
<|{sales_heatmap}|chart|>
|>

## Transaction Analysis
<|layout|columns=1 1|gap=1rem|
<|card|
### Payment Methods
<|{payment_methods_chart}|chart|>
|>

<|card|
### Transaction Value by Store Type
<|{transaction_value_by_store_type_chart}|chart|>
|>
|>

## Inventory Analysis
<|layout|columns=1 1|gap=1rem|
<|card|
### Stock Levels by Product Category
<|{stock_levels_chart}|chart|>
|>

<|card|
### Inventory Turnover Ratio
<|{inventory_turnover_chart}|chart|>
|>
|>

## AI Insights
<|card|
### Anomaly Detection
<|Detect Anomalies|button|on_action=detect_anomalies|class_name=fullwidth|>
<|{ai_insights}|text|>
|>

<|card|
### Custom Analysis
<|{user_question}|input|label=Ask a question about the data|class_name=fullwidth|>
<|Analyze|button|on_action=answer_user_question|class_name=fullwidth|>
<|{ai_answer}|text|>
|>
|>
|>
"""

# Callback functions
def update_data(state):
    state.df_filtered = state.df[(state.df['Date'] >= state.selected_date_range[0]) & (state.df['Date'] <= state.selected_date_range[1])]
    state.sales_over_time_chart = create_sales_over_time_chart(state.df_filtered, state.time_granularity)
    state.sales_forecast_chart = create_sales_forecast_chart(state.df_filtered)
    state.sales_by_category_chart = create_sales_by_category_chart(state.df_filtered)
    state.top_products_chart = create_top_products_chart(state.df_filtered)
    state.sales_heatmap = create_sales_heatmap(state.df_filtered)
    state.customer_segmentation_chart = create_customer_segmentation_chart(state.df_filtered)
    state.customer_lifetime_value_chart = create_customer_lifetime_value_chart(state.df_filtered)
    state.customer_segment_performance_chart = create_customer_segment_performance_chart(state.df_filtered, state.selected_customer_segment)
    state.stock_levels_chart = create_stock_levels_chart(state.df_filtered)
    state.inventory_turnover_chart = create_inventory_turnover_chart(state.df_filtered)
    state.product_performance_matrix = create_product_performance_matrix(state.df_filtered)
    state.seasonal_trends_chart = create_seasonal_trends_chart(state.df_filtered)
    state.payment_methods_chart = create_payment_methods_chart(state.df_filtered)
    state.transaction_value_by_store_type_chart = create_transaction_value_by_store_type_chart(state.df_filtered)
    notify(state, 'info', f"Data updated for selected date range and {state.time_granularity} granularity")

def on_change(state, var_name, var_value):
    if var_name in ['time_granularity', 'selected_date_range']:
        update_data(state)
    elif var_name == 'selected_customer_segment':
        state.customer_segment_performance_chart = create_customer_segment_performance_chart(state.df_filtered, var_value)

def detect_anomalies(state):
    state.ai_insights = anomaly_detection.detect_anomalies()
    notify(state, 'success', "Anomaly detection completed")

def answer_user_question(state):
    state.ai_answer = custom_question.ask_question(state.user_question)
    notify(state, 'success', "Analysis completed")

# CSS for improved styling
css = """
.card {
    background-color: #f8f9fa;
    border-radius: 10px;
    padding: 20px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}
.big-number {
    font-size: 24px;
    font-weight: bold;
    color: #007bff;
}
.fullwidth {
    width: 100%;
}
"""

# Create and run the Gui
gui = Gui(page=page_md)
gui.run(dark_mode=True, css=css)