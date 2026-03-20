from typing import Iterable, Dict, Tuple
from scapy.all import Packet, TCP, IP
from .models import TCPFlow

def extract_tcp_flows(packets: Iterable[Packet]) -> Dict[Tuple, TCPFlow]:
    flows: Dict[Tuple, TCPFlow] = {}
    for pkt in packets:
        if not (IP in pkt and TCP in pkt):
            continue
        ip = pkt[IP]
        tcp = pkt[TCP]
        key = (ip.src, tcp.sport, ip.dst, tcp.dport)
        flow = flows.get(key) or TCPFlow(
            src_ip=ip.src,
            src_port=tcp.sport,
            dst_ip=ip.dst,
            dst_port=tcp.dport,
            packets=0,
            syn_seen=False,
            syn_ack_seen=False,
            ack_seen=False,
        )
        flow.packets += 1
        flags = tcp.flags
        if flags & 0x02:  # SYN
            flow.syn_seen = True
        if flags & 0x12 == 0x12:  # SYN+ACK
            flow.syn_ack_seen = True
        if flags & 0x10:  # ACK
            flow.ack_seen = True
        flows[key] = flow
    return flows