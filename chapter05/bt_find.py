import time
from bluetooth import *
from datetime import datetime


def find_tgt(tgt_name):
    found_devs = discover_devices(lookup_names=True)
    for addr, name in found_devs:
        if tgt_name == name:
            print(f'[*] Found Target Device: {tgt_name}')
            print(f'[+] With MAC Address: {addr}')
            print(f'[+] Time is: {str(datetime.now())}')


if __name__ == '__main__':
    _tgt_name = 'TJ iPhone'
    while True:
        try:
            print(f'[-] Scanning for Bluetooth Device: {_tgt_name}')
            find_tgt(_tgt_name)
            time.sleep(5)
        except KeyboardInterrupt:
            exit(0)
