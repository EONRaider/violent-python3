from scapy.all import rdpcap
from scapy.layers.inet import UDP
from scapy.layers.dns import DNS, DNSQR


def dns_QR_test(pkt):
    if pkt.getlayer(UDP).sport == 53:
        rcode = pkt.getlayer(DNS).rcode
        qname = pkt.getlayer(DNSQR).qname
        if rcode == 3:
            print(f'[!] Name request lookup failed: {qname}')
            return True
    return False


if __name__ == '__main__':
    unans_reqs = 0
    pkts = rdpcap('domain_flux.pcap')
    for _pkt in pkts:
        if dns_QR_test(_pkt):
            unans_reqs += 1
    print(f'[!] {str(unans_reqs)} Total Unanswered Name Requests')
