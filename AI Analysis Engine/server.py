from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from ai_functions import *
import os

app = FastAPI()

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
async def analyze(request: AnalysisRequest):
    if request.analysis_type == 'custom':
        if not request.custom_question:
            raise HTTPException(status_code=400, detail="Custom question is required for custom analysis")
        analysis = CustomQuestion(retail_analyzer)
        result = analysis.ask_question(request.custom_question)
    else:
        analysis_class = get_analysis_class(request.analysis_type)
        if not analysis_class:
            raise HTTPException(status_code=400, detail="Invalid analysis type")
        analysis = analysis_class(retail_analyzer)
        result = analysis.analyze()

    return AnalysisResponse(result=result)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)