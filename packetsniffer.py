#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
#  SNIFF TCP PACKETS IN LOCAL LIKE WIRESHARK|
#  THIS SCRIPT MADE BY imscruz              |
#  STAR MY REPO Pls imscruz/Scapy-Scripts   |
#///////////////////////////////////////////

import os
import time
from scapy.all import ARP, Ether, srp, send
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
from scapy.all import sniff

def packet_sniffer(pkt):
    print(pkt.summary())
print("\n[+] Started SNIFF LIKE A DOG! U can stop with CTRL+C...\n")
sniff(filter="tcp", prn=packet_sniffer, count=500)

# Change "tcp" value if you want udp idk

#change count=500 if you want more sniffing like 999999999999
