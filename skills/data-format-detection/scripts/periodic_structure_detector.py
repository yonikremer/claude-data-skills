#!/usr/bin/env python3
"""
Periodic Structure Detector
Finds the underlying frame size/periodicity of a binary file by checking 
self-similarity at various offsets.
"""

import sys
import numpy as np
from pathlib import Path

def find_periodicity(data, min_period=1, max_period=1024):
    """
    Find the most likely period (frame size) by calculating average 
    absolute difference between frames.
    """
    if len(data) < max_period * 2:
        return []

    data_arr = np.frombuffer(data, dtype=np.uint8).astype(np.int16)
    scores = []

    for period in range(min_period, max_period + 1):
        # Calculate how many full frames we can compare
        n_frames = len(data_arr) // period
        if n_frames < 2: continue
        
        # Reshape into frames and calculate mean difference between adjacent frames
        frames = data_arr[:n_frames*period].reshape((n_frames, period))
        diffs = np.abs(np.diff(frames, axis=0))
        mean_diff = np.mean(diffs)
        
        # Lower score is better (more similarity)
        scores.append((period, mean_diff))

    # Sort by score ascending
    scores.sort(key=lambda x: x[1])
    return scores[:5]

def main():
    if len(sys.argv) < 2:
        print("Usage: python periodic_structure_detector.py <file>")
        sys.exit(1)

    path = Path(sys.argv[1])
    if not path.exists():
        print(f"Error: {path} not found")
        sys.exit(1)

    # Read a sample (e.g., first 64KB)
    with open(path, 'rb') as f:
        data = f.read(65536)

    print(f"Analyzing {path.name} for periodic structures...")
    top_periods = find_periodicity(data)

    print("\nTop 5 likely frame sizes (lower mean diff is better):")
    print(f"{'Frame Size (Bytes)':<20} | {'Mean Byte Difference':<20}")
    print("-" * 45)
    for period, score in top_periods:
        print(f"{period:<20} | {score:<20.4f}")

if __name__ == "__main__":
    main()
