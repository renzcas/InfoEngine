from dataclasses import dataclass
from typing import Optional, List

@dataclass
class PacketMeta:
    timestamp: float
    src_ip: str
    dst_ip: str
    protocol: str
    length: int

@dataclass
class TCPFlow:
    src_ip: str
    src_port: int
    dst_ip: str
    dst_port: int
    packets: int
    syn_seen: bool
    syn_ack_seen: bool
    ack_seen: bool

@dataclass
class DNSQuery:
    qname: str
    qtype: str
    src_ip: str
    dst_ip: str

@dataclass
class TLSHandshake:
    src_ip: str
    dst_ip: str
    version: str
    cipher_suites: List[str]

@dataclass
class HTTPExchange:
    src_ip: str
    dst_ip: str
    method: str
    path: str
    status_code: Optional[int]