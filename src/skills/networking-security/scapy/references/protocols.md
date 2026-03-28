# Scapy Supported Protocols Reference

Scapy supports over 300 protocols. Here are the most common ones:

## 1. Network Layer (Layer 3)
- **IP**: `IP(src="192.168.1.1", dst="8.8.8.8")`
- **IPv6**: `IPv6(dst="2001:4860:4860::8888")`
- **ARP**: `ARP(op=1, pdst="192.168.1.1")` (op=1 for request, op=2 for reply)
- **ICMP**: `ICMP(type=8)` (type=8 for echo-request, type=0 for echo-reply)

## 2. Transport Layer (Layer 4)
- **TCP**: `TCP(sport=1234, dport=80, flags="S")` (flags: S=SYN, A=ACK, F=FIN, R=RST, P=PSH)
- **UDP**: `UDP(sport=1234, dport=53)`
- **SCTP**: `SCTP(sport=1234, dport=80)`

## 3. Application Layer (Layer 7)
- **DNS**: `DNS(rd=1, qd=DNSQR(qname="google.com"))`
- **HTTP**: `HTTP() / HTTPRequest(Method="GET", Path="/")`
- **TLS**: `TLS(type=22)` (type=22 for Handshake)
- **DHCP**: `DHCP(options=[("message-type", "discover"), "end"])`
- **BOOTP**: `BOOTP(chaddr="00:11:22:33:44:55")`

## 4. Link Layer (Layer 2)
- **Ethernet**: `Ether(src="00:11:22:33:44:55", dst="ff:ff:ff:ff:ff:ff")`
- **Dot1Q**: `Dot1Q(vlan=10)`
- **802.11**: `Dot11(addr1="...", addr2="...", addr3="...")`
