import dpkt
import socket


def print_pcap(pcap_file):
    for ts, buf in pcap_file:
        try:
            eth = dpkt.ethernet.Ethernet(buf)
            ip = eth.data
            src = socket.inet_ntoa(ip.src)
            dst = socket.inet_ntoa(ip.dst)
            print(f'[+] Src: {src} --> Dst: {dst}')
        except Exception as e:
            print(f'{"":>3}[-] Exception: {e.__class__.__name__}')
            pass


if __name__ == '__main__':
    with open('geotest.pcap', 'rb') as file:
        pcap = dpkt.pcap.Reader(file)
        print_pcap(pcap)
