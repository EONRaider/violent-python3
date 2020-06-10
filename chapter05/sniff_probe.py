from scapy.all import sniff
from scapy.layers.dot11 import Dot11ProbeReq


def sniff_probe(pkt):
    probe_reqs = []
    if pkt.haslayer(Dot11ProbeReq):
        net_name = pkt.getlayer(Dot11ProbeReq).info
        if net_name not in probe_reqs:
            probe_reqs.append(net_name)
            print(f'[+] Detected New Probe Request: {net_name}')


if __name__ == '__main__':
    sniff(iface='mon0', prn=sniff_probe)
