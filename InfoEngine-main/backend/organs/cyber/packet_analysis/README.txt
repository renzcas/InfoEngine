"""///⭐ The InfoEngine Episode + Lineage Schema (v1)////
Below is the canonical schema that every synthetic scenario will produce.
It’s compact, expressive, and lineage‑aware.
YAMLcanonical schema that every synthetic scenario will produce.
It’s compact, expressive, and lineage‑aware
/////////////////////////////////////////////////////"""
episode_id: string
scenario: string
version: string

metadata:
  created_at_utc: string
  generator: string
  seed: int | null

inputs:
  src_ip: string
  dst_ip: string
  src_port: int
  dst_port: int
  protocol: string
  scenario_params:
    # scenario-specific fields (HTTP path, DNS name, TLS ciphers, etc.)

artifacts:
  pcap_path: string
  packet_count: int

lineage:
  parent_episode: string | null
  derived_from:
    - episode_id: string
      transformation: string
  tags:
    - string

analysis:
  # Filled later by the packet-analysis organ
  flow_count: int | null
  protocols_detected: [string] | null
  summary: string | null

  //////////////////////////////



  episode_id: "http_get_20260330T231700"
scenario: "http_get_basic"
version: "v0.1.0"

metadata:
  created_at_utc: "2026-03-30T23:17:00Z"
  generator: "scapy_traffic_generator"
  seed: null

inputs:
  src_ip: "10.0.0.1"
  dst_ip: "10.0.0.2"
  src_port: 40000
  dst_port: 80
  protocol: "tcp"
  scenario_params:
    host: "example.com"
    path: "/index.html"

artifacts:
  pcap_path: "data/pcap/http_get_20260330T231700.pcap"
  packet_count: 8

lineage:
  parent_episode: null
  derived_from: []
  tags: ["synthetic", "http", "scapy"]

analysis:
  flow_count: null
  protocols_detected: null
  summary: null