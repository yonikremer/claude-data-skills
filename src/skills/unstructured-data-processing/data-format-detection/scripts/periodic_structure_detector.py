#!/usr/bin/env python3
"""
Bitwise Periodic Structure Detector.

Finds the underlying bit-level frame size/periodicity of a binary file by
checking self-similarity at various bit-offsets.
"""

import sys
from pathlib import Path
from typing import List, Optional, Tuple

import numpy as np


def find_bitwise_periodicity(
    data: bytes, max_bit_period: Optional[int] = None
) -> List[Tuple[int, float]]:
    """
    Find the most likely bit-period by calculating average absolute difference between bit-frames.

    Args:
        data: The binary data to analyze.
        max_bit_period: Maximum bit-period to check. Defaults to half the file size.

    Returns:
        A list of top 10 likely bit-periods and their similarity scores (lower is better).
    """
    # Convert bytes to bits
    bits = np.unpackbits(np.frombuffer(data, dtype=np.uint8))
    n_bits = len(bits)

    if max_bit_period is None:
        max_bit_period = n_bits // 2

    max_bit_period = min(max_bit_period, n_bits // 2)

    scores = []

    # We use a step for very large files to keep it responsive,
    # but the logic allows going up to file size.
    # For bitwise research, we usually check up to a few thousand bits unless specified.
    for period in range(1, max_bit_period + 1):
        n_frames = n_bits // period
        if n_frames < 2:
            continue

        # Limit frames for performance if file is huge
        actual_frames = min(n_frames, 1000)

        frames = bits[: actual_frames * period].reshape((actual_frames, period))
        # XOR adjacent frames (similarity = low number of set bits in diff)
        diffs = np.logical_xor(frames[:-1], frames[1:])
        mean_diff = float(np.mean(diffs))

        scores.append((period, mean_diff))

    # Sort by score ascending (lowest mean diff = most similar)
    scores.sort(key=lambda x: x[1])
    return scores[:10]


def main() -> None:
    """Main CLI interface for periodic structure detection."""
    if len(sys.argv) < 2:
        print("Usage: python periodic_structure_detector.py <file> [max_bits]")
        sys.exit(1)

    path = Path(sys.argv[1])
    if not path.exists():
        print(f"Error: {path} not found")
        sys.exit(1)

    max_bits = int(sys.argv[2]) if len(sys.argv) > 2 else None

    # Read the file
    with open(path, "rb") as f:
        data = f.read()

    print(
        f"Analyzing {path.name} ({len(data)} bytes) for bitwise periodic structures..."
    )
    top_periods = find_bitwise_periodicity(data, max_bits)

    print("\nTop 10 likely bit-frame sizes (lower mean diff is better):")
    print(f"{'Bit Period':<15} | {'Byte Equiv':<15} | {'Bit Similarity Score':<20}")
    print("-" * 55)
    for period, score in top_periods:
        byte_equiv = f"{period / 8:.3f}" if period % 8 != 0 else str(period // 8)
        print(f"{period:<15} | {byte_equiv:<15} | {score:<20.6f}")


if __name__ == "__main__":
    main()
