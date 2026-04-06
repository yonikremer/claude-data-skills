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
    gpu_res = signal.lfilter(cp.asarray(b), cp.asarray(a), gpu_data)
    
    # 4. Verify
    gpu_res_cpu = cp.asnumpy(gpu_res)
    assert np.allclose(cpu_res, gpu_res_cpu, atol=1e-5)
    print("Sanity Check Passed!")

if __name__ == "__main__":
    test_sanity()
