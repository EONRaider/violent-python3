import nmap
import argparse


def nmap_scan(tgt_host, tgt_ports):
    nm_scan = nmap.PortScanner()
    for tgt_port in tgt_ports:
        nm_scan.scan(tgt_host, tgt_port)
        state = nm_scan[tgt_host]['tcp'][int(tgt_port)]['state']
        print(f'[*] {tgt_host} tcp/{tgt_port} {state}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        usage='nmap_scan.py TARGET_HOST -p TARGET_PORTS')
    parser.add_argument('host', type=str, metavar='TARGET_HOST',
                        help="specify target host's IP number")
    parser.add_argument('-p', type=str, metavar='TARGET_PORTS',
                        help='specify target port[s] separated by comma '
                             '(no spaces)')
    args = parser.parse_args()

    args.ports = str(args.p).split(',')
    nmap_scan(args.host, args.ports)
