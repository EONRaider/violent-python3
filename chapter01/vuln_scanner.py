import socket
import os
import sys


def ret_banner(ip, port):
    try:
        socket.setdefaulttimeout(2)
        s = socket.socket()
        s.connect((ip, port))
        banner = s.recv(1024)
        return banner
    except OSError:
        return


def check_vulns(banner, filename):
    with open(filename) as file:
        for line in file.readlines():
            if line.strip('\n') in banner.strip('\n'):
                print(f'[+] Server is vulnerable: {banner}')


if __name__ == '__main__':
    if len(sys.argv) == 2:
        _filename = sys.argv[1]
        if not os.path.isfile(_filename):
            print(f'[-] {_filename} does not exist.')
            exit(0)

        if not os.access(_filename, os.R_OK):
            print(f'[-] {_filename} access denied.')
            exit(0)

        port_list = [21, 22, 25, 80, 110, 443]

        for x in range(147, 150):
            _ip = '192.168.95.' + str(x)
            for _port in port_list:
                _banner = ret_banner(_ip, _port)
                if _banner:
                    print(f'[+] {_ip}: {_banner}')
                    check_vulns(_banner, _filename)

    else:
        print(f'[-] Usage: {str(sys.argv[0])} <vuln filename>')
        exit(0)
