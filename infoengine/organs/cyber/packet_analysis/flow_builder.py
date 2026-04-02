from typing import Dict, Tuple, List
from scapy.all import Packet
from .models import TCPFlow, DNSQuery, TLSHandshake, HTTPExchange
from .tcp_decoder import extract_tcp_flows
from .dns_decoder import extract_dns_queries
from .tls_decoder import extract_tls_handshakes
from .http_decoder import extract_http_exchanges

class FlowView:
    def __init__(
        self,
        tcp_flows: Dict[Tuple, TCPFlow],
        dns_queries: List[DNSQuery],
        tls_handshakes: List[TLSHandshake],
        http_exchanges: List[HTTPExchange],
    ):
        self.tcp_flows = tcp_flows
        self.dns_queries = dns_queries
        self.tls_handshakes = tls_handshakes
        self.http_exchanges = http_exchanges

def build_flow_view(packets: List[Packet], pcap_path: str) -> FlowView:
    tcp_flows = extract_tcp_flows(packets)
    dns_queries = extract_dns_queries(packets)
    tls_handshakes = extract_tls_handshakes(packets)
    http_exchanges = extract_http_exchanges(pcap_path)
    return FlowView(tcp_flows, dns_queries, tls_handshakes, http_exchanges)