from bluetooth import *


def sdp_browse(addr):
    services = find_service(address=addr)
    for service in services:
        name = service['name']
        proto = service['protocol']
        port = str(service['port'])
        print(f'[+] Found {str(name)} on {str(proto)}: {port}')


if __name__ == '__main__':
    sdp_browse('00:16:38:DE:AD:11')
