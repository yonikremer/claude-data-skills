"""
Complete classification pipeline example.

This script demonstrates a full machine learning workflow including preprocessing,
model training, hyperparameter tuning, and evaluation.
"""

import warnings
from typing import Any, Dict, List, Union

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import GridSearchCV, cross_val_score, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

warnings.filterwarnings("ignore")


def create_preprocessing_pipeline(
    numeric_features: List[str], categorical_features: List[str]
) -> ColumnTransformer:
    """
    Create a preprocessing pipeline for mixed data types.

    Parameters:
        numeric_features: List of numeric feature column names.
        categorical_features: List of categorical feature column names.

    Returns:
        A Scikit-Learn ColumnTransformer for preprocessing.
    """
    # Numeric preprocessing
    numeric_transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]
    )

    # Categorical preprocessing
    categorical_transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="constant", fill_value="missing")),
            ("onehot", OneHotEncoder(handle_unknown="ignore", sparse_output=False)),
        ]
    )

    # Combine transformers
    preprocessor = ColumnTransformer(
        transformers=[
            ("num", numeric_transformer, numeric_features),
            ("cat", categorical_transformer, categorical_features),
        ]
    )

    return preprocessor


def train_and_evaluate_model(
    x_data: Union[pd.DataFrame, np.ndarray],
    y_data: Union[pd.Series, np.ndarray],
    numeric_features: List[str],
    categorical_features: List[str],
    test_size: float = 0.2,
    random_state: int = 42,
) -> Dict[str, Any]:
    """
    Complete pipeline: preprocess, train, tune, and evaluate a classifier.

    Parameters:
        x_data: Feature matrix.
        y_data: Target variable.
        numeric_features: List of numeric feature names.
        categorical_features: List of categorical feature names.
        test_size: Proportion of data for testing.
        random_state: Random seed for reproducibility.

    Returns:
        Dictionary containing trained model, predictions, and metrics.
    """
    # Split data with stratification
    x_train, x_test, y_train, y_test = train_test_split(
        x_data, y_data, test_size=test_size, stratify=y_data, random_state=random_state
    )

    print(f"Training set size: {len(x_train)}")
    print(f"Test set size: {len(x_test)}")
    print(
        f"Class distribution in training: {pd.Series(y_train).value_counts().to_dict()}"
    )

    # Create preprocessor
    preprocessor = create_preprocessing_pipeline(numeric_features, categorical_features)

    # Define models to compare
    models = {
        "Logistic Regression": Pipeline(
            [
                ("preprocessor", preprocessor),
                (
                    "classifier",
                    LogisticRegression(max_iter=1000, random_state=random_state),
                ),
            ]
        ),
        "Random Forest": Pipeline(
            [
                ("preprocessor", preprocessor),
                (
                    "classifier",
                    RandomForestClassifier(n_estimators=100, random_state=random_state),
                ),
            ]
        ),
        "Gradient Boosting": Pipeline(
            [
                ("preprocessor", preprocessor),
                (
                    "classifier",
                    GradientBoostingClassifier(
                        n_estimators=100, random_state=random_state
                    ),
                ),
            ]
        ),
    }

    # Compare models using cross-validation
    print("\n" + "=" * 60)
    print("Model Comparison (5-Fold Cross-Validation)")
    print("=" * 60)

    cv_results = {}
    for name, model in models.items():
        scores = cross_val_score(model, x_train, y_train, cv=5, scoring="accuracy")
        cv_results[name] = scores.mean()
        print(f"{name:20s}: {scores.mean():.4f} (+/- {scores.std() * 2:.4f})")

    # Select best model based on CV
    best_model_name = max(cv_results, key=cv_results.get)
    best_model = models[best_model_name]

    print(f"\nBest model: {best_model_name}")

    # Hyperparameter tuning for best model
    if best_model_name == "Random Forest":
        param_grid = {
            "classifier__n_estimators": [100, 200],
            "classifier__max_depth": [10, 20, None],
            "classifier__min_samples_split": [2, 5],
        }
    elif best_model_name == "Gradient Boosting":
        param_grid = {
            "classifier__n_estimators": [100, 200],
            "classifier__learning_rate": [0.01, 0.1],
            "classifier__max_depth": [3, 5],
        }
    else:  # Logistic Regression
        param_grid = {
            "classifier__C": [0.1, 1.0, 10.0],
            "classifier__penalty": ["l2"],
        }

    print("\n" + "=" * 60)
    print("Hyperparameter Tuning")
    print("=" * 60)

    grid_search = GridSearchCV(
        best_model, param_grid, cv=5, scoring="accuracy", n_jobs=-1, verbose=0
    )

    grid_search.fit(x_train, y_train)

    print(f"Best parameters: {grid_search.best_params_}")
    print(f"Best CV score: {grid_search.best_score_:.4f}")

    # Evaluate on test set
    tuned_model = grid_search.best_estimator_
    y_pred = tuned_model.predict(x_test)
    y_pred_proba = tuned_model.predict_proba(x_test)

    print("\n" + "=" * 60)
    print("Test Set Evaluation")
    print("=" * 60)

    # Calculate metrics
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, average="weighted")
    recall = recall_score(y_test, y_pred, average="weighted")
    f_one = f1_score(y_test, y_pred, average="weighted")

    print(f"Accuracy:  {accuracy:.4f}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall:    {recall:.4f}")
    print(f"F1-Score:  {f_one:.4f}")

    # ROC AUC (if binary classification)
    if len(np.unique(y_data)) == 2:
        roc_auc = roc_auc_score(y_test, y_pred_proba[:, 1])
        print(f"ROC AUC:   {roc_auc:.4f}")

    print("\n" + "=" * 60)
    print("Classification Report")
    print("=" * 60)
    print(classification_report(y_test, y_pred))

    print("\n" + "=" * 60)
    print("Confusion Matrix")
    print("=" * 60)
    print(confusion_matrix(y_test, y_pred))

    # Feature importance (if available)
    if hasattr(tuned_model.named_steps["classifier"], "feature_importances_"):
        print("\n" + "=" * 60)
        print("Top 10 Most Important Features")
        print("=" * 60)

        feature_names = tuned_model.named_steps["preprocessor"].get_feature_names_out()
        importances = tuned_model.named_steps["classifier"].feature_importances_

        feature_importance_df = (
            pd.DataFrame({"feature": feature_names, "importance": importances})
            .sort_values("importance", ascending=False)
            .head(10)
        )

        print(feature_importance_df.to_string(index=False))

    return {
        "model": tuned_model,
        "y_test": y_test,
        "y_pred": y_pred,
        "y_pred_proba": y_pred_proba,
        "metrics": {
            "accuracy": accuracy,
            "precision": precision,
            "recall": recall,
            "f1": f_one,
        },
    }


# Example usage
if __name__ == "__main__":
    # Load example dataset
    from sklearn.datasets import load_breast_cancer

    # Load data
    data_pkg = load_breast_cancer()
    x_in = pd.DataFrame(data_pkg.data, columns=data_pkg.feature_names)
    y_in = data_pkg.target

    # For demonstration, treat all features as numeric
    numeric_feat = x_in.columns.tolist()
    categorical_feat: List[str] = []

    print("=" * 60)
    print("Classification Pipeline Example")
    print("Dataset: Breast Cancer Wisconsin")
    print("=" * 60)

    # Run complete pipeline
    results_dict = train_and_evaluate_model(
        x_in, y_in, numeric_feat, categorical_feat, test_size=0.2, random_state=42
    )

    print("\n" + "=" * 60)
    print("Pipeline Complete!")
    print("=" * 60)
