import os
import logging
from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from ai_functions import *


# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='api_access.log',
    filemode='a'
)
logger = logging.getLogger(__name__)



app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Replace with your React app's URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the RetailDataAnalyzer
script_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(script_dir, 'retail_data.csv')
retail_analyzer = RetailDataAnalyzer(csv_path)

class AnalysisRequest(BaseModel):
    analysis_type: str
    custom_question: Optional[str] = None

class AnalysisResponse(BaseModel):
    result: str

def get_analysis_class(analysis_type: str):
    analysis_classes = {
        'product': ProductAnalysis,
        'customer': CustomerAnalysis,
        'seasonal': SeasonalAnalysis,
        'financial': FinancialAnalysis,
        'transaction': TransactionAnalysis,
        'anomaly': AnomalyDetection,
        'gender_based_item': GenderBasedItemAnalysis,
        'location_based_category': LocationbasedCategoryAnalysis,
        'location_based_item': LocationBasedItemAnalysis,
        'payment_method': PaymentMethodAnalysis,
        'basket_size': BasketSizeAnalysis,
        'profit_margin': ProfitMarginAnalysis,
        'product_association': ProductAssociationAnalysis,
        'customer_spending_behavior': CustomerSpendingBehaviorAnalysis,
        'customer_retention': CustomerRetentionAnalysis,
        'product_return': ProductReturnAnalysis,
        'weather_impact': WeatherImpactAnalysis,
        'loyalty_program': LoyaltyProgramAnalysis,
        'underperforming_products': UnderperformingProductsAnalysis,
        'marketing_channel_effectiveness': MarketingChannelEffectivenessAnalysis,
        'repeat_purchase_interval': RepeatPurchaseIntervalAnalysis,
        'urban_rural_sales': UrbanRuralSalesAnalysis,
        'staff_training_impact': StaffTrainingImpactAnalysis,
        'seasonal_promotion_impact': SeasonalPromotionImpactAnalysis,
        'optimal_pricing': OptimalPricingAnalysis,
        'promotion': PromotionAnalysis
    }
    return analysis_classes.get(analysis_type)


@app.post("/analyze", response_model=AnalysisResponse)
async def analyze(request: Request, analysis_request: AnalysisRequest):
    logger.info(f"Received analysis request: {analysis_request.analysis_type}")
    
    try:
        if analysis_request.analysis_type == 'custom':
            if not analysis_request.custom_question:
                logger.error("Custom question is required for custom analysis")
                raise HTTPException(status_code=400, detail="Custom question is required for custom analysis")
            analysis = CustomQuestion(retail_analyzer)
            result = analysis.ask_question(analysis_request.custom_question)
        else:
            analysis_class = get_analysis_class(analysis_request.analysis_type)
            if not analysis_class:
                logger.error(f"Invalid analysis type: {analysis_request.analysis_type}")
                raise HTTPException(status_code=400, detail="Invalid analysis type")
            analysis = analysis_class(retail_analyzer)
            result = analysis.analyze()
        
        logger.info(f"Analysis completed successfully for: {analysis_request.analysis_type}")
        return AnalysisResponse(result=result)
    except Exception as e:
        logger.error(f"Error during analysis: {str(e)}")
        raise HTTPException(status_code=500, detail="An error occurred during analysis")

if __name__ == "__main__":
    import uvicorn
    logger.info("Starting the Retail Analysis AI Server")
    uvicorn.run(app, host="127.0.0.1", port=8000)