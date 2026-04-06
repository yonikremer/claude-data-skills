---
name: cupy-signal
description: GPU-accelerated signal processing using cupyx.scipy.signal. Provides a high-performance, drop-in replacement for scipy.signal on NVIDIA (CUDA) and AMD (ROCm) GPUs.
---

# CuPy Signal Processing Mastery

## Overview

`cupyx.scipy.signal` is a GPU-accelerated subset of the SciPy signal processing module. It leverages NVIDIA's CUDA libraries (cuFFT, cuSPARSE) and custom kernels to provide significant speedups (10x-100x+) for large-scale digital signal processing (DSP).

## Domain Fundamentals

Understanding the "Why" and "What" of signal processing is crucial for effective tool usage.

### 1. What is a Signal?
A signal is any quantity that varies over time, space, or another independent variable (e.g., sound waves, sensor data, or image pixels). Signal processing is the art of analyzing, modifying, or synthesizing these signals to improve quality or extract information.

### 2. Time Domain vs. Frequency Domain
- **Time Domain**: Represents how a signal's value changes over time (e.g., an oscilloscope view).
- **Frequency Domain**: Represents how much of the signal lies within each frequency band (e.g., a graphic equalizer view).

### 3. Fast Fourier Transform (FFT)
The FFT is an algorithm that efficiently converts a signal from the **Time Domain** to the **Frequency Domain**. 
- **The Concept**: It breaks down a complex signal into its constituent pure sine waves (frequencies). 
- **Why it matters**: It is the foundation of modern communications (WiFi, 5G), audio/image compression (MP3, JPEG), and spectral analysis.

### 4. Digital Filtering
A filter is a system that removes unwanted components (e.g., noise) or enhances specific features of a signal.
- **Low-Pass Filter**: Removes high-frequency noise (e.g., blurring an image or removing static hiss).
- **High-Pass Filter**: Removes low-frequency components (e.g., sharpening edges or removing low-end hum).
- **Band-Pass Filter**: Isolates a specific frequency range (e.g., picking out a human voice from background noise).

## Core Principles

1.  **Drop-in Replacement**: Most `scipy.signal` APIs are available under `cupyx.scipy.signal`.
2.  **GPU-Resident Data**: Data must be moved to the GPU (as a `cupy.ndarray`) before processing.
3.  **Vectorized Operations**: Avoid loops; use CuPy's built-in functions for maximum parallelism.
4.  **Asynchronous Execution**: GPU kernels return control to the CPU immediately. Use synchronization for accurate timing.

## Workflow

### 1. Data Transfer
Always move your data to the GPU at the beginning of your pipeline and keep it there as long as possible.

```python
import cupy as cp
import numpy as np
from cupyx.scipy import signal

# CPU to GPU
data_cpu = np.random.randn(10**7).astype(np.float32)
data_gpu = cp.asarray(data_cpu)

# GPU to CPU (Only at the end!)
res_cpu = cp.asnumpy(data_gpu)
```

### 2. Filtering
CuPy supports standard IIR and FIR filtering. Note that filter coefficients (`b`, `a`) must also be CuPy arrays.

```python
from cupyx.scipy import signal as cp_signal
import scipy.signal as sp_signal

# Design on CPU (fast)
b, a = sp_signal.butter(3, 0.1)

# Convert to GPU
b_gpu, a_gpu = cp.asarray(b), cp.asarray(a)

# Apply filter
filtered_gpu = cp_signal.lfilter(b_gpu, a_gpu, data_gpu)
```

### 3. Spectral Analysis
For large signals, `welch`, `periodogram`, and `spectrogram` offer massive speedups over SciPy.

```python
f, psd = cp_signal.welch(data_gpu, fs=1000)
```

## Common Use Cases

| Field | Application |
| :--- | :--- |
| **Audio** | Real-time noise cancellation, speech recognition, and effect processing. |
| **Communication** | Decoding high-bandwidth signals in Software Defined Radios (SDR). |
| **Biomedical** | Analyzing real-time high-sample-rate data from ECG or EEG sensors. |
| **Geophysics** | Processing seismic data to map underground structures. |
| **IoT/Vibration** | Predicting machine failure by analyzing high-frequency motor vibrations. |

## Wall of Shame (Common Pitfalls)

| Pitfall | Impact | Detection | Prevention |
| :--- | :--- | :--- | :--- |
| **PCIe Bottleneck** | GPU is 100x slower for small arrays. | Small signal sizes (< 10^5 elements) are slower on GPU. | Only use CuPy for large data or massive parallel batches. |
| **Asynchronous Timing** | False reports of "0.001s" for large tasks. | `time.time()` returns immediately after kernel launch. | Use `cupyx.profiler.benchmark` or `cp.cuda.Device().synchronize()`. |
| **Memory Fragmentation** | `OutOfMemoryError` despite low usage. | Repeatedly creating large arrays of different sizes. | Use `cp.get_default_memory_pool().free_all_blocks()` to clear cache. |
| **FFT Plan Cache** | GPU memory leaks over time. | Memory usage grows after each FFT call. | Limit cache with `cp.fft.config.set_cufft_plan_cache_max_size(0)`. |
| **Scalar Access** | Extreme slowdown (1000x+). | Accessing elements in a loop: `data_gpu[i]`. | Use vectorized CuPy functions exclusively. |

## Benchmarks (RTX 4050 Verification)

On a mobile RTX 4050 (Laptop), we observed the following speedups for a 10^7 (10M) sample signal:
-   **`lfilter`**: ~7.5x speedup.
-   **`welch`**: ~17.2x speedup.

## Supported Functional Groups (v14.0.1)

-   **Convolution**: `convolve`, `correlate`, `fftconvolve`.
-   **Filtering**: `lfilter`, `filtfilt`, `sosfilt`, `wiener`, `medfilt`.
-   **Filter Design**: `butter`, `cheby1`, `cheby2`, `ellip`, `firwin`, `iirfilter`.
-   **Spectral Analysis**: `periodogram`, `welch`, `spectrogram`, `stft`.
-   **LTI Systems**: `dlsim`, `dimpulse`, `dstep`, `freqz`.

## References
-   [Official CuPy Signal Documentation](https://docs.cupy.dev/en/stable/reference/scipy_signal.html)
-   [CuPy Comparison Table](https://docs.cupy.dev/en/stable/reference/comparison.html)
