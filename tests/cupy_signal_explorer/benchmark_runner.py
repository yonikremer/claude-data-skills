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
        gpu_b, gpu_a = cp.asarray(b), cp.asarray(a)
        def cp_test():
            return cp_func(gpu_b, gpu_a, gpu_data)
        
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
