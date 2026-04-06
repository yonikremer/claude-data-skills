# CuPy Signal Processing Mastery Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Research, verify, and document `cupyx.scipy.signal` (CuPy v14.0.1) for GPU-accelerated signal processing.

**Architecture:** Use an empirical benchmarking scaffold to compare CuPy against SciPy across functional groups (Filtering, Spectral, Convolution, LTI). Document findings into a "Wall of Shame" and a "Gold Standard" `SKILL.md`.

**Tech Stack:** CuPy v14.0.1, SciPy, NumPy, CUDA 12.8, RTX 4050.

---

### Task 1: Basic Scaffolding & Sanity Check

**Files:**
- Create: `tests/cupy_signal_explorer/sanity_check.py`

- [ ] **Step 1: Write a minimal sanity check script**

```python
import cupy as cp
import numpy as np
from cupyx.scipy import signal
import scipy.signal as sp_signal

def test_sanity():
    # 1. Create data
    data = np.random.randn(1024).astype(np.float32)
    gpu_data = cp.asarray(data)
    
    # 2. Design filter
    b, a = sp_signal.butter(3, 0.1)
    
    # 3. Apply filter
    cpu_res = sp_signal.lfilter(b, a, data)
    gpu_res = signal.lfilter(b, a, gpu_data)
    
    # 4. Verify
    assert np.allclose(cpu_res, cp.asnumpy(gpu_res), atol=1e-5)
    print("Sanity Check Passed!")

if __name__ == "__main__":
    test_sanity()
```

- [ ] **Step 2: Run sanity check**

Run: `python tests/cupy_signal_explorer/sanity_check.py`
Expected: "Sanity Check Passed!"

- [ ] **Step 3: Commit**

```bash
git add tests/cupy_signal_explorer/sanity_check.py
git commit -m "test: add cupy signal sanity check"
```

---

### Task 2: Empirical Benchmarking Runner

**Files:**
- Create: `tests/cupy_signal_explorer/benchmark_runner.py`

- [ ] **Step 1: Implement the benchmark runner**

```python
import cupy as cp
import numpy as np
import time
from cupyx.scipy import signal as cp_signal
import scipy.signal as sp_signal
from cupyx.profiler import benchmark

def run_benchmark(func_name, sp_func, cp_func, data_size=10**6, iterations=10):
    print(f"\n--- Benchmarking {func_name} (Size: {data_size}) ---")
    
    # Setup data
    data = np.random.randn(data_size).astype(np.float32)
    gpu_data = cp.asarray(data)
    
    # Special handling for filters (using coefficients)
    if func_name in ['lfilter', 'filtfilt']:
        b, a = sp_signal.butter(3, 0.1)
        # Benchmark SciPy
        start = time.time()
        for _ in range(iterations):
            _ = sp_func(b, a, data)
        sp_time = (time.time() - start) / iterations
        
        # Benchmark CuPy (Proper way using cupyx.profiler.benchmark)
        def cp_test():
            return cp_func(b, a, gpu_data)
        
        perf = benchmark(cp_test, n_repeat=iterations)
        cp_time = perf.gpu_times.mean()
        
    elif func_name == 'welch':
        start = time.time()
        for _ in range(iterations):
            _ = sp_func(data)
        sp_time = (time.time() - start) / iterations
        
        def cp_test():
            return cp_func(gpu_data)
        
        perf = benchmark(cp_test, n_repeat=iterations)
        cp_time = perf.gpu_times.mean()

    print(f"SciPy Time: {sp_time:.6f}s")
    print(f"CuPy Time:  {cp_time:.6f}s")
    print(f"Speedup:    {sp_time/cp_time:.2f}x")

if __name__ == "__main__":
    run_benchmark('lfilter', sp_signal.lfilter, cp_signal.lfilter, data_size=10**7)
    run_benchmark('welch', sp_signal.welch, cp_signal.welch, data_size=10**7)
```

- [ ] **Step 2: Run benchmarks**

Run: `python tests/cupy_signal_explorer/benchmark_runner.py`
Expected: Detailed timing output showing speedups for 10^7 size.

- [ ] **Step 3: Commit**

```bash
git add tests/cupy_signal_explorer/benchmark_runner.py
git commit -m "test: add empirical benchmark runner for cupy signal"
```

---

### Task 3: "Wall of Shame" Pitfall Verification

**Files:**
- Create: `tests/cupy_signal_explorer/test_pitfalls.py`

- [ ] **Step 1: Write pitfall demonstration script**

```python
import cupy as cp
import numpy as np
import time
from cupyx.scipy import signal as cp_signal
import scipy.signal as sp_signal

def test_pcie_bottleneck():
    print("\n[Pitfall] PCIe Bottleneck (Small Arrays)")
    size = 1000
    data = np.random.randn(size).astype(np.float32)
    
    # CPU
    start = time.time()
    _ = sp_signal.lfilter(*sp_signal.butter(3, 0.1), data)
    cpu_t = time.time() - start
    
    # GPU with Transfer
    start = time.time()
    g_data = cp.asarray(data)
    res = cp_signal.lfilter(*sp_signal.butter(3, 0.1), g_data)
    _ = cp.asnumpy(res)
    gpu_t = time.time() - start
    
    print(f"Size {size} - CPU: {cpu_t:.6f}s, GPU (w/ transfer): {gpu_t:.6f}s")
    if gpu_t > cpu_t:
        print("!!! VERIFIED: GPU is SLOWER for small arrays due to transfer overhead.")

def test_async_pitfall():
    print("\n[Pitfall] Async Timing (The False Speedup)")
    size = 10**7
    g_data = cp.asarray(np.random.randn(size).astype(np.float32))
    b, a = sp_signal.butter(3, 0.1)
    
    start = time.time()
    _ = cp_signal.lfilter(b, a, g_data)
    wrong_t = time.time() - start
    
    start = time.time()
    _ = cp_signal.lfilter(b, a, g_data)
    cp.cuda.Device().synchronize()
    correct_t = time.time() - start
    
    print(f"Async measurement: {wrong_t:.6f}s")
    print(f"Synced measurement: {correct_t:.6f}s")
    print(f"Error Factor: {correct_t/wrong_t:.1f}x")

if __name__ == "__main__":
    test_pcie_bottleneck()
    test_async_pitfall()
```

- [ ] **Step 2: Run pitfall tests**

Run: `python tests/cupy_signal_explorer/test_pitfalls.py`
Expected: Evidence that GPU is slower for small arrays and sync timing is mandatory.

- [ ] **Step 3: Commit**

```bash
git add tests/cupy_signal_explorer/test_pitfalls.py
git commit -m "test: verify cupy signal pitfalls for wall of shame"
```

---

### Task 4: Gold Standard SKILL.md Generation

**Files:**
- Create: `src/skills/data-analysis/cupy-signal/SKILL.md`

- [ ] **Step 1: Write the final skill document**
(Draft the content based on empirical findings from previous tasks)

- [ ] **Step 2: Commit**

```bash
git add src/skills/data-analysis/cupy-signal/SKILL.md
git commit -m "docs: add gold standard cupy-signal skill"
```
