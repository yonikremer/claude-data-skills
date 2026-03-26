# Scapy PCAP Management Reference

## 1. Reading PCAP files
```python
from scapy.all import rdpcap

# Read all packets into memory
pkts = rdpcap("traffic.pcap")

# Read first 100 packets
pkts = rdpcap("traffic.pcap", count=100)
```

## 2. Writing PCAP files
```python
from scapy.all import wrpcap

# Write list of packets to file
wrpcap("output.pcap", pkts)

# Append to existing file
wrpcap("output.pcap", pkts, append=True)
```

## 3. Streaming (Large files)
```python
from scapy.all import PcapReader, PcapWriter

# Process one packet at a time (Memory Efficient)
with PcapReader("large_file.pcap") as pr:
    for pkt in pr:
        if pkt.haslayer(IP):
            print(f"IP: {pkt[IP].src}")

# Write one packet at a time
with PcapWriter("output.pcap", append=True, sync=True) as pw:
    for pkt in pkts:
        pw.write(pkt)
```

## 4. Filtering with Tcpdump syntax
```python
from scapy.all import sniff

# Sniff and save to file immediately
sniff(filter="tcp and port 80", prn=lambda x: wrpcap("http.pcap", x, append=True))
```
