#!/usr/bin/env python3
"""
Auto ECC Repair & Discovery.

Attempts to detect and fix bit-level corruption using multiple ECC strategies.
"""

import binascii
import sys
import zlib
from pathlib import Path
from typing import Dict, List, Tuple

import magic
from reedsolo import ReedSolomonError, RSCodec


def brute_force_bitflips(
        data: bytes, max_bytes: int = 1024
) -> List[Tuple[int, int, str]]:
    """
    Try flipping every single bit in the first max_bytes and check for file type change.

    Args:
        data: The binary data to check.
        max_bytes: Maximum number of bytes to search from the beginning.

    Returns:
        A list of tuples (byte_index, bit_index, detected_mime) where a change was found.
    """
    print(
        f"[*] Brute-forcing single bit-flips in first {min(len(data), max_bytes)} bytes..."
    )
    data_list = bytearray(data)
    results = []

    # Only check the beginning of the file where headers usually are
    search_range = min(len(data), max_bytes)

    for i in range(search_range):
        original = data_list[i]
        for bit in range(8):
            data_list[i] = original ^ (1 << bit)
            mime = magic.from_buffer(data_list, mime=True)
            if "octet-stream" not in mime and "data" not in mime:
                results.append((i, bit, mime))
        data_list[i] = original  # reset

    return results


def check_common_checksums(data: bytes) -> Dict[str, int]:
    """
    Calculate common checksums to see if they match any known patterns.

    Args:
        data: The binary data to check.

    Returns:
        A dictionary mapping checksum algorithm names to their calculated values.
    """
    results = {
        "CRC32": binascii.crc32(data) & 0xFFFFFFFF,
        "Adler32": zlib.adler32(data) & 0xFFFFFFFF,
    }
    return results


def try_reedsolo(data: bytes, max_ecc: int = 32) -> List[Tuple[int, int, bytes]]:
    """
    Attempt Reed-Solomon correction with varying ECC lengths.

    Args:
        data: The binary data to attempt correction on.
        max_ecc: Maximum ECC length to try.

    Returns:
        A list of tuples (ecc_len, error_count, corrected_data) for successful corrections.
    """
    print(f"[*] Attempting Reed-Solomon recovery (ECC lengths 2 to {max_ecc})...")
    results = []
    # Try common block sizes/ECC lengths
    for ecc_len in [2, 4, 8, 16, 32]:
        if ecc_len >= len(data):
            break
        try:
            rs = RSCodec(ecc_len)
            decoded, corrected, errata = rs.decode(data)
            if len(errata) > 0:
                results.append((ecc_len, len(errata), decoded))
        except (ReedSolomonError, ValueError):
            continue
    return results


def main() -> None:
    """Main CLI interface for Auto ECC Discovery."""
    if len(sys.argv) < 2:
        print("Usage: python auto_ecc_repair.py <file>")
        sys.exit(1)

    path = Path(sys.argv[1])
    if not path.exists():
        print(f"Error: File {path} not found.")
        sys.exit(1)

    with open(path, "rb") as f:
        data = f.read()

    print(f"=== Auto ECC Discovery for {path.name} ===")

    # 1. Check Checksums
    sums = check_common_checksums(data)
    print("\n[+] Common Checksums:")
    for k, v in sums.items():
        print(f"    {k}: {hex(v)}")

    # 2. Try Bitflips
    flip_results = brute_force_bitflips(data)
    if flip_results:
        print("\n[!] Significant Bit-flip Discoveries:")
        for pos, bit, mime in flip_results[:5]:
            print(f"    Byte {pos}, Bit {bit} -> Found {mime}")
    else:
        print("\n[-] No single bit-flip resulted in a recognized file header.")

    # 3. Try Reed-Solomon
    rs_results = try_reedsolo(data)
    if rs_results:
        print("\n[!] Reed-Solomon Potential Fixes:")
        for ecc, err_count, decoded in rs_results:
            print(f"    ECC Length {ecc}: Corrected {err_count} errors.")
            # Verify if corrected data is recognized
            mime = magic.from_buffer(decoded, mime=True)
            print(f"    -> Resulting MIME: {mime}")
    else:
        print("\n[-] No Reed-Solomon blocks detected with common ECC lengths.")


if __name__ == "__main__":
    main()
