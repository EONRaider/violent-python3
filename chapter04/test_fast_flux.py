from scapy.all import rdpcap
from scapy.layers.dns import DNSRR

dns_records = {}


def handle_pkt(pkt):
    if pkt.haslayer(DNSRR):
        rrname = pkt.getlayer(DNSRR).rrname
        rdata = pkt.getlayer(DNSRR).rdata
        if rrname in dns_records:
            if rdata not in dns_records[rrname]:
                dns_records[rrname].append(rdata)
        else:
            dns_records[rrname] = []
            dns_records[rrname].append(rdata)


if __name__ == '__main__':
    pkts = rdpcap('fast_flux.pcap')
    for _pkt in pkts:
        handle_pkt(_pkt)
    
    for item in dns_records:
        print(f"[+] {item.decode('utf-8')} has {str(len(dns_records[item]))} "
              f"unique IPs.")
