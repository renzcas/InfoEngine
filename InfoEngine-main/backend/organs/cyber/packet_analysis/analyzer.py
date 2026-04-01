# backend/organs/cyber/packet_analysis/analyzer.py

from typing import Dict, Any, List
import uuid
from datetime import datetime


def _event_id() -> str:
    return str(uuid.uuid4())


def analyze_episode_to_events(episode: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Takes an enriched episode (with parsed_packets + analysis.flows)
    and returns a list of cockpit-ready events.
    """
    events: List[Dict[str, Any]] = []
    episode_id = episode["episode_id"]
    analysis = episode.get("analysis", {})
    flows = analysis.get("flows", [])
    parsed_packets = episode.get("parsed_packets", [])

    # --- Episode summary event ---
    episode_summary_event = {
        "event_id": _event_id(),
        "event_type": "episode_summary",
        "timestamp_utc": episode["metadata"]["created_at_utc"],
        "episode_id": episode_id,
        "payload": {
            "episode_id": episode_id,
            "scenario": episode["scenario"],
            "flow_count": analysis.get("flow_count", len(flows)),
            "packet_count": len(parsed_packets),
            "protocols_detected": analysis.get("protocols_detected", []),
            "created_at_utc": episode["metadata"]["created_at_utc"],
        },
    }
    events.append(episode_summary_event)

    # --- Flow summary events ---
    for flow in flows:
        events.append({
            "event_id": _event_id(),
            "event_type": "flow_summary",
            "timestamp_utc": flow["start_time_utc"],
            "episode_id": episode_id,
            "payload": flow,
        })

    # --- Packet events (timeline / stream) ---
    for idx, pkt in enumerate(parsed_packets):
        payload = dict(pkt)
        payload["packet_id"] = idx

        events.append({
            "event_id": _event_id(),
            "event_type": "packet",
            "timestamp_utc": pkt["timestamp_utc"],
            "episode_id": episode_id,
            "payload": payload,
        })

    # --- (Optional) simple alerts example ---
    # e.g., alert if any flow has > N packets
    for flow in flows:
        if flow["packet_count"] > 50:
            events.append({
                "event_id": _event_id(),
                "event_type": "alert",
                "timestamp_utc": flow["end_time_utc"],
                "episode_id": episode_id,
                "payload": {
                    "severity": "low",
                    "category": "flow",
                    "message": f"High packet count in flow {flow['flow_id']}",
                    "flow_id": flow["flow_id"],
                    "packet_index": None,
                },
            })

    # Sort events by time for clean timelines
    events.sort(key=lambda e: e["timestamp_utc"])

    return events