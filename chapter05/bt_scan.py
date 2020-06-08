import time
from bluetooth import *


def find_devs():
    already_found = []
    found_devs = discover_devices(lookup_names=True)
    for addr, name in found_devs:
        if addr not in already_found:
            print(f'[*] Found Bluetooth Device: {str(name)}')
            print(f'[+] MAC Address: {str(addr)}')
            already_found.append(addr)


if __name__ == '__main__':
    while True:
        try:
            find_devs()
            time.sleep(5)
        except KeyboardInterrupt:
            exit(0)
