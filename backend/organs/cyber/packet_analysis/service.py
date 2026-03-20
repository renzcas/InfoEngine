from typing import Dict, Tuple
from scapy.all import Packet
from .pcap_loader import load_pcap
from .flow_builder import build_flow_view
from .models import TCPFlow, DNSQuery, TLSHandshake, HTTPExchange

class PacketAnalysisService:
    def analyze_pcap(self, path: str):
        packets = list(load_pcap(path))
        view = build_flow_view(packets, path)
        return {
            "tcp_flows": list(view.tcp_flows.values()),
            "dns_queries": view.dns_queries,
            "tls_handshakes": view.tls_handshakes,
            "http_exchanges": view.http_exchanges,
        }