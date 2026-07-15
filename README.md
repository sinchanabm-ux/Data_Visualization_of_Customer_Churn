# Customer Churn Analysis and Prediction using Power BI and Machine Learning

This project looks at customer churn for a telecom company. The dataset was cleaned and transformed in Python, a machine learning model was trained to predict which customers are likely to churn, and the results were brought into Power BI to build a dashboard that a business team could actually use.

## What's in this repo

- `Churn_RiskAssign.ipynb` - the notebook where data cleaning, model training, and churn risk scoring happens
- `Customer_Churn_Analysis_and_Prediction_FINAL.pbix` - the Power BI file with the dashboard
- `README.md` - this file

## The dataset

6,418 customer records with 32 columns covering demographics, the services each customer had signed up for, billing info, and whether they'd churned. A good chunk of the service-related columns (things like Online Security, Streaming TV, Multiple Lines) had missing values, mostly because those customers didn't have internet service to begin with, so those were filled in as "NA" rather than dropped.

Customer status originally had three values - Stayed, Joined, and Churned. For modeling purposes this was collapsed into a binary target: Stayed and Joined became 0, Churned became 1.

## Building the model

Six different classification models were trained and compared: Logistic Regression, Random Forest, Extra Trees, Gradient Boosting, KNN, and Naive Bayes. Each was scored on accuracy, precision, recall, F1, and ROC-AUC, and the average of those five became the deciding metric.

| Model | Accuracy | Precision | Recall | F1 Score | ROC-AUC | Overall Score |
|---|---|---|---|---|---|---|
| Logistic Regression | 0.842 | 0.725 | 0.669 | 0.696 | 0.891 | 0.765 |
| Gradient Boosting | 0.840 | 0.745 | 0.622 | 0.678 | 0.898 | 0.757 |
| Extra Trees | 0.829 | 0.719 | 0.605 | 0.657 | 0.885 | 0.739 |
| Random Forest | 0.831 | 0.743 | 0.573 | 0.647 | 0.887 | 0.736 |
| Naive Bayes | 0.772 | 0.553 | 0.818 | 0.660 | 0.866 | 0.734 |
| KNN | 0.791 | 0.622 | 0.582 | 0.601 | 0.808 | 0.681 |

Logistic Regression came out on top and was used as the final model. It's not the fanciest choice, but it edged out the ensemble models here and is easy to explain to non-technical stakeholders, which matters for a churn project like this.

Every active customer (not already churned) was scored with a churn probability and put into a risk bucket:

- 70% or higher: High risk
- 40% to 69%: Medium risk
- Below 40%: Low risk

Revenue at risk for each customer was estimated as their monthly charge multiplied by their churn probability. The final scored dataset was exported to CSV and pulled into Power BI.

## The dashboard

The Power BI file has four pages.

**Executive Overview** - the top-level numbers: 6.42K total customers, 1.73K churned, 434 flagged high risk. Also shows churn rate trend over tenure, the breakdown of churn reasons (competitor, attitude, dissatisfaction, price, other), and a simple view of how many customers stayed, churned, or joined.

**Customer Analysis** - digs into who's churning. Breaks it down by internet type, payment method, and contract type, and includes a chart of which features mattered most to the model - total revenue, total charges, contract type, long distance charges, and monthly charges were the biggest drivers.

**Churn Risk Prediction** - this is where the model output lives. 434 high-risk customers, about $622.5K in revenue tied to them, and an average churn likelihood of 17%. It shows risk broken out by contract, how churn probability trends across tenure, and which internet service types carry the most risk (fiber optic customers stood out here).

**Key Insights** - a decomposition tree and a plain list of findings pulled from the analysis:

- Month-to-month customers churn at around 40%, compared to about 3% for two-year contracts. That gap alone accounts for roughly 65% of the revenue lost to churn.
- 75% of the customers who churn do so within their first six months.
- Fiber optic customers churn about 35% more than other internet types, despite paying a premium, which is worth investigating on the service or billing side.
- Customers who've adopted four or more services churn at under 5%, versus 40% for customers with just one service. Getting people onto more services early seems to matter a lot.

There's also a simple projection of how much revenue could be recovered at 10%, 20%, and 30% retention improvement rates, to give a sense of what's actually at stake.

## How the data connects in Power BI

Four tables feed the dashboard: the cleaned customer data (6,418 rows), a validation table comparing actual vs predicted churn on a holdout set, the risk predictions table with churn probability and risk category per customer, and a small table listing which features drove the model's predictions.

## Tools used

Python (pandas, numpy, scikit-learn) for the data work and modeling. Power BI for the dashboard and DAX measures.

## Running it yourself

Clone the repo, open the notebook if you want to see or rerun the modeling steps, and open the .pbix file in Power BI Desktop to explore the dashboard directly.

## Takeaways

If I had to summarize what this means for the business: push customers off month-to-month contracts where possible, pay close attention to the first six months of a customer's lifecycle since that's where most churn happens, look into why fiber optic customers are unhappy, and encourage customers to adopt more services early since that seems to be one of the strongest things tying people to the company.
