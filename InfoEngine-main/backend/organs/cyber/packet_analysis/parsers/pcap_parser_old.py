# backend/organs/cyber/packet_analysis/parsers/pcap_parser.py

from typing import Dict, Any, List


def parse_pcap_for_episode(episode: Dict[str, Any]) -> Dict[str, Any]:
    """
    Given an episode record (with artifacts.pcap_path),
    parse the PCAP and return an enriched episode:

      - add parsed_packets (optional, or stored elsewhere)
      - add basic flow summary into episode['analysis']
    """
    pcap_path = episode["artifacts"]["pcap_path"]

    # 1) open PCAP
    # 2) iterate packets
    # 3) extract (timestamp, src_ip, dst_ip, src_port, dst_port, protocol, length, flags)
    # 4) group into flows (5-tuple)
    # 5) compute summary

    parsed_packets: List[Dict[str, Any]] = []
    flows: Dict[str, Dict[str, Any]] = {}

    # ... parsing logic goes here ...

    # Example of how you might update analysis:
    episode["analysis"] = {
        "flow_count": len(flows),
        "protocols_detected": ["tcp", "http"],
        "summary": f"{len(parsed_packets)} packets across {len(flows)} flows",
    }

    # Option A: attach parsed_packets directly (for small episodes)
    episode["parsed_packets"] = parsed_packets

    # Option B (later): store parsed_packets in a separate store and only keep references

    return episode