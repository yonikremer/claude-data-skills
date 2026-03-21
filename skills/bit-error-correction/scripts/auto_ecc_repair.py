#!/usr/bin/env python3
"""
Auto ECC Repair & Discovery
Attempts to detect and fix bit-level corruption using multiple ECC strategies.
"""

import sys
import binascii
import zlib
from pathlib import Path
import numpy as np

try:
    import magic
    HAS_MAGIC = True
except ImportError:
    HAS_MAGIC = False

try:
    from reedsolo import RSCodec, ReedSolomonError
    HAS_REEDSOLO = True
except ImportError:
    HAS_REEDSOLO = False

def brute_force_bitflips(data, max_bytes=1024):
    """Try flipping every single bit in the first max_bytes and check for file type change."""
    if not HAS_MAGIC:
        return "Skip bitflip: python-magic not installed"
    
    print(f"[*] Brute-forcing single bit-flips in first {min(len(data), max_bytes)} bytes...")
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
        data_list[i] = original # reset
        
    return results

def check_common_checksums(data):
    """Calculate common checksums to see if they match any known patterns."""
    results = {
        "CRC32": binascii.crc32(data) & 0xffffffff,
        "Adler32": zlib.adler32(data) & 0xffffffff,
    }
    return results

def try_reedsolo(data, max_ecc=32):
    """Attempt Reed-Solomon correction with varying ECC lengths."""
    if not HAS_REEDSOLO:
        return "Skip RS: reedsolo not installed"
    
    print(f"[*] Attempting Reed-Solomon recovery (ECC lengths 2 to {max_ecc})...")
    results = []
    # Try common block sizes/ECC lengths
    for ecc_len in [2, 4, 8, 16, 32]:
        if ecc_len >= len(data): break
        try:
            rs = RSCodec(ecc_len)
            decoded, corrected, errata = rs.decode(data)
            if len(errata) > 0:
                results.append((ecc_len, len(errata), decoded))
        except ReedSolomonError:
            continue
    return results

def main():
    if len(sys.argv) < 2:
        print("Usage: python auto_ecc_repair.py <file>")
        sys.exit(1)

    path = Path(sys.argv[1])
    with open(path, 'rb') as f:
        data = f.read()

    print(f"=== Auto ECC Discovery for {path.name} ===")
    
    # 1. Check Checksums
    sums = check_common_checksums(data)
    print("\n[+] Common Checksums:")
    for k, v in sums.items():
        print(f"    {k}: {hex(v)}")

    # 2. Try Bitflips
    flip_results = brute_force_bitflips(data)
    if flip_results and isinstance(flip_results, list):
        print("\n[!] Significant Bit-flip Discoveries:")
        for pos, bit, mime in flip_results[:5]:
            print(f"    Byte {pos}, Bit {bit} -> Found {mime}")
    elif not flip_results:
        print("\n[-] No single bit-flip resulted in a recognized file header.")

    # 3. Try Reed-Solomon
    rs_results = try_reedsolo(data)
    if rs_results and isinstance(rs_results, list):
        print("\n[!] Reed-Solomon Potential Fixes:")
        for ecc, err_count, decoded in rs_results:
            print(f"    ECC Length {ecc}: Corrected {err_count} errors.")
            # Verify if corrected data is recognized
            if HAS_MAGIC:
                mime = magic.from_buffer(decoded, mime=True)
                print(f"    -> Resulting MIME: {mime}")
    else:
        print("\n[-] No Reed-Solomon blocks detected with common ECC lengths.")

if __name__ == "__main__":
    main()
