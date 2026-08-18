"""
Minimal FastAPI service that serves your churn model.
Run with:  uvicorn main:app --reload
Then visit http://127.0.0.1:8000/docs for an auto-generated test UI.
"""

import pandas as pd
import joblib
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Customer Churn Prediction API")

artifacts = joblib.load("model_artifacts.pkl")
model = artifacts["model"]
scaler = artifacts["scaler"]
numeric_cols = artifacts["numeric_cols"]
training_columns = artifacts["training_columns"]


# Describes exactly the fields a caller must send — FastAPI validates
# incoming requests against this automatically and rejects bad input.
# These are the RAW fields (before one-hot encoding) — pd.get_dummies()
# below expands things like State/Contract into the columns the model
# was actually trained on.
class CustomerInput(BaseModel):
    Gender: str
    Age: int
    Married: str
    State: str
    Number_of_Referrals: int
    Tenure_in_Months: int
    Value_Deal: str
    Phone_Service: str
    Multiple_Lines: str
    Internet_Service: str
    Internet_Type: str
    Online_Security: str
    Online_Backup: str
    Device_Protection_Plan: str
    Premium_Support: str
    Streaming_TV: str
    Streaming_Movies: str
    Streaming_Music: str
    Unlimited_Data: str
    Contract: str
    Paperless_Billing: str
    Payment_Method: str
    Monthly_Charge: float
    Total_Charges: float
    Total_Refunds: float
    Total_Extra_Data_Charges: float
    Total_Long_Distance_Charges: float
    Total_Revenue: float


def risk(prob: float) -> str:
    if prob >= 0.58251:
        return "High"
    elif prob >= 0.30:
        return "Medium"
    return "Low"


@app.get("/")
def health_check():
    return {"status": "ok", "message": "Churn prediction API is running"}


@app.post("/predict")
def predict_churn(customer: CustomerInput):
    # Convert the single customer into a one-row DataFrame, then align it
    # to the exact same columns the model was trained on.
    input_df = pd.DataFrame([customer.dict()])
    input_df = pd.get_dummies(input_df)
    input_df = input_df.reindex(columns=training_columns, fill_value=0)

    input_df[numeric_cols] = scaler.transform(input_df[numeric_cols])

    prob = model.predict_proba(input_df)[:, 1][0]

    return {
        "churn_probability": round(float(prob) * 100, 2),
        "risk_category": risk(prob),
        "estimated_revenue_at_risk": round(customer.Monthly_Charge * prob, 2),
    }
