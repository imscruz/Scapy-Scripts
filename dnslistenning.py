

#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
#  LISTEN YOUR DNS PACKETS                  |
#  THIS SCRIPT MADE BY imscruz              |
#  STAR MY REPO Pls imscruz/Scapy-Scripts   |
#///////////////////////////////////////////

from scapy.all import sniff, DNS #MODULEES

def dns_callback(packet): # FONKSIOYNEL
    if packet.haslayer(DNS):
        print(f"DNS: {packet[DNS].qd.qname.decode()}")

sniff(filter="udp port 53", prn=dns_callback, store=0) #PORT 53 IS DNS PORT IF DONT WORK JUST LEARN YOUR DNS PORT MAYBE 5353
