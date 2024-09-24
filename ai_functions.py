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

load_dotenv()

class RetailDataAnalyzer:
    def __init__(self, csv_path):
        self.df = self._load_data(csv_path)
        self.llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")
        self.pandas_agent = create_pandas_dataframe_agent(
            self.llm, self.df, verbose=True, allow_dangerous_code=True
        )
        self.tools = self._create_tools()
        self.agent = self._setup_agent()

    def _load_data(self, csv_path):
        df = pd.read_csv(csv_path)
        df['Date'] = pd.to_datetime(df['Date'])
        df['Month'] = df['Date'].dt.month
        df['Year'] = df['Date'].dt.year
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
            memory=memory
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

    def top_products_by_sales(self):
        return self.analyzer.analyze("What are the top 5 products by total sales?")

class CustomerAnalysis:
    def __init__(self, analyzer):
        self.analyzer = analyzer

    def segment_customers(self):
        return self.analyzer.analyze("Can you perform customer segmentation and describe the characteristics of each segment?")

    def top_customers_by_lifetime_value(self):
        return self.analyzer.analyze("Who are our top 10 customers by lifetime value?")

class SeasonalAnalysis:
    def __init__(self, analyzer):
        self.analyzer = analyzer

    def analyze_trends(self):
        return self.analyzer.analyze("What are the seasonal trends in our sales data?")

class FinancialAnalysis:
    def __init__(self, analyzer):
        self.analyzer = analyzer

    def discount_correlation(self):
        return self.analyzer.analyze("Is there a correlation between discount applied and total cost?")

class TransactionAnalysis:
    def __init__(self, analyzer):
        self.analyzer = analyzer

    def payment_methods(self):
        return self.analyzer.analyze("What's the most common payment method for high-value transactions?")

    def transaction_value_by_store_type(self):
        return self.analyzer.analyze("How does the average transaction value vary across different store types?")

class AnomalyDetection:
    def __init__(self, analyzer):
        self.analyzer = analyzer

    def detect_anomalies(self):
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
    retail_analyzer = RetailDataAnalyzer('retail_data.csv')

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

    print("Custom Question: ")
    print(custom_question.ask_question("What is the top sold item in Chicago ?"))