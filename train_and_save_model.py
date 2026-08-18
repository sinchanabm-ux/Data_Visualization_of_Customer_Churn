"""
Trains the churn model using the same logic as Churn_RiskAssign.ipynb,
then saves everything the API will need to make predictions later:
  - the trained model
  - the fitted scaler
  - the exact column order used at training time (needed so new
    single-customer inputs get one-hot encoded/reindexed consistently)

Run this once (or whenever you retrain) to produce model_artifacts.pkl.
"""

import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

# --- 1. Load data -----------------------------------------------------
# Matches the dataset now committed in your repo at:
# dataset/customer-churn-dataset.xlsx
DATA_PATH = "dataset/customer-churn-dataset.xlsx"

df = pd.read_excel(dataset\customer-churn-dataset.xlsx)

# --- 2. Clean, same as your notebook -----------------------------------
cols_to_fill = [
    'Value_Deal', 'Multiple_Lines', 'Online_Security', 'Online_Backup',
    'Device_Protection_Plan', 'Premium_Support', 'Streaming_TV',
    'Streaming_Movies', 'Streaming_Music', 'Unlimited_Data',
    'Churn_Category', 'Churn_Reason'
]
for col in cols_to_fill:
    df[col] = df[col].fillna('NA')

df['Customer_Status'] = df['Customer_Status'].map({'Stayed': 0, 'Joined': 0, 'Churned': 1})
df = df.drop(columns=['Churn_Category', 'Churn_Reason'])

X = df.drop(columns=['Customer_Status', 'Customer_ID'])
y = df['Customer_Status']
X = pd.get_dummies(X, drop_first=True)

numeric_cols = [
    'Age', 'Number_of_Referrals', 'Tenure_in_Months', 'Monthly_Charge',
    'Total_Charges', 'Total_Refunds', 'Total_Extra_Data_Charges',
    'Total_Long_Distance_Charges', 'Total_Revenue'
]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.20, random_state=42, stratify=y
)

scaler = StandardScaler()
X_train = X_train.copy()
X_train[numeric_cols] = scaler.fit_transform(X_train[numeric_cols])

model = LogisticRegression(max_iter=5000, random_state=42)
model.fit(X_train, y_train)

# --- 3. Save everything the API needs -----------------------------------
artifacts = {
    "model": model,
    "scaler": scaler,
    "numeric_cols": numeric_cols,
    "training_columns": list(X.columns),  # exact column order/one-hot layout
}
joblib.dump(artifacts, "model_artifacts.pkl")
print("Saved model_artifacts.pkl — ready for the FastAPI service.")
