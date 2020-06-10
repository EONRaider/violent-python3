import re
import argparse
from scapy.layers.inet import IP
from scapy.all import sniff, conf


def fire_catcher(pkt):
    cookie_table = {}
    raw = pkt.sprintf('%Raw.load%')
    r = re.findall(r'wordpress_[0-9a-fA-F]{32}', raw)
    if r and 'Set' not in raw:
        if r[0] not in list(cookie_table.keys()):
            cookie_table[r[0]] = pkt.getlayer(IP).src
            print('[+] Detected and indexed cookie.')
        elif cookie_table[r[0]] != pkt.getlayer(IP).src:
            print(f'[*] Detected Conflict for {r[0]}')
            print(f'Victim   = {cookie_table[r[0]]}')
            print(f'Attacker = {pkt.getlayer(IP).src}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        usage='python3 fire_catcher.py INTERFACE')
    parser.add_argument('iface', type=str, metavar='INTERFACE',
                        help='specify the interface to listen on')
    args = parser.parse_args()
    conf.iface = args.iface

    try:
        sniff(filter='tcp port 80', prn=fire_catcher)
    except KeyboardInterrupt:
        exit(0)
