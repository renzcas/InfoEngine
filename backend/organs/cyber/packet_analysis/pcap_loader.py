from typing import Iterable
from scapy.all import rdpcap, Packet

def load_pcap(path: str) -> Iterable[Packet]:
    return rdpcap(path)