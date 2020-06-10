from scapy.all import sniff, conf
from scapy.layers.dot11 import Dot11
from bluetooth import *


def ret_bt_addr(addr):
    bt_addr = str(hex(int(addr.replace(':', ''), 16) + 1))[2:]
    return f'{bt_addr[:2]}:{bt_addr[2:4]}:{bt_addr[4:6]}:{bt_addr[6:8]}' \
           f':{bt_addr[8:10]}:{bt_addr[10:12]}'


def check_bluetooth(bt_addr):
    bt_name = lookup_name(bt_addr)
    if bt_name:
        print(f'[+] Detected Bluetooth Device: {bt_name}')
    else:
        print(f'{"":>3}[-] Failed to Detect Bluetooth Device')


def wifi_print(pkt):
    iphone_oui = 'd0:23:db'
    if pkt.haslayer(Dot11):
        wifi_mac = pkt.getlayer(Dot11).addr2
        if iphone_oui == wifi_mac[:8]:
            print(f'[*] Detected iPhone MAC: {wifi_mac}')
            bt_addr = ret_bt_addr(wifi_mac)
            print(f'[+] Testing Bluetooth MAC: {bt_addr}')
            check_bluetooth(bt_addr)


if __name__ == '__main__':
    conf.iface = 'mon0'
    sniff(prn=wifi_print)
