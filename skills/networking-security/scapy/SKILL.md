---
name: scapy
description: Use when performing interactive packet manipulation, sniffing, and crafting using Scapy. Ideal for network discovery, protocol research, and low-level network security analysis. CRITICAL: Run `get-available-resources` for high-volume packet capture.
---
# Scapy (Network Research)

Scapy is a powerful Python-based interactive packet manipulation program and library. It can forge or decode packets of a wide number of protocols, send them on the wire, capture them, match requests and replies, and much more.

## ⚠️ Mandatory Pre-flight: Resource Check

Packet sniffing and processing can be CPU and RAM intensive, especially on high-speed interfaces.

1. **Check Resources**: Run `python skills/get-available-resources/scripts/detect_resources.py`.
2. **Buffering Strategy**: For sustained capture (>1 min), use `sniff(..., prn=callback, store=0)` to avoid filling RAM with packet history.

## Core Concepts

- **Layers**: Packets are built by stacking layers using the `/` operator (e.g., `IP()/TCP()`).
- **Sniffing**: Capturing packets from an interface.
- **Crafting**: Creating custom packets from scratch.
- **Sending**: Injecting packets into the network (`send`, `sendp`, `sr`, `srp`).

## Common Operations

### 1. Packet Crafting
```python
from scapy.all import IP, TCP, Ether

# Create a TCP/IP packet
pkt = IP(dst="8.8.8.8") / TCP(dport=443, flags="S")

# Layer 2 (Ethernet)
eth_pkt = Ether() / IP(dst="192.168.1.1") / TCP()
```

### 2. Sniffing
```python
from scapy.all import sniff

# Capture 10 packets
pkts = sniff(count=10, iface="eth0")

# Live processing (no memory storage)
def process_pkt(pkt):
    if pkt.haslayer(IP):
        print(f"Source: {pkt[IP].src}")

sniff(filter="icmp", prn=process_pkt, store=0)
```

### 3. Sending and Receiving
```python
from scapy.all import sr1, send

# Send at Layer 3 and wait for 1 reply
resp = sr1(IP(dst="google.com")/ICMP())

# Send at Layer 2 (requires Ether)
sendp(Ether()/IP(dst="1.2.3.4")/UDP(), iface="eth0")
```

### 4. Network Discovery
```python
from scapy.all import arping

# Simple ARP scan
ans, unans = arping("192.168.1.0/24")
```

## Strict Idioms

- **Check Permissions**: Most Scapy operations require root/Administrator privileges.
- **Specific Filters**: Always use BPF filters (e.g., `filter="tcp and port 80"`) during sniffing to reduce CPU load.
- **Layer Existence**: Always check if a layer exists before accessing it: `if pkt.haslayer(TCP): ...`

## Common Pitfalls (The "Wall of Shame")

1. **The `store=1` Trap**: Calling `sniff()` without `store=0` on a busy network will eventually crash the session due to RAM exhaustion.
2. **Missing `Ether()`**: Sending packets at Layer 2 (`sendp`) without an `Ether` header will fail or cause OS-level errors.
3. **Implicit Layer Access**: Accessing `pkt[TCP]` when the packet is ICMP will raise an `IndexError`. Always guard with `haslayer()`.

## References (Load on demand)
- `references/protocols.md` — Detailed list of supported Scapy layers (HTTP, DNS, TLS, etc.).
- `references/pcap_management.md` — Reading/writing `.pcap` files.
