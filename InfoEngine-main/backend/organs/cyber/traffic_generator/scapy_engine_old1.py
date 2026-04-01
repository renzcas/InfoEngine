# backend/organs/cyber/traffic_generator/scapy_engine.py

from typing import Dict
from datetime import datetime
from pathlib import Path

from scapy.all import IP, TCP, wrpcap, RandInt


def generate_tcp_handshake_scenario(
    src_ip: str,
    dst_ip: str,
    src_port: int,
    dst_port: int,
    output_dir: str = "data/pcap",
    episode_id: str | None = None,
) -> Dict:
    """
    Generate a synthetic TCP 3-way handshake and save to a PCAP file.

    Returns a lineage/episode record describing what was generated.
    """

    # --- Episode / lineage basics ---
    if episode_id is None:
        ts = datetime.utcnow().strftime("%Y%m%dT%H%M%S")
        episode_id = f"tcp_handshake_{ts}"

    output_dir_path = Path(output_dir)
    output_dir_path.mkdir(parents=True, exist_ok=True)

    pcap_path = output_dir_path / f"{episode_id}.pcap"

    # --- Build packets with Scapy ---
    ip = IP(src=src_ip, dst=dst_ip)

    # Random initial sequence numbers for realism
    client_isn = RandInt()
    server_isn = RandInt()

    syn = ip / TCP(
        sport=src_port,
        dport=dst_port,
        flags="S",
        seq=client_isn,
    )

    syn_ack = ip / TCP(
        sport=dst_port,
        dport=src_port,
        flags="SA",
        seq=server_isn,
        ack=client_isn + 1,
    )

    ack = ip / TCP(
        sport=src_port,
        dport=dst_port,
        flags="A",
        seq=client_isn + 1,
        ack=server_isn + 1,
    )

    packets = [syn, syn_ack, ack]

    # --- Write PCAP ---
    wrpcap(str(pcap_path), packets)

    # --- Build lineage / episode record ---
    episode_record: Dict = {
        "episode_id": episode_id,
        "scenario": "tcp_handshake_basic",
        "pcap_path": str(pcap_path),
        "params": {
            "src_ip": src_ip,
            "dst_ip": dst_ip,
            "src_port": src_port,
            "dst_port": dst_port,
        },
        "packet_count": len(packets),
        "created_at_utc": datetime.utcnow().isoformat() + "Z",
        "version": "v0.1.0",
    }

    return episode_record