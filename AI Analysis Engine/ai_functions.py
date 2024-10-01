import os
from dotenv import load_dotenv
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from langchain_experimental.agents import create_pandas_dataframe_agent
from langchain.agents import Tool, AgentExecutor
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.agents import initialize_agent, AgentType
import matplotlib.pyplot as plt
import seaborn as sns
import logging

load_dotenv()

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class RetailDataAnalyzer:
    def __init__(self, csv_path):
        self.df = self._load_data(csv_path)
        self.llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")
        self.pandas_agent = create_pandas_dataframe_agent(
            self.llm, self.df, verbose=True, allow_dangerous_code=True
        )
        self.instruction = """
You are an expert retail data analyst with years of experience in interpreting complex retail datasets. Your task is to provide comprehensive, actionable insights from the given retail data. Follow these guidelines:

1. Always start by understanding the data structure and key metrics.
2. Provide both high-level summaries and detailed breakdowns of important trends.
3. Identify correlations between different variables and explain their potential business implications.
4. Suggest concrete, data-driven strategies to improve sales, customer retention, and overall business performance.
5. When appropriate, compare current performance to industry benchmarks or historical data.
6. Always consider the practical application of your insights for business decision-making.
7. Donot create images...
8. Always give data driven analysis
"""
        self.context = """
When analyzing the data, consider these industry-specific metrics and KPIs:

Sales per square foot
Inventory turnover ratio
Gross margin return on investment (GMROI)
Customer acquisition cost (CAC)
Average transaction value
Conversion rate
Year-over-year growth
Same-store sales growth

Remember to support your insights with specific data points, visualizations when appropriate, and always tie your recommendations back to potential business impact.

"""
        self.tools = self._create_tools()
        self.agent = self._setup_agent()

    def _load_data(self, csv_path):
        logging.debug(f"Attempting to load data from {csv_path}")
        
        # Check if the file exists
        if not os.path.exists(csv_path):
            logging.error(f"CSV file not found: {csv_path}")
            raise FileNotFoundError(f"CSV file not found: {csv_path}")
        
        # Check if the file is readable
        if not os.access(csv_path, os.R_OK):
            logging.error(f"CSV file is not readable: {csv_path}")
            raise PermissionError(f"CSV file is not readable: {csv_path}")
        
        # Try to read the CSV file
        try:
            df = pd.read_csv(csv_path)
            logging.debug(f"Successfully loaded CSV file with {len(df)} rows")
        except Exception as e:
            logging.error(f"Error reading CSV file: {str(e)}")
            raise

        # Process the dataframe
        try:
            df['Date'] = pd.to_datetime(df['Date'])
            df['Month'] = df['Date'].dt.month
            df['Year'] = df['Date'].dt.year
            logging.debug("Data processed successfully")
        except Exception as e:
            logging.error(f"Error processing data: {str(e)}")
            raise

        return df

    def _create_tools(self):
        return [
            Tool(
                name="Pandas DataFrame Analysis",
                func=self.pandas_agent.run,
                description="Useful for when you need to answer questions about the DataFrame or perform data manipulations."
            ),
            Tool(
                name="Customer Segmentation",
                func=lambda _: self.customer_segmentation(),
                description="Perform customer segmentation using K-means clustering."
            ),
            Tool(
                name="Seasonal Trends Analysis",
                func=lambda _: self.seasonal_trends(),
                description="Analyze and visualize seasonal sales trends."
            ),
            Tool(
                name="Customer Lifetime Value",
                func=lambda _: self.customer_lifetime_value(),
                description="Calculate customer lifetime value."
            )
        ]

    def _setup_agent(self):
        memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
        return initialize_agent(
            self.tools,
            self.llm,
            agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
            verbose=True,
            memory=memory,
            agent_kwargs={
                "prefix": f"{self.instruction}\n\nContext: {self.context}\n\n"
            }
        )

    def analyze(self, question):
        return self.agent.run(question)

    def customer_segmentation(self):
        features = ['Total_Items', 'Total_Cost']
        X = self.df[features]
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        kmeans = KMeans(n_clusters=3, random_state=42)
        self.df['Cluster'] = kmeans.fit_predict(X_scaled)
        return self.df

    def seasonal_trends(self):
        seasonal_sales = self.df.groupby(['Season', 'Year'])['Total_Cost'].sum().unstack()
        plt.figure(figsize=(12, 6))
        seasonal_sales.plot(kind='bar')
        plt.title('Seasonal Sales Trends')
        plt.xlabel('Season')
        plt.ylabel('Total Sales')
        plt.legend(title='Year')
        plt.tight_layout()
        plt.savefig('seasonal_trends.png')
        return 'Seasonal trends analysis completed. Check seasonal_trends.png for the visualization.'

    def customer_lifetime_value(self):
        clv = self.df.groupby('Customer_Name')['Total_Cost'].sum().sort_values(ascending=False)
        return clv.to_dict()

class ProductAnalysis:
    def __init__(self, analyzer):
        self.analyzer = analyzer

    def analyze(self):
        return self.analyzer.analyze("What are the top 5 products by total sales?")

class CustomerAnalysis:
    def __init__(self, analyzer):
        self.analyzer = analyzer

    def analyze(self):
        return self.analyzer.analyze("Can you perform customer segmentation and describe the characteristics of each segment?")

    # def top_customers_by_lifetime_value(self):
    #     return self.analyzer.analyze("Who are our top 10 customers by lifetime value?")

class SeasonalAnalysis:
    def __init__(self, analyzer):
        self.analyzer = analyzer

    def analyze(self):
        return self.analyzer.analyze("What are the seasonal trends in our sales data?")

class FinancialAnalysis:
    def __init__(self, analyzer):
        self.analyzer = analyzer

    def analyze(self):
        return self.analyzer.analyze("Is there a correlation between discount applied and total cost?")

class TransactionAnalysis:
    def __init__(self, analyzer):
        self.analyzer = analyzer

    def analyze(self):
        return self.analyzer.analyze("What's the most common payment method for high-value transactions?")

    # def transaction_value_by_store_type(self):
    #     return self.analyzer.analyze("How does the average transaction value vary across different store types?")

class AnomalyDetection:
    def __init__(self, analyzer):
        self.analyzer = analyzer

    def analyze(self):
        return self.analyzer.analyze("Can you identify any interesting patterns or anomalies in the data?")
    
class GenderBasedItemAnalysis:
    def __init__(self, analyzer):
        self.analyzer = analyzer

    def analyze(self):
        return self.analyzer.analyze("What are the top products purchased by male and female customers?")
    
class LocationbasedCategoryAnalysis:
    def __init__(self, analyzer):
        self.analyzer = analyzer
    
    def analyze(self):
        return self.analyzer.analyze("What are the top categories of products sold in each location?")
    
class LocationBasedItemAnalysis:
    def __init__(self, analyzer):
        self.analyzer = analyzer

    def analyze(self):
        return self.analyzer.analyze("What are the top products sold in each location?")
    
class PaymentMethodAnalysis:
    def __init__(self, analyzer):
        self.analyzer = analyzer

    def analyze(self):
        return self.analyzer.analyze("What are the most common payment methods used by customers in each location and category?")
    
class BasketSizeAnalysis:
    def __init__(self, analyzer):
        self.analyzer = analyzer

    def analyze(self):
        return self.analyzer.analyze("What is the average basket size (number of items per transaction) and how does it vary by store type or location?")

class ProfitMarginAnalysis:
    def __init__(self, analyzer):
        self.analyzer = analyzer

    def analyze(self):
        return self.analyzer.analyze("Which product categories have the highest profit margins?")

class ProductAssociationAnalysis:
    def __init__(self, analyzer):
        self.analyzer = analyzer

    def analyze(self):
        return self.analyzer.analyze("Are there any products that are frequently purchased together? Can we identify any strong product associations?")

class CustomerSpendingBehaviorAnalysis:
    def __init__(self, analyzer):
        self.analyzer = analyzer

    def analyze(self):
        return self.analyzer.analyze("How does customer spending behavior change during different times of the day or days of the week?")

class CustomerRetentionAnalysis:
    def __init__(self, analyzer):
        self.analyzer = analyzer

    def analyze(self):
        return self.analyzer.analyze("What is the customer retention rate, and how does it vary across different customer segments?")

class ProductReturnAnalysis:
    def __init__(self, analyzer):
        self.analyzer = analyzer

    def analyze(self):
        return self.analyzer.analyze("Which products have the highest return rates, and are there any patterns in the reasons for returns?")

class WeatherImpactAnalysis:
    def __init__(self, analyzer):
        self.analyzer = analyzer

    def analyze(self):
        return self.analyzer.analyze("How do weather conditions affect sales of specific product categories?")

class LoyaltyProgramAnalysis:
    def __init__(self, analyzer):
        self.analyzer = analyzer

    def analyze(self):
        return self.analyzer.analyze("What is the impact of loyalty programs on customer purchase frequency and average transaction value?")

class UnderperformingProductsAnalysis:
    def __init__(self, analyzer):
        self.analyzer = analyzer

    def analyze(self):
        return self.analyzer.analyze("Are there any underperforming products that we should consider discontinuing?")

class MarketingChannelEffectivenessAnalysis:
    def __init__(self, analyzer):
        self.analyzer = analyzer

    def analyze(self):
        return self.analyzer.analyze("How does the effectiveness of different marketing channels vary in terms of driving sales and customer acquisition?")

class RepeatPurchaseIntervalAnalysis:
    def __init__(self, analyzer):
        self.analyzer = analyzer

    def analyze(self):
        return self.analyzer.analyze("What is the average time between purchases for repeat customers, and how can we reduce this interval?")

class UrbanRuralSalesAnalysis:
    def __init__(self, analyzer):
        self.analyzer = analyzer

    def analyze(self):
        return self.analyzer.analyze("How do sales trends differ between urban and rural store locations?")

class StaffTrainingImpactAnalysis:
    def __init__(self, analyzer):
        self.analyzer = analyzer

    def analyze(self):
        return self.analyzer.analyze("What is the correlation between staff training levels and sales performance in different store locations?")

class SeasonalPromotionImpactAnalysis:
    def __init__(self, analyzer):
        self.analyzer = analyzer

    def analyze(self):
        return self.analyzer.analyze("How do seasonal promotions impact overall profitability compared to regular sales periods?")

class OptimalPricingAnalysis:
    def __init__(self, analyzer):
        self.analyzer = analyzer

    def analyze(self):
        return self.analyzer.analyze("What is the optimal price point for our best-selling products to maximize both sales volume and profit?")

class CustomQuestion:
    def __init__(self, analyzer):
        self.analyzer = analyzer

    def ask_question(self, question):
        return self.analyzer.analyze(question)
    
class PromotionAnalysis:
    def __init__(self, analyzer):
        self.analyzer = analyzer
    
    def analyze(self):
        return self.analyzer.analyze("What are the promotions that cause the greatest increase in sales?    ")

# Usage
if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(script_dir, 'retail_data.csv')
    logging.info(f"Script directory: {script_dir}")
    logging.info(f"CSV path: {csv_path}")

    try:
        retail_analyzer = RetailDataAnalyzer(csv_path)
        product_analysis = ProductAnalysis(retail_analyzer)
        customer_analysis = CustomerAnalysis(retail_analyzer)
        seasonal_analysis = SeasonalAnalysis(retail_analyzer)
        financial_analysis = FinancialAnalysis(retail_analyzer)
        transaction_analysis = TransactionAnalysis(retail_analyzer)
        anomaly_detection = AnomalyDetection(retail_analyzer)
        custom_question = CustomQuestion(retail_analyzer)

        # print("Top Products by Sales:")
        # print(product_analysis.top_products_by_sales())

        # print("\nCustomer Segmentation:")
        # print(customer_analysis.segment_customers())

        # print("\nSeasonal Trends:")
        # print(seasonal_analysis.analyze_trends())

        # print("\nTop Customers by Lifetime Value:")
        # print(customer_analysis.top_customers_by_lifetime_value())

        # print("\nDiscount Correlation:")
        # print(financial_analysis.discount_correlation())

        # print("\nPayment Methods for High-Value Transactions:")
        # print(transaction_analysis.payment_methods())

        # print("\nTransaction Value by Store Type:")
        # print(transaction_analysis.transaction_value_by_store_type())

        # print("Custom Question: ")
        # print(custom_question.ask_question("Reach a sales analysis for the given CSV Retail Data ?"))


    except Exception as e:
        logging.error(f"An error occurred: {str(e)}", exc_info=True)
        print(f"An error occurred: {str(e)}")