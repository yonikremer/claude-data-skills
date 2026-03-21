---
name: anomaly-detection
description: Identifies unusual patterns or outliers in data that do not conform to expected behavior. Use when detecting fraud, monitoring system health, or flagging abnormal traffic. Do NOT use for general exploratory analysis (use exploratory-data-analysis) or for basic data cleaning (use pandas).
---
# Anomaly Detection

This skill focuses on identifying unusual patterns or outliers in data that do not conform to expected behavior. Anomalies can signify critical incidents, fraud, system failures, or novel opportunities.

## Overview

Anomaly detection is crucial in various domains, including:
- **Fraud Detection**: Identifying unusual financial transactions.
- **Intrusion Detection**: Flagging abnormal network traffic.
- **System Health Monitoring**: Detecting unusual sensor readings or server behavior.
- **Manufacturing Quality Control**: Spotting defective products.
- **Medical Diagnostics**: Finding abnormal patterns in patient data.

## Key Concepts

### Types of Anomalies
1.  **Point Anomalies**: A single data instance that is anomalous with respect to the rest of the data. (e.g., a single fraudulent transaction).
2.  **Contextual Anomalies**: A data instance that is anomalous in a specific context but not otherwise. (e.g., a high temperature reading is normal in summer but anomalous in winter).
3.  **Collective Anomalies**: A collection of related data instances that is anomalous with respect to the entire dataset, even if individual instances are not. (e.g., a sudden drop in website traffic for a short period).

### Challenges
-   **Data Sparsity**: Anomalies are rare by definition.
-   **Noisy Data**: Irrelevant variations can mask true anomalies.
-   **Concept Drift**: The definition of "normal" can change over time.
-   **Lack of Labeled Data**: Often, anomalies are unlabeled.

## Common Techniques

### 1. Statistical Methods

#### Z-score / Standard Deviation
Assumes data is normally distributed. An anomaly is detected if a data point is many standard deviations away from the mean.
```python
import numpy as np
import pandas as pd

def detect_zscore_outliers(df, column, threshold=3):
    mean = df[column].mean()
    std = df[column].std()
    df['z_score'] = (df[column] - mean) / std
    return df[np.abs(df['z_score']) > threshold]

# Example usage
data = {'value': np.random.normal(0, 1, 100)}
data['value'][10] = 10 # Introduce an anomaly
df = pd.DataFrame(data)
outliers = detect_zscore_outliers(df, 'value')
print("Z-score outliers:\n", outliers)
```

#### IQR (Interquartile Range)
More robust to non-normal distributions and outliers.
```python
def detect_iqr_outliers(df, column, k=1.5):
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - k * IQR
    upper_bound = Q3 + k * IQR
    return df[(df[column] < lower_bound) | (df[column] > upper_bound)]

# Example usage
outliers = detect_iqr_outliers(df, 'value')
print("IQR outliers:\n", outliers)
```

### 2. Machine Learning Methods

#### Isolation Forest
An ensemble learning method based on decision trees. It "isolates" anomalies by randomly selecting a feature and then randomly selecting a split value between the maximum and minimum values of the selected feature.
```python
from sklearn.ensemble import IsolationForest
import pandas as pd
import numpy as np

# Generate sample data with anomalies
rng = np.random.RandomState(42)
X = 0.3 * rng.randn(100, 2)
X_outliers = rng.uniform(low=-4, high=4, size=(20, 2))
X = np.r_[X + 2, X - 2, X_outliers] # Add two clusters and outliers

clf = IsolationForest(random_state=42)
clf.fit(X)
y_pred_train = clf.predict(X)

# Anomalies are predicted as -1
anomalies_idx = np.where(y_pred_train == -1)[0]
print("Isolation Forest detected anomalies at indices:", anomalies_idx)
```

#### One-Class SVM
A type of Support Vector Machine that is trained only on "normal" data points and learns a boundary that encapsulates them. Any data point falling outside this boundary is considered an anomaly.
```python
from sklearn.svm import OneClassSVM

# Assuming X contains mostly normal data
# Fit the model (nu is an upper bound on the fraction of training errors
# and a lower bound of the fraction of support vectors)
oc_svm = OneClassSVM(nu=0.1, kernel="rbf", gamma=0.1)
oc_svm.fit(X)

y_pred_ocsvm = oc_svm.predict(X)
anomalies_ocsvm_idx = np.where(y_pred_ocsvm == -1)[0]
print("One-Class SVM detected anomalies at indices:", anomalies_ocsvm_idx)
```

#### Local Outlier Factor (LOF)
Measures the local deviation of a given data point with respect to its neighbors. It considers as outliers those samples that have a substantially lower density than their neighbors.
```python
from sklearn.neighbors import LocalOutlierFactor

# LOF works best when you don't fit it to the data
# just compute the scores on new data.
# However, for demonstration, we'll fit and predict on the same data.
lof = LocalOutlierFactor(n_neighbors=20, contamination=0.1) # Contamination is the proportion of outliers
y_pred_lof = lof.fit_predict(X)

anomalies_lof_idx = np.where(y_pred_lof == -1)[0]
print("LOF detected anomalies at indices:", anomalies_lof_idx)
```

### 3. Time Series Specific Methods

#### ETS / ARIMA with Residual Analysis
Model the time series, then analyze the residuals. Large residuals indicate anomalies.
```python
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.arima.model import ARIMA
import matplotlib.pyplot as plt

# Example time series data (replace with your actual data)
n_samples = 100
time_series_data = pd.Series(np.random.randn(n_samples)).cumsum() + np.linspace(0, 10, n_samples)
time_series_data[50] += 50 # Introduce an anomaly

# Decompose time series to observe trend, seasonality, and residuals
decomposition = seasonal_decompose(time_series_data, model='additive', period=10)
# decomposition.plot()
# plt.show()

# Fit ARIMA model
# model = ARIMA(time_series_data, order=(5,1,0))
# model_fit = model.fit()
# residuals = pd.Series(model_fit.resid)

# Anomaly detection on residuals (e.g., using Z-score on residuals)
# from scipy.stats import zscore
# anomaly_threshold = 3
# anomalies = time_series_data[np.abs(zscore(residuals)) > anomaly_threshold]
# print("Time Series Anomalies:\n", anomalies)
```

## Workflow

1.  **Understand the Data**: What is "normal" behavior? What are potential anomaly types?
2.  **Data Preprocessing**: Handle missing values, normalize/standardize features, perform feature engineering.
3.  **Choose a Technique**: Select an appropriate algorithm based on data characteristics (e.g., univariate/multivariate, time series, labeled/unlabeled).
4.  **Model Training (if applicable)**: Train the model on normal data or mixed data (for supervised/semi-supervised methods).
5.  **Anomaly Scoring/Detection**: Get anomaly scores for new data points and apply a threshold.
6.  **Evaluation**: Assess the performance of the anomaly detection system using appropriate metrics (e.g., precision, recall, F1-score if labels are available).
7.  **Interpretation and Action**: Investigate detected anomalies and take appropriate action.
