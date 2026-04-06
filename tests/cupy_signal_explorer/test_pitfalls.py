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
    res = cp_signal.lfilter(*[cp.asarray(x) for x in sp_signal.butter(3, 0.1)], g_data)
    _ = cp.asnumpy(res)
    gpu_t = time.time() - start
    
    print(f"Size {size} - CPU: {cpu_t:.6f}s, GPU (w/ transfer): {gpu_t:.6f}s")
    if gpu_t > cpu_t:
        print("!!! VERIFIED: GPU is SLOWER for small arrays due to transfer overhead.")

def test_async_pitfall():
    print("\n[Pitfall] Async Timing (The False Speedup)")
    size = 10**7
    g_data = cp.asarray(np.random.randn(size).astype(np.float32))
    b, a = [cp.asarray(x) for x in sp_signal.butter(3, 0.1)]
    
    start = time.time()
    _ = cp_signal.lfilter(b, a, g_data)
    wrong_t = time.time() - start
    
    start = time.time()
    _ = cp_signal.lfilter(b, a, g_data)
    cp.cuda.Device().synchronize()
    correct_t = time.time() - start
    
    print(f"Async measurement: {wrong_t:.6f}s")
    print(f"Synced measurement: {correct_t:.6f}s")
    
    if wrong_t > 0:
        print(f"Error Factor: {correct_t/wrong_t:.1f}x")
    else:
        print("Error Factor: Infinite (Async timing was near-zero)")

if __name__ == "__main__":
    test_pcie_bottleneck()
    test_async_pitfall()
