from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.packet import ethernet, ipv4, arp, tcp, udp, icmp
from datetime import datetime

log = core.getLogger()

LOG_FILE = "/home/rohith/pox/logs/packet_log.txt"

def log_to_file(data):
    with open(LOG_FILE, "a") as f:
        f.write(data + "\n")

def identify_protocol(packet):
    if packet.find('arp'):
        return "ARP"
    if packet.find('icmp'):
        return "ICMP"
    if packet.find('tcp'):
        return "TCP"
    if packet.find('udp'):
        return "UDP"
    return "UNKNOWN"

def _handle_PacketIn(event):
    packet = event.parsed

    if not packet:
        return

    eth = packet
    src = eth.src
    dst = eth.dst

    protocol = identify_protocol(packet)

    ip_pkt = packet.find('ipv4')
    src_ip = ip_pkt.srcip if ip_pkt else "N/A"
    dst_ip = ip_pkt.dstip if ip_pkt else "N/A"

    timestamp = datetime.now().strftime("%H:%M:%S")

    log_msg = f"[{timestamp}] {protocol} | {src} -> {dst} | {src_ip} -> {dst_ip}"

    log.info(log_msg)
    log_to_file(log_msg)

def launch():
    log.info("Packet Logger Started...")
    core.openflow.addListenerByName("PacketIn", _handle_PacketIn)
