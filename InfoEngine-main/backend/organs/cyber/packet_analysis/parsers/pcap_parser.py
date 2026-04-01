# backend/organs/cyber/packet_analysis/parsers/pcap_parser.py

from typing import Dict, Any, List
from datetime import datetime

from scapy.all import rdpcap, IP, TCP, UDP


def _to_iso_utc(ts: float) -> str:
    return datetime.utcfromtimestamp(ts).isoformat() + "Z"


def _flow_key(src_ip: str, dst_ip: str, src_port: int | None,
              dst_port: int | None, protocol: str) -> str:
    return f"{src_ip}:{src_port}->{dst_ip}:{dst_port}/{protocol}"


def parse_pcap_for_episode(episode: Dict[str, Any]) -> Dict[str, Any]:
    """
    Given an episode record (with artifacts.pcap_path),
    parse the PCAP and enrich the episode with:

      - episode['parsed_packets']: list of packet dicts
      - episode['analysis']: flow summary + protocol list
    """
    pcap_path = episode["artifacts"]["pcap_path"]

    scapy_packets = rdpcap(pcap_path)

    parsed_packets: List[Dict[str, Any]] = []
    flows: Dict[str, Dict[str, Any]] = {}
    protocols_seen: set[str] = set()

    for pkt in scapy_packets:
        # Only handle IP for now
        if not pkt.haslayer(IP):
            continue

        ip = pkt[IP]
        src_ip = ip.src
        dst_ip = ip.dst
        src_port: int | None = None
        dst_port: int | None = None
        proto = "ip"
        flags_str: str | None = None

        if pkt.haslayer(TCP):
            tcp = pkt[TCP]
            src_port = int(tcp.sport)
            dst_port = int(tcp.dport)
            proto = "tcp"
            flags_str = tcp.sprintf("%TCP.flags%")
        elif pkt.haslayer(UDP):
            udp = pkt[UDP]
            src_port = int(udp.sport)
            dst_port = int(udp.dport)
            proto = "udp"

        protocols_seen.add(proto)

        length = len(pkt)
        ts = float(pkt.time)
        ts_iso = _to_iso_utc(ts)

        flow_id = _flow_key(src_ip, dst_ip, src_port, dst_port, proto)

        parsed_packet = {
            "timestamp_utc": ts_iso,
            "src_ip": src_ip,
            "dst_ip": dst_ip,
            "src_port": src_port,
            "dst_port": dst_port,
            "protocol": proto,
            "length": length,
            "flags": flags_str,
            "flow_id": flow_id,
        }
        parsed_packets.append(parsed_packet)

        # Initialize or update flow summary
        if flow_id not in flows:
            flows[flow_id] = {
                "flow_id": flow_id,
                "src_ip": src_ip,
                "dst_ip": dst_ip,
                "src_port": src_port,
                "dst_port": dst_port,
                "protocol": proto,
                "packet_count": 0,
                "byte_count": 0,
                "start_time_utc": ts_iso,
                "end_time_utc": ts_iso,
            }

        flow = flows[flow_id]
        flow["packet_count"] += 1
        flow["byte_count"] += length
        flow["end_time_utc"] = ts_iso

    # Attach parsed data to episode
    episode["parsed_packets"] = parsed_packets
    episode["analysis"] = {
        "flow_count": len(flows),
        "protocols_detected": sorted(list(protocols_seen)),
        "summary": f"{len(parsed_packets)} packets across {len(flows)} flows",
        "flows": list(flows.values()),
    }

    return episode