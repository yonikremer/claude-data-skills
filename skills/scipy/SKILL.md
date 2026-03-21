---
name: scipy
description: Scientific computing with SciPy — statistics, signal processing, optimization, interpolation, linear algebra, integration, and spatial operations. Use for hypothesis testing, curve fitting, filtering signals, solving equations, and numerical methods beyond what numpy provides.
license: https://github.com/scipy/scipy/blob/main/LICENSE.txt
metadata:
    skill-author: K-Dense Inc.
---

# SciPy

## Overview

SciPy builds on NumPy and provides domain-specific scientific algorithms. Key submodules:

| Module | Use For |
|--------|---------|
| `scipy.stats` | Distributions, hypothesis tests, descriptive stats |
| `scipy.signal` | Filtering, FFT, peak detection, spectral analysis |
| `scipy.optimize` | Curve fitting, root finding, minimization |
| `scipy.interpolate` | Interpolate between data points |
| `scipy.linalg` | Linear algebra (prefer over numpy.linalg) |
| `scipy.integrate` | Numerical integration, ODEs |
| `scipy.spatial` | KD-trees, distance matrices, convex hull |
| `scipy.io` | MATLAB .mat files, WAV audio, netCDF |

```bash
pip install scipy
```

## scipy.stats — Statistics

### Descriptive statistics

```python
from scipy import stats
import numpy as np

data = np.array([2.1, 3.4, 2.8, 4.1, 3.9, 2.5, 3.7])

stats.describe(data)
# nobs=7, minmax=(2.1, 4.1), mean=3.21, variance=0.46, skewness=..., kurtosis=...

stats.zscore(data)             # standardize to z-scores
stats.iqr(data)                # interquartile range
stats.sem(data)                # standard error of mean
stats.trim_mean(data, 0.1)     # 10% trimmed mean (robust to outliers)
stats.mode(data)               # most common value
```

### Hypothesis tests

```python
# t-test: compare means
stats.ttest_1samp(data, popmean=3.0)          # one-sample vs known mean
stats.ttest_ind(group_a, group_b)              # two independent groups
stats.ttest_rel(before, after)                 # paired samples

# Non-parametric alternatives
stats.mannwhitneyu(group_a, group_b)           # non-parametric two-sample
stats.wilcoxon(before, after)                  # paired non-parametric
stats.kruskal(g1, g2, g3)                      # non-parametric ANOVA

# Normality tests
stats.shapiro(data)                            # Shapiro-Wilk (small n)
stats.normaltest(data)                         # D'Agostino-Pearson
stats.kstest(data, 'norm')                     # Kolmogorov-Smirnov

# Chi-squared
stats.chisquare(observed, expected)            # goodness of fit
stats.chi2_contingency(contingency_table)      # independence test

# Correlation
stats.pearsonr(x, y)     # Pearson r + p-value
stats.spearmanr(x, y)    # Spearman rank correlation
stats.kendalltau(x, y)   # Kendall tau

# All tests return (statistic, p_value)
t_stat, p_val = stats.ttest_ind(group_a, group_b)
print(f"t={t_stat:.3f}, p={p_val:.4f}, {'significant' if p_val < 0.05 else 'not significant'}")
```

### Probability distributions

```python
from scipy.stats import norm, expon, poisson, uniform, lognorm

# PDF, CDF, PPF (inverse CDF), RVS (random samples)
norm.pdf(x=1.96)           # probability density at x
norm.cdf(1.96)             # P(X <= 1.96) ≈ 0.975
norm.ppf(0.975)            # quantile: value where CDF = 0.975 → 1.96
norm.sf(1.96)              # survival: P(X > 1.96)
norm.interval(0.95)        # 95% confidence interval

# With parameters
norm(loc=10, scale=2).rvs(size=1000)    # samples from N(10, 2²)
expon(scale=1/0.5).rvs(size=1000)       # exponential with rate=0.5

# Fit distribution to data
mu, sigma = norm.fit(data)
shape, loc, scale = lognorm.fit(data, floc=0)

# Q-Q plot
import matplotlib.pyplot as plt
stats.probplot(data, dist='norm', plot=plt)
plt.show()
```

## scipy.signal — Signal Processing

```python
from scipy import signal
import numpy as np

# --- Filtering ---

# Design a Butterworth low-pass filter
fs = 1000        # sample rate (Hz)
fc = 50          # cutoff frequency (Hz)
order = 4

b, a = signal.butter(order, fc, btype='low', fs=fs)
filtered = signal.filtfilt(b, a, raw_signal)   # zero-phase filtering

# Band-pass filter (keep frequencies between f1 and f2)
b, a = signal.butter(order, [10, 100], btype='band', fs=fs)
filtered = signal.filtfilt(b, a, raw_signal)

# Savitzky-Golay filter (smooth while preserving peaks)
filtered = signal.savgol_filter(raw_signal, window_length=11, polyorder=3)

# --- Spectral Analysis ---

# FFT
freqs = np.fft.rfftfreq(len(signal_data), d=1/fs)
fft_vals = np.abs(np.fft.rfft(signal_data))

# Power Spectral Density (Welch method — more robust than raw FFT)
freqs, psd = signal.welch(signal_data, fs=fs, nperseg=256)

# Spectrogram
f, t, Sxx = signal.spectrogram(signal_data, fs=fs)
import matplotlib.pyplot as plt
plt.pcolormesh(t, f, 10 * np.log10(Sxx))

# --- Peak Detection ---
peaks, properties = signal.find_peaks(
    signal_data,
    height=0.5,          # minimum peak height
    distance=50,         # minimum samples between peaks
    prominence=0.3,      # minimum prominence
    width=5,             # minimum peak width
)
peak_times = peaks / fs  # convert sample index to seconds

# --- Resampling ---
resampled = signal.resample(signal_data, num=new_n_samples)
resampled = signal.resample_poly(signal_data, up=4, down=5)   # rational ratio

# --- Correlation ---
correlation = signal.correlate(signal_a, signal_b, mode='full')
lag = np.argmax(correlation) - (len(signal_b) - 1)   # time lag at max correlation
```

## scipy.optimize — Curve Fitting and Minimization

```python
from scipy.optimize import curve_fit, minimize, fsolve, brentq

# --- Curve Fitting ---
def model(x, a, b, c):
    return a * np.exp(-b * x) + c

xdata = np.linspace(0, 4, 50)
ydata = model(xdata, 2.5, 1.3, 0.5) + np.random.normal(0, 0.1, 50)

params, covariance = curve_fit(model, xdata, ydata)
a_fit, b_fit, c_fit = params
errors = np.sqrt(np.diag(covariance))   # 1-sigma parameter uncertainties

# With bounds
params, _ = curve_fit(model, xdata, ydata, bounds=([0,0,0], [10,5,2]))

# --- Minimization ---
def cost(params):
    a, b = params
    pred = a * xdata + b
    return np.sum((pred - ydata)**2)

result = minimize(cost, x0=[1.0, 0.0], method='Nelder-Mead')
result.x        # optimal parameters
result.success  # bool

# With gradient (faster)
result = minimize(cost, x0=[1.0, 0.0], method='L-BFGS-B',
                  bounds=[(-10, 10), (-10, 10)])

# --- Root Finding ---
def f(x):
    return x**3 - 2*x - 5

root = brentq(f, 1, 3)         # find root between 1 and 3
roots = fsolve(f, x0=2.0)      # general root finder (may converge to local root)
```

## scipy.interpolate

```python
from scipy.interpolate import interp1d, CubicSpline, griddata

x = np.array([0, 1, 2, 3, 4, 5])
y = np.array([0, 1, 4, 9, 16, 25])

# 1D interpolation
f_linear = interp1d(x, y, kind='linear')
f_cubic  = interp1d(x, y, kind='cubic')
f_cubic  = interp1d(x, y, kind='cubic', fill_value='extrapolate')

x_new = np.linspace(0, 5, 100)
y_new = f_cubic(x_new)

# Cubic spline (smoother, better for scientific data)
cs = CubicSpline(x, y)
y_new = cs(x_new)
dy_dx = cs(x_new, 1)    # first derivative

# 2D / ND interpolation (scattered points)
points = np.random.rand(100, 2)   # (x, y) coordinates
values = np.sin(points[:, 0]) * np.cos(points[:, 1])

grid_x, grid_y = np.mgrid[0:1:100j, 0:1:100j]
grid_z = griddata(points, values, (grid_x, grid_y), method='cubic')
```

## scipy.io — File I/O

```python
from scipy import io

# MATLAB .mat files
mat = io.loadmat('data.mat')       # dict of arrays
io.savemat('out.mat', {'x': arr, 'y': arr2})

# MATLAB v7.3 (HDF5-based, use h5py instead)
# io.loadmat raises error for v7.3 — use h5py

# WAV audio files
sample_rate, data = io.wavfile.read('audio.wav')
io.wavfile.write('out.wav', rate=44100, data=audio_array)

# Fortran-formatted binary files
data = io.FortranFile('data.unf').read_reals(dtype=np.float32)
```

## scipy.spatial — Distances and Spatial Structures

```python
from scipy.spatial import KDTree, distance_matrix
from scipy.spatial.distance import cdist, pdist, squareform

# Distance matrix between two sets of points
A = np.random.rand(100, 3)
B = np.random.rand(50, 3)
D = cdist(A, B, metric='euclidean')   # (100, 50) distance matrix

# All pairwise distances within one set
D = pdist(A, metric='euclidean')      # condensed form (upper triangle)
D_sq = squareform(D)                  # convert to full (100, 100) matrix

# KD-Tree: fast nearest-neighbor queries
tree = KDTree(A)
distances, indices = tree.query(B, k=3)   # 3 nearest neighbors in A for each point in B
indices_within_r = tree.query_ball_point(B[0], r=0.1)  # all points within radius
```

## scipy.linalg

```python
from scipy import linalg
import numpy as np

A = np.array([[1, 2], [3, 4]])

# Prefer scipy.linalg over numpy.linalg — more complete and often faster
linalg.inv(A)             # inverse
linalg.det(A)             # determinant
linalg.norm(A)            # matrix norm
linalg.solve(A, b)        # solve Ax = b (prefer over inv(A) @ b)

# Decompositions
eigenvalues, eigenvectors = linalg.eig(A)
U, s, Vt = linalg.svd(A)      # singular value decomposition
L, U = linalg.lu(A)[:2]       # LU decomposition (returns P, L, U)
Q, R = linalg.qr(A)           # QR decomposition
```
