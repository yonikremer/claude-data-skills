# Spec: CuPy Signal Processing Mastery

## 1. Overview
This project aims to research, verify, and document the use of `cupyx.scipy.signal` (CuPy v14.0.1) for high-performance signal processing. The goal is to provide a "Gold Standard" `SKILL.md` that enables developers to leverage GPU acceleration for common DSP tasks like filtering, spectral analysis, and LTI system simulation.

## 2. Research Goals
- Identify the scope of `cupyx.scipy.signal` API (v14.0.1).
- Benchmark performance against `scipy.signal` for various signal sizes.
- Verify "drop-in" compatibility and identify edge cases where behavior diverges.
- Document best practices for memory management and asynchronous execution.

## 3. Success Criteria
- [ ] Comprehensive test scaffold covering Filtering, FFT/Spectral, and LTI systems.
- [ ] Empirically verified performance gains (>10x for large signals).
- [ ] "Wall of Shame" documenting pitfalls (PCIe overhead, Async timing, FFT cache).
- [ ] "Gold Standard" `SKILL.md` generated and reviewed.

## 4. Proposed Approaches

### Approach A: Comprehensive Empirical Benchmarking (Recommended)
Systematically test functional groups (Convolution/Filtering, Spectral Analysis, Filter Design, LTI) using a dedicated test script that compares CuPy and SciPy results/times.
- **Pros**: Highest confidence, clear performance data.
- **Cons**: Takes more time to implement.

### Approach B: Documentation-First Synthesis
Rely primarily on official documentation and existing benchmarks to create the skill.
- **Pros**: Faster delivery.
- **Cons**: Lacks empirical verification on the specific hardware (RTX 4050).

**Recommendation**: Approach A. The RTX 4050 provides a unique mobile GPU context that should be verified.

## 5. Design

### Functional Groups to Verify
1. **Filtering**: `lfilter`, `filtfilt`, `sosfilt`.
2. **Spectral**: `periodogram`, `welch`, `spectrogram`.
3. **Convolution**: `convolve`, `fftconvolve`.
4. **LTI**: `dlsim`, `dimpulse`.

### Scaffolding Design
A Python script `tests/cupy_signal_explorer/benchmark_runner.py` that:
- Generates test signals on CPU.
- Transfers to GPU.
- Runs CuPy and SciPy versions.
- Asserts results are numerically close (`cp.allclose`).
- Measures time using `cupyx.profiler.benchmark`.

### "Wall of Shame" Categories
- **PCIe Latency**: When small arrays are slower on GPU.
- **Async Pitfall**: Measuring time without synchronization.
- **In-Place Mutations**: Unexpected behavior with view vs copy.
- **API Gaps**: Functions present in SciPy but missing in CuPy.
