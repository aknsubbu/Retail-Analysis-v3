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
from functools import lru_cache

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
7. Do not create images.
8. Always give data-driven analysis with specific numbers and percentages.
9. Provide clear, actionable recommendations based on the analysis.
10. When possible, segment the data to provide more nuanced insights.
"""
        self.context = """
When analyzing the data, consider these industry-specific metrics and KPIs:

- Sales per square foot
- Inventory turnover ratio
- Gross margin return on investment (GMROI)
- Customer acquisition cost (CAC)
- Average transaction value
- Conversion rate
- Year-over-year growth
- Same-store sales growth
- Customer lifetime value (CLV)
- Net Promoter Score (NPS)
- Sell-through rate
- Shrinkage rate

Remember to support your insights with specific data points and always tie your recommendations back to potential business impact.
"""
        self.tools = self._create_tools()
        self.agent = self._setup_agent()

    def _load_data(self, csv_path):
        logging.debug(f"Attempting to load data from {csv_path}")
        
        if not os.path.exists(csv_path):
            logging.error(f"CSV file not found: {csv_path}")
            raise FileNotFoundError(f"CSV file not found: {csv_path}")
        
        if not os.access(csv_path, os.R_OK):
            logging.error(f"CSV file is not readable: {csv_path}")
            raise PermissionError(f"CSV file is not readable: {csv_path}")
        
        try:
            df = pd.read_csv(csv_path)
            logging.debug(f"Successfully loaded CSV file with {len(df)} rows")
        except Exception as e:
            logging.error(f"Error reading CSV file: {str(e)}")
            raise

        try:
            df['Date'] = pd.to_datetime(df['Date'])
            df['Month'] = df['Date'].dt.month
            df['Year'] = df['Date'].dt.year
            df['Season'] = df['Month'].map({12:1, 1:1, 2:1, 3:2, 4:2, 5:2, 6:3, 7:3, 8:3, 9:4, 10:4, 11:4})
            df['Season'] = df['Season'].map({1:'Winter', 2:'Spring', 3:'Summer', 4:'Fall'})
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
                func=self.customer_segmentation,
                description="Perform customer segmentation using K-means clustering."
            ),
            Tool(
                name="Seasonal Trends Analysis",
                func=self.seasonal_trends,
                description="Analyze and visualize seasonal sales trends."
            ),
            Tool(
                name="Customer Lifetime Value",
                func=self.customer_lifetime_value,
                description="Calculate customer lifetime value."
            ),
            Tool(
                name="Product Performance Analysis",
                func=self.product_performance_analysis,
                description="Analyze the performance of products based on sales and profitability."
            ),
            Tool(
                name="Store Performance Analysis",
                func=self.store_performance_analysis,
                description="Analyze the performance of different store locations."
            ),
            Tool(
                name="Promotion Effectiveness Analysis",
                func=self.promotion_effectiveness_analysis,
                description="Analyze the effectiveness of different promotional campaigns."
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

    @lru_cache(maxsize=None)
    def analyze(self, question):
        return self.agent.run(question)

    def customer_segmentation(self, analysis_type=None):
        try:
            # Select features for clustering
            features = ['Total_Cost', 'Total_Items']
            X = self.df.groupby('Customer_Name')[features].mean().reset_index()
            
            # Normalize the features
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X[features])
            
            # Perform K-means clustering
            kmeans = KMeans(n_clusters=3, random_state=42)
            X['Cluster'] = kmeans.fit_predict(X_scaled)
            
            # Calculate cluster characteristics
            cluster_characteristics = X.groupby('Cluster')[features].mean()
            
            # Add more descriptive statistics
            cluster_characteristics['Customer_Count'] = X.groupby('Cluster').size()
            cluster_characteristics['Avg_Purchase_Frequency'] = self.df.groupby('Customer_Name').size().groupby(X.set_index('Customer_Name')['Cluster']).mean()
            
            # Describe segments
            segments = {
                0: "Budget Conscious",
                1: "Average Spenders",
                2: "High-Value Customers"
            }
            
            results = {}
            for cluster, name in segments.items():
                results[name] = {
                    "Average Total Cost": round(cluster_characteristics.loc[cluster, 'Total_Cost'], 2),
                    "Average Items per Purchase": round(cluster_characteristics.loc[cluster, 'Total_Items'], 2),
                    "Customer Count": int(cluster_characteristics.loc[cluster, 'Customer_Count']),
                    "Average Purchase Frequency": round(cluster_characteristics.loc[cluster, 'Avg_Purchase_Frequency'], 2)
                }
            
            return results
        except Exception as e:
            logging.error(f"Error in customer segmentation: {str(e)}")
            return str(e)



    def seasonal_trends(self, analysis_type=None):
        try:
            seasonal_sales = self.df.groupby(['Season', 'Year'])['Total_Cost'].sum().unstack()
            
            if analysis_type == "Identify any interesting patterns or anomalies in the seasonal sales trends data.":
                # Calculate year-over-year growth
                yoy_growth = seasonal_sales.pct_change()
                
                # Calculate average seasonal pattern
                avg_seasonal_pattern = seasonal_sales.mean(axis=1)
                
                # Identify seasons with unusual growth or decline
                unusual_growth = yoy_growth[yoy_growth.abs() > 0.2]  # 20% threshold for unusual growth/decline
                
                # Identify seasons that deviate significantly from the average pattern
                deviations = seasonal_sales.sub(avg_seasonal_pattern, axis=0).abs()
                significant_deviations = deviations[deviations > deviations.mean() + 2*deviations.std()]
                
                results = {
                    "seasonal_sales": seasonal_sales.to_dict(),
                    "year_over_year_growth": yoy_growth.to_dict(),
                    "average_seasonal_pattern": avg_seasonal_pattern.to_dict(),
                    "unusual_growth": unusual_growth.to_dict(),
                    "significant_deviations": significant_deviations.to_dict()
                }
                
                # Analyze and summarize findings
                summary = []
                if not unusual_growth.empty:
                    summary.append(f"Unusual growth/decline (>20%) observed in: {', '.join(unusual_growth.index.get_level_values('Season').unique())}")
                if not significant_deviations.empty:
                    summary.append(f"Significant deviations from average pattern observed in: {', '.join(significant_deviations.index.get_level_values('Season').unique())}")
                if seasonal_sales.idxmax().nunique() == 1:
                    peak_season = seasonal_sales.idxmax().iloc[0]
                    summary.append(f"Consistent peak season across years: {peak_season}")
                
                results["summary"] = summary
                
                return results
            else:
                return seasonal_sales.to_dict()
        except Exception as e:
            logging.error(f"Error in seasonal trends analysis: {str(e)}")
            return str(e)

    def customer_lifetime_value(self):
        try:
            clv = self.df.groupby('Customer_Name')['Total_Cost'].sum().sort_values(ascending=False)
            return clv.head(10).to_dict()
        except Exception as e:
            logging.error(f"Error in customer lifetime value calculation: {str(e)}")
            return str(e)

    def product_performance_analysis(self, analysis_type=None):
        try:
            logging.debug(f"DataFrame columns: {self.df.columns.tolist()}")
            logging.debug(f"DataFrame shape: {self.df.shape}")
            logging.debug(f"DataFrame info:\n{self.df.info()}")

            # Try to identify the correct column names
            product_column = next((col for col in self.df.columns if 'product' in col.lower()), None)
            store_column = next((col for col in self.df.columns if 'store' in col.lower()), None)
            quantity_column = next((col for col in self.df.columns if 'quantity' in col.lower() or 'items' in col.lower()), None)
            sales_column = next((col for col in self.df.columns if 'cost' in col.lower() or 'sales' in col.lower()), None)

            if not all([product_column, store_column, quantity_column, sales_column]):
                raise ValueError(f"Unable to identify required columns. Found: Product: {product_column}, Store: {store_column}, Quantity: {quantity_column}, Sales: {sales_column}")

            product_performance = self.df.groupby([store_column, product_column]).agg({
                sales_column: 'sum',
                quantity_column: 'sum',
            }).reset_index()

            if analysis_type == "Top products sold in each location":
                results = {}
                for store in product_performance[store_column].unique():
                    store_products = product_performance[product_performance[store_column] == store]
                    top_products = store_products.nlargest(5, quantity_column)
                    results[store] = [
                        {
                            "Product": product[product_column],
                            "Quantity": int(product[quantity_column]),
                            "Total_Sales": float(product[sales_column])
                        }
                        for _, product in top_products.iterrows()
                    ]
                
                return results
            else:
                return product_performance.sort_values(sales_column, ascending=False).head(10).to_dict('records')
        except Exception as e:
            logging.error(f"Error in product performance analysis: {str(e)}")
            return str(e)

    def store_performance_analysis(self, analysis_type=None):
        try:
            if analysis_type == "Top products sold in each location":
                top_products = self.df.groupby(['Store_Type', 'Item_Name'])['Quantity'].sum().reset_index()
                top_products = top_products.sort_values(['Store_Type', 'Quantity'], ascending=[True, False])
                top_products = top_products.groupby('Store_Type').head(5)
                return top_products.to_dict(orient='records')
            else:
                store_performance = self.df.groupby('Store_Type').agg({
                    'Total_Cost': 'sum',
                    'Total_Items': 'sum',
                    'Customer_Name': 'nunique'
                }).rename(columns={'Customer_Name': 'Unique_Customers'})
                return store_performance.to_dict()
        except Exception as e:
            logging.error(f"Error in store performance analysis: {str(e)}")
            return str(e)

    def promotion_effectiveness_analysis(self, analysis_type=None):
        try:
            self.df['Discount_Rate'] = self.df['Discount_Applied'] / self.df['Total_Cost']
            promotion_effectiveness = self.df.groupby('Store_Type').agg({
                'Discount_Rate': 'mean',
                'Total_Cost': 'sum',
                'Quantity': 'sum'
            })

            if analysis_type == "Identify promotions that lead to the greatest increase in sales":
                # Calculate the correlation between discount rate and total sales
                correlation = self.df.groupby('Store_Type').apply(lambda x: x['Discount_Rate'].corr(x['Total_Cost']))
                
                # Identify store types where higher discounts lead to higher sales
                effective_promotions = correlation[correlation > 0].sort_values(ascending=False)
                
                results = {
                    "promotion_effectiveness": promotion_effectiveness.to_dict(),
                    "discount_sales_correlation": correlation.to_dict(),
                    "most_effective_promotions": effective_promotions.to_dict()
                }
                
                return results
            else:
                return promotion_effectiveness.to_dict()
        except Exception as e:
            logging.error(f"Error in promotion effectiveness analysis: {str(e)}")
            return str(e)


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