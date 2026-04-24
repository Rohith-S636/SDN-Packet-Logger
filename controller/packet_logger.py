from pox.core import core
import pox.openflow.libopenflow_01 as of

from pox.lib.packet import ethernet
from pox.lib.packet import ipv4
from pox.lib.packet import arp
from pox.lib.packet import tcp
from pox.lib.packet import udp
from pox.lib.packet import icmp

import os
from datetime import datetime

log = core.getLogger()

# =========================
# 📂 Dynamic Log Path Setup
# =========================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Go to project root → ../../logs
LOG_DIR = os.path.join(BASE_DIR, "../../logs")

# Create logs folder if not exists
os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE = os.path.join(LOG_DIR, "packet_log.txt")


# =========================
# 📝 Logging Function
# =========================

def log_to_file(data):
    try:
        with open(LOG_FILE, "a") as f:
            f.write(data + "\n")
    except Exception as e:
        log.error(f"Error writing to file: {e}")


# =========================
# 🔍 Protocol Detection
# =========================

def identify_protocol(packet):
    if packet.find('arp'):
        return "ARP"
    elif packet.find('icmp'):
        return "ICMP"
    elif packet.find('tcp'):
        return "TCP"
    elif packet.find('udp'):
        return "UDP"
    else:
        return "UNKNOWN"


# =========================
# 📦 Packet Handler
# =========================

def _handle_PacketIn(event):
    packet = event.parsed

    if not packet:
        return

    eth = packet
    src_mac = eth.src
    dst_mac = eth.dst

    protocol = identify_protocol(packet)

    ip_pkt = packet.find('ipv4')

    if ip_pkt:
        src_ip = ip_pkt.srcip
        dst_ip = ip_pkt.dstip
    else:
        src_ip = "N/A"
        dst_ip = "N/A"

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    log_msg = (
        f"[{timestamp}] "
        f"{protocol} | "
        f"MAC: {src_mac} -> {dst_mac} | "
        f"IP: {src_ip} -> {dst_ip}"
    )

    # Print in controller
    log.info(log_msg)

    # Save to file
    log_to_file(log_msg)

    # =========================
    # 🔥 Forward Packet (CRITICAL)
    # =========================
    msg = of.ofp_packet_out()
    msg.data = event.ofp
    msg.actions.append(of.ofp_action_output(port=of.OFPP_FLOOD))
    event.connection.send(msg)


# =========================
# 🚀 Launch Controller
# =========================

def launch():
    log.info("🚀 Packet Logger Started...")
    log.info(f"📁 Logging to file: {os.path.abspath(LOG_FILE)}")

    core.openflow.addListenerByName("PacketIn", _handle_PacketIn)
