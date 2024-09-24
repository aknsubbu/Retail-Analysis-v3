# AI-powered Retail Analysis Dashboard

# Retail Data Analysis Project

## Table of Contents

1. [Introduction](#introduction)
2. [Project Structure](#project-structure)
3. [Backend: RetailDataAnalyzer](#backend-retaildataanalyzer)
   - [Overview](#overview)
   - [Key Components](#key-components)
   - [Installation](#backend-installation)
   - [Configuration](#backend-configuration)
   - [Usage](#backend-usage)
   - [Extending the Analyzer](#extending-the-analyzer)
4. [Frontend: React Dashboard](#frontend-react-dashboard)
   - [Overview](#frontend-overview)
   - [Key Components](#frontend-key-components)
   - [Installation](#frontend-installation)
   - [Configuration](#frontend-configuration)
   - [Usage](#frontend-usage)
   - [Customizing the Dashboard](#customizing-the-dashboard)
5. [Connecting Frontend and Backend](#connecting-frontend-and-backend)
6. [Data Requirements](#data-requirements)
7. [AI Assistant Capabilities](#ai-assistant-capabilities)
8. [Troubleshooting](#troubleshooting)
9. [Contributing](#contributing)
10. [License](#license)

## Introduction

The Retail Data Analysis Project is a comprehensive solution for analyzing and visualizing retail data. It combines a powerful Python backend for data processing and analysis with an interactive React frontend for data visualization and querying. This project allows retail businesses to gain insights into their sales patterns, customer behavior, and overall performance through data analysis and AI-powered querying.

## Project Structure

```
retail-data-analysis/
├── backend/
│   ├── retail_data_analyzer.py
│   ├── analysis/
│   │   ├── product_analysis.py
│   │   ├── customer_analysis.py
│   │   └── ...
│   ├── requirements.txt
│   └── .env
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Dashboard.tsx
│   │   │   ├── AIAssistant.tsx
│   │   │   └── ...
│   │   ├── App.tsx
│   │   └── main.tsx
│   ├── package.json
│   └── tailwind.config.js
├── data/
│   └── retail_data.csv
└── README.md
```

## Backend: RetailDataAnalyzer

### Overview

The backend is built in Python and leverages various libraries for data analysis, machine learning, and natural language processing. The core of the backend is the `RetailDataAnalyzer` class, which loads the data and provides tools for analysis.

### Key Components

1. **RetailDataAnalyzer**: The main class that handles data loading, preprocessing, and analysis.
2. **Specialized Analysis Classes**:
   - `ProductAnalysis`: Analyzes product-related data.
   - `CustomerAnalysis`: Performs customer segmentation and lifetime value analysis.
   - `SeasonalAnalysis`: Examines seasonal trends in sales data.
   - `FinancialAnalysis`: Analyzes financial aspects like discounts and costs.
   - `TransactionAnalysis`: Examines transaction patterns and payment methods.
   - `AnomalyDetection`: Identifies unusual patterns or outliers in the data.
   - `GenderBasedItemAnalysis`: Analyzes product preferences by gender.
   - `LocationbasedCategoryAnalysis`: Examines product categories by location.
   - `LocationBasedItemAnalysis`: Analyzes specific product sales by location.
   - `PaymentMethodAnalysis`: Examines payment method usage patterns.
   - `PromotionAnalysis`: Evaluates the effectiveness of promotions.

### Backend Installation

1. Clone the repository:

   ```
   git clone https://github.com/your-repo/retail-data-analysis.git
   cd retail-data-analysis/backend
   ```

2. Create a virtual environment:

   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install required packages:
   ```
   pip install -r requirements.txt
   ```

### Backend Configuration

1. Create a `.env` file in the `backend/` directory with the following content:

   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```

2. Ensure your retail data CSV file is placed in the `data/` directory.

### Backend Usage

Here's an example of how to use the RetailDataAnalyzer:

```python
from retail_data_analyzer import RetailDataAnalyzer

analyzer = RetailDataAnalyzer('data/retail_data.csv')

# Perform product analysis
product_analysis = ProductAnalysis(analyzer)
top_products = product_analysis.top_products_by_sales()
print("Top 5 products by sales:", top_products)

# Ask a custom question
custom_question = CustomQuestion(analyzer)
result = custom_question.ask_question("What is the top sold item in Chicago?")
print("Top sold item in Chicago:", result)
```

### Extending the Analyzer

To add new analysis capabilities:

1. Create a new analysis class in the `analysis/` directory.
2. Import and instantiate your new class in `retail_data_analyzer.py`.
3. Add a new tool in the `_create_tools` method of `RetailDataAnalyzer` if necessary.

## Frontend: React Dashboard

### Frontend Overview

The frontend is a React-based dashboard that visualizes the data from the RetailDataAnalyzer and provides an interactive interface for querying the data.

### Frontend Key Components

1. **Dashboard**: The main component that displays various charts and metrics.
2. **AIAssistant**: An interactive component for asking questions about the data.
3. **Charts**: Various chart components (AreaChart, BarChart, PieChart) for data visualization.

### Frontend Installation

1. Navigate to the frontend directory:

   ```
   cd retail-data-analysis/frontend
   ```

2. Install dependencies:
   ```
   npm install
   ```

### Frontend Configuration

1. Create a `.env` file in the `frontend/` directory with the backend API URL:

   ```
   REACT_APP_API_URL=http://localhost:5000
   ```

2. Adjust the `tailwind.config.js` file if you need to customize the styling.

### Frontend Usage

1. Start the development server:

   ```
   npm run dev
   ```

2. Open your browser and navigate to `http://localhost:3000`.

### Customizing the Dashboard

To add new visualizations or metrics:

1. Create a new component in the `src/components/` directory.
2. Import and add your new component to the `Dashboard.tsx` file.
3. Fetch necessary data in the component using the API utility functions.

## Connecting Frontend and Backend

The frontend communicates with the backend through API calls. Ensure that:

1. The backend server is running (typically on `http://localhost:5000`).
2. The frontend is configured with the correct API endpoint in the `.env` file.
3. CORS is properly configured on the backend to allow requests from the frontend.

## Data Requirements

The `retail_data.csv` file should contain the following columns:

- Transaction_ID
- Date
- Customer_Name
- Product
- Total_Items
- Total_Cost
- Payment_Method
- City
- Store_Type
- Discount_Applied
- Customer_Category
- Season
- Promotion

Ensure your data file follows this structure for the analyzer to work correctly.

## AI Assistant Capabilities

The AI Assistant can answer a wide range of questions about the retail data. Some example questions include:

- What are the top 5 products by total sales?
- Can you perform customer segmentation and describe the characteristics of each segment?
- What are the seasonal trends in our sales data?
- Is there a correlation between discount applied and total cost?
- What's the most common payment method for high-value transactions?
- What are the top products purchased by male and female customers?
- What are the promotions that cause the greatest increase in sales?

For a full list of sample questions, refer to the `faqQuestions` array in the `AIAssistant.tsx` component.

## Troubleshooting

- If you encounter CORS issues, ensure your backend is configured to allow requests from your frontend's origin.
- For OpenAI API errors, check that your API key is correctly set in the backend's `.env` file.
- If charts are not rendering, check the browser console for any JavaScript errors and ensure all required data is being fetched correctly.

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch: `git checkout -b feature-branch-name`.
3. Make your changes and commit them: `git commit -m 'Add some feature'`.
4. Push to the branch: `git push origin feature-branch-name`.
5. Submit a pull request.
