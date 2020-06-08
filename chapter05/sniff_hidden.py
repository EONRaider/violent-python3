from scapy.layers.dot11 import Dot11, Dot11ProbeResp, Dot11Beacon
from scapy.all import sniff


def sniff_dot11(packet):
    hidden_nets = []
    unhidden_nets = []

    if packet.haslayer(Dot11ProbeResp):
        addr2 = packet.getlayer(Dot11).addr2
        if (addr2 in hidden_nets) & (addr2 not in unhidden_nets):
            net_name = packet.getlayer(Dot11ProbeResp).info
            print(f'[+] De-cloaked Hidden SSID: {net_name} for MAC: {addr2}')
            unhidden_nets.append(addr2)
    
    if packet.haslayer(Dot11Beacon):
        if packet.getlayer(Dot11Beacon).info == '':
            addr2 = packet.getlayer(Dot11).addr2
            if addr2 not in hidden_nets:
                print(f'[-] Detected Hidden SSID with MAC: {addr2}')
                hidden_nets.append(addr2)


if __name__ == '__main__':
    sniff(iface='mon0', prn=sniff_dot11)
