# backend/organs/cyber/traffic_generator/scapy_engine.py

from typing import Dict
from datetime import datetime
from pathlib import Path

from scapy.all import IP, TCP, Raw, wrpcap, RandInt


def generate_http_get_scenario(
    src_ip: str,
    dst_ip: str,
    src_port: int,
    dst_port: int = 80,
    host: str = "example.com",
    path: str = "/",
    output_dir: str = "data/pcap",
    episode_id: str | None = None,
) -> Dict:
    """
    Generate a synthetic HTTP GET flow:
      - TCP 3-way handshake
      - HTTP GET request
      - HTTP 200 OK response
      - TCP FIN/ACK teardown (simple)

    Saves to a PCAP file and returns an episode/lineage record.
    """

    # --- Episode / lineage basics ---
    if episode_id is None:
        ts = datetime.utcnow().strftime("%Y%m%dT%H%M%S")
        episode_id = f"http_get_{ts}"

    output_dir_path = Path(output_dir)
    output_dir_path.mkdir(parents=True, exist_ok=True)

    pcap_path = output_dir_path / f"{episode_id}.pcap"

    # --- Common layers ---
    ip_c2s = IP(src=src_ip, dst=dst_ip)   # client → server
    ip_s2c = IP(src=dst_ip, dst=src_ip)   # server → client

    client_isn = RandInt()
    server_isn = RandInt()

    # --- TCP 3-way handshake ---
    syn = ip_c2s / TCP(
        sport=src_port,
        dport=dst_port,
        flags="S",
        seq=client_isn,
    )

    syn_ack = ip_s2c / TCP(
        sport=dst_port,
        dport=src_port,
        flags="SA",
        seq=server_isn,
        ack=client_isn + 1,
    )

    ack = ip_c2s / TCP(
        sport=src_port,
        dport=dst_port,
        flags="A",
        seq=client_isn + 1,
        ack=server_isn + 1,
    )

    # --- HTTP GET request ---
    http_get_payload = (
        f"GET {path} HTTP/1.1\r\n"
        f"Host: {host}\r\n"
        "User-Agent: InfoEngine-Scapy\r\n"
        "Accept: */*\r\n"
        "\r\n"
    ).encode()

    http_get = ip_c2s / TCP(
        sport=src_port,
        dport=dst_port,
        flags="PA",  # PSH+ACK
        seq=client_isn + 1,
        ack=server_isn + 1,
    ) / Raw(load=http_get_payload)

    # --- HTTP 200 OK response ---
    http_body = b"<html><body><h1>Hello from InfoEngine</h1></body></html>"
    http_response_payload = (
        b"HTTP/1.1 200 OK\r\n"
        b"Content-Type: text/html\r\n"
        b"Content-Length: " + str(len(http_body)).encode() + b"\r\n"
        b"\r\n" +
        http_body
    )

    server_seq_after_synack = server_isn + 1
    server_seq_after_response = server_seq_after_synack + len(http_response_payload)

    http_200 = ip_s2c / TCP(
        sport=dst_port,
        dport=src_port,
        flags="PA",  # PSH+ACK
        seq=server_seq_after_synack,
        ack=client_isn + 1 + len(http_get_payload),
    ) / Raw(load=http_response_payload)

    # --- Simple TCP teardown (FIN/ACK) ---
    fin_c2s = ip_c2s / TCP(
        sport=src_port,
        dport=dst_port,
        flags="FA",
        seq=client_isn + 1 + len(http_get_payload),
        ack=server_seq_after_response,
    )

    fin_ack_s2c = ip_s2c / TCP(
        sport=dst_port,
        dport=src_port,
        flags="FA",
        seq=server_seq_after_response,
        ack=client_isn + 2 + len(http_get_payload),
    )

    last_ack_c2s = ip_c2s / TCP(
        sport=src_port,
        dport=dst_port,
        flags="A",
        seq=client_isn + 2 + len(http_get_payload),
        ack=server_seq_after_response + 1,
    )

    packets = [
        syn,
        syn_ack,
        ack,
        http_get,
        http_200,
        fin_c2s,
        fin_ack_s2c,
        last_ack_c2s,
    ]

    # --- Write PCAP ---
    wrpcap(str(pcap_path), packets)

    # --- Episode / lineage record ---
    episode_record: Dict = {
        "episode_id": episode_id,
        "scenario": "http_get_basic",
        "pcap_path": str(pcap_path),
        "params": {
            "src_ip": src_ip,
            "dst_ip": dst_ip,
            "src_port": src_port,
            "dst_port": dst_port,
            "host": host,
            "path": path,
        },
        "packet_count": len(packets),
        "created_at_utc": datetime.utcnow().isoformat() + "Z",
        "version": "v0.1.0",
    }

    return episode_record