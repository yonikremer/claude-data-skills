---
name: timesfm-forecasting
description: Use when performing zero-shot time series forecasting using Google's TimesFM foundation models. Supports univariate forecasting with highly accurate prediction intervals. CRITICAL: Run `get-available-resources` first; requires ~4GB VRAM or 8GB RAM.
---

# TimesFM Zero-Shot Forecasting

Professional workflow for generating high-accuracy time series forecasts without model training.

## ⚠️ Mandatory Pre-flight: Resource Check

TimesFM 2.5 is a 200M parameter foundation model and requires significant resources.

1. **Run Detection**: Execute `python skills/get-available-resources/scripts/detect_resources.py`.
2. **Strategy**:
    - **GPU Available (>=4GB VRAM)**: Use `torch` backend with CUDA.
    - **CPU Only (>=8GB RAM)**: Use `torch` or `transformers` backend. Expect ~1-5s per forecast.
    - **Low Memory (<8GB RAM)**: Use smaller batch sizes or sample the data.

---

## 1. Core Workflow

TimesFM follows a **Load -> Compile -> Forecast** pattern.

### Step 1: Model Initialization

```python
from timesfm import TimesFM_2p5_200M_torch
model = TimesFM_2p5_200M_torch.from_pretrained("google/timesfm-2.5-200m-pytorch")
```

### Step 2: Compilation (Configuring constraints)

```python
from timesfm import ForecastConfig
model.compile(ForecastConfig(
    max_context=1024,
    max_horizon=256,
    normalize_inputs=True,  # RECOMMENDED
    infer_is_positive=True  # Set False for negative values (e.g. returns)
))
```

### Step 3: Inference

```python
# inputs: list of 1D numpy arrays
point_forecast, quantile_forecast = model.forecast(horizon=24, inputs=my_data_list)
```

---

## 2. Best Practices

- **Context Length**: Provide at least 2-3x the horizon length for context if possible.
- **Normalization**: Always set `normalize_inputs=True` unless your data is already zero-mean unit-variance.
- **Positivity**: Use `infer_is_positive=True` (default) for sales, demand, and prices to avoid negative forecasts.
- **Intervals**: Use `quantile_forecast` for uncertainty. Index `[0]` is mean, `[1-9]` are quantiles 10-90.

---

## 🛠️ Common Pitfalls (The "Wall of Shame")

1. **Missing Compilation**: Calling `forecast()` before `compile()` will raise a `RuntimeError`.
2. **Wrong Input Format**: `forecast()` expects a **list** of arrays, even for a single series. Use `[my_array]`.
3. **Internal NaNs**: While the model interpolates them, high NaN density ( >10% ) will significantly degrade accuracy.
4. **Large Batch OOM**: Processing 1000s of series at once on a small GPU. Reduce `per_core_batch_size`.

## References

- `skills/machine-learning/timesfm-forecasting/references/api_reference.md` — Full parameter list and output shapes.
- `skills/machine-learning/timesfm-forecasting/references/data_preparation.md` — Handling NaNs, frequency detection, and
  scaling.
