---
name: bit-error-correction
description: Detects and repairs corrupted data using error-correcting codes (ECC). Use for recovering data from noisy channels, damaged storage, or corrupted binary streams using Hamming, Reed-Solomon, and CRCs.
---
# Bit Error Correction (ECC)

This skill provides methods for identifying and repairing bit-level corruption in data streams.

## 1. Error Detection (Check Algorithms)

Before correcting, you must detect if corruption exists.

### Cyclic Redundancy Checks (CRC)
Best for detecting burst errors in packets.
```python
import binascii

def get_crc32(data: bytes):
    # Standard CRC32 used in Ethernet/Gzip
    return binascii.crc32(data) & 0xffffffff
```

### Adler-32
Faster than CRC32 but slightly less reliable for small changes.
```python
import zlib
checksum = zlib.adler32(b"data")
```

## 2. Forward Error Correction (Correction)

### Hamming Codes (SEC-DED)
Best for single-bit errors. If 1 bit flips, Hamming can tell you exactly which one and flip it back.

**Logic**: Uses parity bits at positions that are powers of 2 (1, 2, 4, 8...).
- **Rule**: If `syndrome == 0`, no error. If `syndrome != 0`, the syndrome value is the 1-based index of the corrupted bit.

### Reed-Solomon Codes
The "Gold Standard" for burst errors (multiple contiguous bits). Used in QR codes, NASA deep space telemetry, and RAID 6.

```python
# pip install reedsolo
from reedsolo import RSCodec, ReedSolomonError

def repair_data(corrupted_data: bytes, ecc_len: int):
    rs = RSCodec(ecc_len)
    try:
        # Returns (decoded_data, corrected_data, errata_pos)
        return rs.decode(corrupted_data)[0]
    except ReedSolomonError:
        return None # Too many errors to fix
```

## 3. Auto-ECC Discovery (The "Try Everything" Approach)

If the corruption type is unknown, use the automated discovery script. It will sequentially attempt common checksum matches, single-bit flip brute forcing (looking for valid headers), and Reed-Solomon correction with variable ECC lengths.

```python
# Run automated forensic repair:
# python skills/bit-error-correction/scripts/auto_ecc_repair.py <corrupted_file>
```

### Discovery Logic:
1. **Header Reconstruction**: Flips every bit in the first 1KB and checks `python-magic` for a format match.
2. **Heuristic Reed-Solomon**: Tries common ECC power-of-2 lengths (2, 4, 8, 16, 32).
3. **Checksum Profiling**: Reports CRC32 and Adler32 to check for partial block matches.

## 4. Forensic Recovery Workflow

If you encounter a corrupted binary file from an unknown system:

1. **Calculate Entropy**: High entropy + failing checksums = likely compressed data with bit-flips.
2. **Scan for Parity**: Check if every 9th bit or every 17th bit follows a parity rule.
3. **Burst Search**: If data is mostly readable but has "static" chunks, it likely needs Reed-Solomon.
4. **Brute Force Bit-Flip**: If a file is small and a single bit-flip is suspected (e.g., a header byte), iterate through every bit and check if `python-magic` recognizes the resulting format.

```python
def brute_force_bitflip(data: bytes):
    import magic
    data_list = bytearray(data)
    for i in range(len(data_list)):
        original = data_list[i]
        for bit in range(8):
            data_list[i] = original ^ (1 << bit)
            mime = magic.from_buffer(data_list, mime=True)
            if "octet-stream" not in mime:
                print(f"Potential fix at byte {i}, bit {bit}: {mime}")
        data_list[i] = original # Reset
```

## Professional Best Practices

- **Differentiate Error Types**:
  - **Single Bit**: Use Hamming.
  - **Burst/Erasure**: Use Reed-Solomon.
  - **Packet Loss**: Use Parity/Check-sums for re-transmission.
- **Resource Check**: ECC decoding (especially RS) is CPU intensive for large files. Run `get-available-resources` first.
- **Always Verify**: After correction, re-run `data-format-detection` to ensure the repaired file is valid.
