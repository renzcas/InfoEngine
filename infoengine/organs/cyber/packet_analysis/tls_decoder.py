from typing import Iterable, List
from scapy.all import Packet
from .models import TLSHandshake

def extract_tls_handshakes(packets: Iterable[Packet]) -> List[TLSHandshake]:
    # Placeholder: real TLS parsing often uses pyshark or dissect
    return []