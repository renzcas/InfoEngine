///parsed tpackket schemaper packet//////
timestamp_utc: string
src_ip: string
dst_ip: string
src_port: int | null
dst_port: int | null
protocol: string        # "tcp", "udp", "ip", etc.
length: int
flags: string | null    # e.g. "S", "SA", "PA"
flow_id: string         # stable ID for 5-tuple

//////////flow schema
flow_id: string
src_ip: string
dst_ip: string
src_port: int
dst_port: int
protocol: string
packet_count: int
byte_count: int
start_time_utc: string
end_time_utc: string
roles:            # optional
  client_ip: string
  server_ip: string

  /////////2. Example: full loop from generator → parse

  # somewhere in a test harness or organ orchestrator

from organs.cyber.traffic_generator.scapy_engine import generate_http_get_scenario
from organs.cyber.packet_analysis.parsers.pcap_parser import parse_pcap_for_episode

episode = generate_http_get_scenario(
    src_ip="10.0.0.1",
    dst_ip="10.0.0.2",
    src_port=40000,
    dst_port=80,
    host="example.com",
    path="/index.html",
)

episode_enriched = parse_pcap_for_episode(episode)

print(episode_enriched["analysis"]["summary"])
print(episode_enriched["analysis"]["flows"])

////////////////////////////

event_type: "packet"
payload:
  packet_id: int
  timestamp_utc: string
  src_ip: string
  dst_ip: string
  src_port: int | null
  dst_port: int | null
  protocol: string
  length: int
  flags: string | null
  flow_id: string


  event_type: "flow_summary"
payload:
  flow_id: string
  src_ip: string
  dst_ip: string
  src_port: int
  dst_port: int
  protocol: string
  packet_count: int
  byte_count: int
  start_time_utc: string
  end_time_utc: string



  event_type: "episode_summary"
payload:
  episode_id: string
  scenario: string
  flow_count: int
  packet_count: int
  protocols_detected: [string]
  created_at_utc: string

 ///Alert event (op
  event_type: "alert"
payload:
  severity: string          # "info", "low", "medium", "high"
  category: string          # "http", "dns", "tcp", "tls", "meta"
  message: string
  flow_id: string | null
  packet_index: int | null


///6. Where this lives in the organ
//Your packet‑analysis organ can expose something like:

  def analyze_episode_to_events(episode: dict) -> list[dict]:
    """
    Takes an enriched episode (with parsed_packets + flows)
    and returns a list of cockpit-ready events.
    """