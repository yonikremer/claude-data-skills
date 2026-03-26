# Domain-Specific Binary Parsing Patterns

## Sensor / Instrument Data

### Fixed-rate time series (common in DAQ, embedded systems)

```python
import struct
import numpy as np
import pandas as pd

# Many instruments write: header, then dense fixed-width records
HEADER_FMT = '<4sHHdI'  # magic(4), major(2), minor(2), start_epoch(8), n_samples(4)
RECORD_FMT = '<HHf'     # channel(2), flags(2), value(4)

def read_daq_file(path: str) -> pd.DataFrame:
    with open(path, 'rb') as f:
        hdr_size = struct.calcsize(HEADER_FMT)
        magic, major, minor, start_epoch, n_samples = struct.unpack(
            HEADER_FMT, f.read(hdr_size)
        )

        dtype = np.dtype([
            ('channel', '<u2'),
            ('flags',   '<u2'),
            ('value',   '<f4'),
        ])
        arr = np.frombuffer(f.read(), dtype=dtype)

    df = pd.DataFrame(arr)
    # Reconstruct timestamps if samples are evenly spaced
    sample_rate = 1000  # Hz — get from header if present
    df['timestamp'] = start_epoch + np.arange(len(df)) / sample_rate
    return df
```

### Chunked / tagged format (TLV — Type-Length-Value)

Common in instrumentation, network protocols, custom storage formats.

```python
import struct
from dataclasses import dataclass
from typing import Iterator

@dataclass
class Chunk:
    type_id: int
    data: bytes

def parse_tlv(data: bytes, type_size=2, length_size=2) -> Iterator[Chunk]:
    """Generic TLV parser. Adjust type_size/length_size to match your format."""
    type_fmt  = {1: 'B', 2: '<H', 4: '<I'}[type_size]
    len_fmt   = {1: 'B', 2: '<H', 4: '<I'}[length_size]
    hdr_size  = type_size + length_size
    offset    = 0
    while offset + hdr_size <= len(data):
        type_id = struct.unpack_from(type_fmt, data, offset)[0]
        length  = struct.unpack_from(len_fmt,  data, offset + type_size)[0]
        offset += hdr_size
        yield Chunk(type_id=type_id, data=data[offset:offset + length])
        offset += length
```

## Network Protocols / Packet Data

### Parse pcap-style frames

```python
import struct
from datetime import datetime, timezone

# pcap global header
PCAP_GLOBAL_HDR = '<IHHiIII'  # magic, major, minor, thiszone, sigfigs, snaplen, network

# pcap packet record header
PCAP_PKT_HDR = '<IIII'  # ts_sec, ts_usec, incl_len, orig_len

def read_pcap(path: str):
    with open(path, 'rb') as f:
        gbl_size = struct.calcsize(PCAP_GLOBAL_HDR)
        magic, major, minor, tz, sigfigs, snaplen, network = struct.unpack(
            PCAP_GLOBAL_HDR, f.read(gbl_size)
        )
        assert magic == 0xA1B2C3D4, "Not a valid pcap file"

        pkt_hdr_size = struct.calcsize(PCAP_PKT_HDR)
        packets = []
        while True:
            raw_hdr = f.read(pkt_hdr_size)
            if len(raw_hdr) < pkt_hdr_size:
                break
            ts_sec, ts_usec, incl_len, orig_len = struct.unpack(PCAP_PKT_HDR, raw_hdr)
            payload = f.read(incl_len)
            ts = datetime.fromtimestamp(ts_sec + ts_usec / 1e6, tz=timezone.utc)
            packets.append({'timestamp': ts, 'payload': payload, 'orig_len': orig_len})

    return packets
```

## Legacy Formats (Python 2 / old code)

### Python 2 pickle files

```python
import pickle

# Python 2 pickles can be read in Python 3 with encoding='latin1' for byte strings
# or encoding='bytes' to get raw bytes objects
with open('legacy.pkl', 'rb') as f:
    data = pickle.load(f, encoding='latin1')   # str → str
    # or
    data = pickle.load(f, encoding='bytes')    # str → bytes
```

### NumPy .npy / .npz (old or cross-version)

```python
import numpy as np

# Safe loading of .npy from old numpy versions
arr = np.load('old_data.npy', allow_pickle=False)  # set True only if needed

# .npz (zipped archive of arrays)
npz = np.load('data.npz')
print(list(npz.files))   # list array names
arr = npz['my_array']
```

### MATLAB .mat files (v7.3 = HDF5, older = legacy)

```python
# For MATLAB < 7.3 files
import scipy.io
mat = scipy.io.loadmat('data.mat')

# For MATLAB v7.3 (HDF5-based)
import h5py
with h5py.File('data_v73.mat', 'r') as f:
    arr = f['variable_name'][()]
```

## Unknown / Reverse-Engineering a Binary Format

Systematic approach when you don't have a spec:

```python
import struct
from collections import Counter

def analyze_binary(path: str, record_size_hint: int = None):
    with open(path, 'rb') as f:
        data = f.read()

    print(f"File size: {len(data)} bytes")

    # 1. Look for magic bytes / ASCII at start
    print(f"First 32 bytes (hex): {data[:32].hex()}")
    print(f"First 32 bytes (ascii): {data[:32]}")

    # 2. Try common record sizes
    if record_size_hint:
        remainder = len(data) % record_size_hint
        print(f"With record_size={record_size_hint}: remainder={remainder} bytes")

    # 3. Check for repeating patterns
    for size in [4, 8, 12, 16, 20, 24, 32]:
        if len(data) % size == 0:
            print(f"  Evenly divisible by {size} ({len(data)//size} records)")

    # 4. Entropy / byte frequency
    freq = Counter(data)
    print(f"Unique byte values: {len(freq)}/256")
    print(f"Most common bytes: {freq.most_common(5)}")

    # 5. Try interpreting as floats at different offsets
    print("\nFirst values interpreted as float32 (little-endian):")
    for i in range(0, min(32, len(data) - 3), 4):
        val = struct.unpack_from('<f', data, i)[0]
        if not (val != val) and abs(val) < 1e10:  # skip NaN and huge values
            print(f"  offset {i}: {val:.4f}")
```

## Reading Binary Data into pandas

```python
import numpy as np
import pandas as pd

# Method 1: structured dtype → DataFrame directly
dtype = np.dtype([
    ('timestamp', '>u4'),
    ('channel',   '>u2'),
    ('value',     '>f4'),
    ('status',    '>u2'),
])

with open('data.bin', 'rb') as f:
    f.seek(header_size)
    df = pd.DataFrame(np.frombuffer(f.read(), dtype=dtype))

# Method 2: parse records with struct, collect into list of dicts
import struct

records = []
rec_fmt = '>IHfH'
rec_size = struct.calcsize(rec_fmt)

with open('data.bin', 'rb') as f:
    f.seek(header_size)
    while True:
        raw = f.read(rec_size)
        if len(raw) < rec_size:
            break
        ts, ch, val, status = struct.unpack(rec_fmt, raw)
        records.append({'timestamp': ts, 'channel': ch, 'value': val, 'status': status})

df = pd.DataFrame(records)
```
