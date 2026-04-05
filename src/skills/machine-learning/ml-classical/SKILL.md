---
name: ml-classical
description: Use for traditional machine learning tasks: classification, regression, clustering, and dimensionality reduction. Unified guide for Scikit-Learn, UMAP (visualization), and Anomaly Detection. CRITICAL: Run `get-available-resources` first for datasets > 10^6 rows.
---

# Classical Machine Learning (Consolidated)

Unified expert guide for traditional ML workflows using the industry's most robust libraries.

## ⚠️ Mandatory Pre-flight: Data & Memory

1. **Memory Detection**: Scikit-learn typically requires 3-5x the dataset size in RAM for training.
2. **Feature Scaling**: Always scale features (`StandardScaler`, `MinMaxScaler`) before training distance-based models (
   SVM, k-Means, KNN).
3. **Reproducibility**: Always set `random_state` for consistent results.

---

## 1. Scikit-Learn (The Gold Standard)

Use for core ML tasks: classification, regression, and clustering.

### Core Idioms

- **Pipelines**: Always use `Pipeline` to wrap preprocessing and modeling to prevent data leakage.
- **Cross-Validation**: Use `cross_val_score` or `GridSearchCV` for robust performance estimation.

```python
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier

pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('rf', RandomForestClassifier(random_state=42))
])
```

---

## 2. Dimensionality Reduction (UMAP)

Use for high-performance non-linear dimensionality reduction and visualization.

### Core Idiom

- **Comparison**: UMAP is generally faster and preserves more global structure than t-SNE.

```python
import umap
reducer = umap.UMAP(n_neighbors=15, min_dist=0.1, random_state=42)
embedding = reducer.fit_transform(data)
```

---

## 3. Anomaly Detection

Use for identifying outliers and novel patterns in datasets.

### Core Tools

- **Isolation Forest**: Best for high-dimensional data.
- **Local Outlier Factor (LOF)**: Best for detecting anomalies relative to their local neighborhood.

---

## 🛠️ Common Pitfalls (The "Wall of Shame")

1. **Data Leakage**: Fitting a scaler on the entire dataset instead of just the training set.
2. **Ignoring Imbalance**: Using Accuracy for highly imbalanced datasets; use F1-score or PR-AUC instead.
3. **Overfitting**: Not using a separate test set or cross-validation for hyperparameter tuning.

## References

- `skills/machine-learning/ml-classical/references/scikit-learn/` — Model selection and evaluation.
- `skills/machine-learning/ml-classical/references/umap-learn/` — Visualization and projection tuning.
