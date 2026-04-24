# 🚀 SDN Packet Logger — Run & Demo Guide (POX + Mininet)

This guide explains **step-by-step** how to run the SDN Packet Logger project using the POX controller and Mininet.

---

# 📌 Prerequisites

- Ubuntu (VM or native)
- Python3
- Internet connection

---

# 🧭 TERMINAL LEGEND

| Terminal | Purpose |
|----------|--------|
| Terminal 1 | POX Controller |
| Terminal 2 | Mininet |
| Terminal 3 | Log File View (optional) |

---

# 📥 STEP 1: Clone Project

### 🟢 Terminal 1

```bash
git clone https://github.com/Rohith-S636/SDN-Packet-Logger.git
cd SDN-Packet-Logger
```
# 📦 STEP 2: Install Dependencies

## 🟢 Terminal 1
```bash
sudo apt update
sudo apt install mininet git python3 -y
```
# 📥 STEP 3: Clone POX Controller

## 🟢 Terminal 1
```bash
git clone https://github.com/noxrepo/pox.git
```
# 📂 STEP 4: Place Controller File Correctly

## 🟢 Terminal 1
```bash
# Create required directory inside POX
mkdir -p pox/pox/ext

# Copy your controller file
cp controller/packet_logger.py pox/pox/ext/

# Create init file (IMPORTANT)
touch pox/pox/ext/__init__.py
```
# ✅ VERIFY FILE PLACEMENT

## 🟢 Terminal 1
```bash
ls pox/pox/ext
```
Expected output:
```bash
packet_logger.py  __init__.py
```
# ▶️ STEP 5: Start POX Controller

## 🟢 Terminal 1
```bash
cd pox
./pox.py log.level --DEBUG openflow.of_01 ext.packet_logger
```
📸 Screenshot 1:
```bash
"Packet Logger Started"
"Listening on 6633"
```
# 🌐 STEP 6: Start Mininet

## 🟡 Terminal 2 (NEW TERMINAL)
```bash
cd ~/SDN-Packet-Logger
sudo mn -c
sudo mn --custom topology.py --topo mytopo --controller=remote
```

📸 Screenshot 2: Mininet topology created

# 🧪 STEP 7: Test Connectivity

## 🟡 Terminal 2
```bash
pingall
```

Expected:
```bash
0% dropped
```

📸 Screenshot 3 (IMPORTANT)

# 🔁 STEP 8: Generate Traffic

## 🟡 Terminal 2
```bash
h1 ping h2
```
📸 Screenshot 4: Ping running

# 🖥️ STEP 9: View Controller Logs

## 🟢 Terminal 1
```bash
You will see:

ICMP | MAC: ... | IP: 10.0.0.1 -> 10.0.0.2
```
📸 Screenshot 5 (CORE OUTPUT)

# 📂 STEP 10: View Log File
## 🔵 Terminal 3 (OPTIONAL)
```bash
cat ~/SDN-Packet-Logger/pox/logs/packet_log.txt
```
📸 Screenshot 6: Stored logs

# 📊 STEP 11: View Flow Table

## 🟡 Terminal 2
```bash
dpctl dump-flows
```
📸 Screenshot 7:

* Look for actions=FLOOD
* Packet counters

# 🎯 COMPLETE DEMO FLOW
* Start POX Controller (Terminal 1)
* Start Mininet (Terminal 2)
* Run pingall
* Run h1 ping h2
* Show logs (Terminal 1)
* Show flow table (Terminal 2)
* Show log file (Terminal 3)

# 🧠 DEMO EXPLANATION 

The POX controller captures PacketIn events, extracts MAC and IP headers, identifies protocol types such as ICMP, logs the data in real-time, and forwards packets using OpenFlow flooding.
