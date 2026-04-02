from scapy.all import IP, TCP, send

def send_syn(dst_ip: str, dst_port: int):
    pkt = IP(dst=dst_ip)/TCP(dport=dst_port, flags="S")
    send(pkt, verbose=False)