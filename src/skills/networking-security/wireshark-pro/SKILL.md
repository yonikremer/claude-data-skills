---
name: wireshark-pro
description: Use when analyzing network traffic, handling PCAP files larger than 1GB, extracting packet data programmatically, or needing to split/merge captures.
---

# Wireshark Pro

## Overview

Mastery of network packet analysis using Wireshark CLI tools (`tshark`, `editcap`, `capinfos`, `mergecap`) and Python
libraries (`pyshark`, `scapy`). This skill shifts analysis from the memory-heavy UI to scalable, scriptable command-line
workflows.

## When to Use

- PCAP files are too large to open in the UI (frequent crashes).
- You need to extract specific fields (IPs, ports, headers) into a CSV/tabular format.
- You need to programmatically analyze custom protocols.
- You need to split, merge, or deduplicate capture files.

## Red Flags - STOP and Re-evaluate

- **"I'll just open this 5GB PCAP in Wireshark."** (It will OOM and crash. Split it or filter it via CLI first.)
- **"I'll read all packets into a Python list."** (Both PyShark and Scapy will exhaust memory. Use generators and
  streaming.)
- **"I'll iterate packets in Python to filter for IP 1.2.3.4."** (Push filtering down to `tshark` or PyShark's
  `display_filter` parameter; it's 100x faster.)

## Common Rationalizations

| Excuse                            | Reality                                                                             |
|-----------------------------------|-------------------------------------------------------------------------------------|
| "Opening the UI is easier"        | `capinfos` gives file stats instantly. `tshark` filters take seconds vs UI minutes. |
| "I'll use PyShark for everything" | PyShark is slow (~5k pkt/s). Use Scapy or `dpkt` if you only need basic IPs/Ports.  |
| "I'll use Scapy's `rdpcap()`"     | `rdpcap()` loads the entire file into RAM. Use `PcapReader` to stream.              |
| "Filtering in Python is fine"     | Python loops are slow. Pass `display_filter` or BPF filters directly to the engine. |

## Quick Reference: CLI Tools

| Tool       | Purpose                         | Essential Command                                 |
|------------|---------------------------------|---------------------------------------------------|
| `tshark`   | Deep analysis, capture, filter  | `tshark -r in.pcap -Y "http" -T fields -e ip.src` |
| `capinfos` | Instant stats (count, duration) | `capinfos -c -d in.pcap`                          |
| `editcap`  | Split, truncate, deduplicate    | `editcap -c 100000 large.pcap chunk.pcap`         |
| `mergecap` | Combine files by timestamp      | `mergecap -w merged.pcap f1.pcap f2.pcap`         |

## Core Patterns

### 1. The Large File Triage

Never open a massive PCAP blindly. Triage it via CLI.

```bash
# 1. Get stats (packet count, duration, file type)
capinfos in.pcapng

# 2. Extract only what you need (e.g., specific IP)
tshark -r in.pcapng -Y "ip.addr == 10.0.0.1" -w target_ip.pcapng

# 3. Alternatively, split into 100k packet chunks
editcap -c 100000 in.pcapng split.pcapng
```

### 2. Fast CSV/JSON Extraction

Instead of parsing in Python, use `tshark` to output exactly what you need.

```bash
# CSV Extraction: Source/Dest IP and TCP Port
tshark -r in.pcap -T fields -e ip.src -e ip.dst -e tcp.dstport -E separator=, > data.csv

# JSON Extraction (Detailed Dissection)
tshark -r in.pcap -T json -e frame.time -e ip.src -e http.request.method > data.json
```

### 3. PyShark: Complex Analytics & Reassembly

Use when you need to reconstruct streams or extract objects (files, images).

```python
import pyshark

# REQUIRED: keep_packets=False prevents catastrophic memory leaks
# REQUIRED: display_filter for stream reassembly
cap = pyshark.FileCapture('traffic.pcap', display_filter='tcp.stream eq 0', keep_packets=False)

full_payload = b""
for pkt in cap:
    try:
        # Access binary payload directly
        full_payload += pkt.tcp.payload.binary_value
    except AttributeError:
        pass  # Skip ACKs/Empty packets

# Object Extraction (HTTP Example)
if hasattr(pkt.http, 'file_data'):
    with open('extracted_file.bin', 'wb') as f:
        f.write(pkt.http.file_data.binary_value)
```

### 4. Extensions & Custom Dissectors (Lua)

Use Lua for custom protocols. It is loaded at runtime and doesn't require compilation.

- **Placement:** Save as `.lua` in `C:\Users\<user>\AppData\Roaming\Wireshark\plugins` (Windows).
- **Reloading:** Press `Ctrl+Shift+L` in Wireshark to reload without restarting.

```lua
-- Simple Lua Dissector Template
local my_proto = Proto("MyProto", "My Custom Protocol")
local f_field = ProtoField.uint16("myproto.field", "Some Field", base.HEX)
my_proto.fields = { f_field }

function my_proto.dissector(buffer, pinfo, tree)
    pinfo.cols.protocol = my_proto.name
    local subtree = tree:add(my_proto, buffer(), "My Proto Data")
    subtree:add(f_field, buffer(0,2))
end

local tcp_table = DissectorTable.get("tcp.port")
tcp_table:add(1234, my_proto)
```

## Common Field Guide (`-e` arguments)

| Field Name             | Description         | Example Value |
|------------------------|---------------------|---------------|
| `frame.number`         | Packet index        | `1024`        |
| `frame.time_relative`  | Seconds since start | `12.45`       |
| `ip.src` / `ip.dst`    | Source/Dest IP      | `192.168.1.5` |
| `tcp.stream`           | Wireshark Stream ID | `0`           |
| `tcp.analysis.ack_rtt` | Calculated Latency  | `0.0045`      |
| `http.host`            | Host header         | `google.com`  |
| `dns.qry.name`         | DNS Query           | `example.com` |

## Common Mistakes

1. **Zombie `tshark` processes:** PyShark spawns `tshark` instances. If you don't call `.close()` or your script
   crashes, you will leave orphaned `tshark` processes consuming RAM. Always use `try/finally` or context managers.
2. **Missing `keep_packets=False`:** PyShark defaults to saving every parsed packet in a list. This guarantees an
   Out-Of-Memory (OOM) error on large files.
3. **Using `rdpcap()` in Scapy:** Scapy's standard read function loads everything into RAM. Switch to `PcapReader` for
   99% of use cases.
4. **Ignoring `tshark -G fields`:** Use this to find the *exact* field name you need for extraction.
   `tshark -G fields | findstr "keyword"` is faster than guessing.