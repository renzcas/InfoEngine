from typing import Iterable, List
from scapy.all import Packet, DNS, DNSQR, IP
from .models import DNSQuery

def extract_dns_queries(packets: Iterable[Packet]) -> List[DNSQuery]:
    queries: List[DNSQuery] = []
    for pkt in packets:
        if not (IP in pkt and DNS in pkt and DNSQR in pkt):
            continue
        ip = pkt[IP]
        dns = pkt[DNS]
        q = dns[DNSQR]
        queries.append(
            DNSQuery(
                qname=q.qname.decode(errors="ignore"),
                qtype=str(q.qtype),
                src_ip=ip.src,
                dst_ip=ip.dst,
            )
        )
    return queries