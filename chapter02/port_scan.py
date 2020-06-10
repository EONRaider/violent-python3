import argparse
import socket
import threading


def port_scan(tgt_host, tgt_ports):
    try:
        tgt_ip = socket.gethostbyname(tgt_host)
    except socket.herror:
        print(f'[-] Cannot resolve {tgt_host}: Unknown host')
        return

    try:
        tgt_name = socket.gethostbyaddr(tgt_ip)
        print(f'\n[+] Scan Results for: {tgt_name[0]}')
    except socket.herror:
        print(f'\n[+] Scan Results for: {tgt_ip}')

    socket.setdefaulttimeout(1)

    for ports in tgt_ports:
        t = threading.Thread(target=conn_scan, args=(tgt_host, int(ports)))
        t.start()


def conn_scan(tgt_host, tgt_port):
    screen_lock = threading.Semaphore()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as conn_skt:
        try:
            conn_skt.connect((tgt_host, tgt_port))
            conn_skt.send(b'ViolentPython\r\n')
            results = conn_skt.recv(100).decode('utf-8')
            screen_lock.acquire()
            print(f'[+] {tgt_port}/tcp open')
            print(f'   [>] {results}')
        except OSError:
            screen_lock.acquire()
            print(f'[-] {tgt_port}/tcp closed')
        finally:
            screen_lock.release()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        usage='port_scan.py TARGET_HOST -p TARGET_PORTS'
              '\nexample: python3 port_scan.py scanme.nmap.org -p 21,80')

    parser.add_argument('tgt_host', type=str, metavar='TARGET_HOST',
                        help='specify target host (IP address or domain name)')
    parser.add_argument('-p', required=True, type=str, metavar='TARGET_PORTS',
                        help='specify target port[s] separated by comma '
                             '(no spaces)')
    args = parser.parse_args()

    args.tgt_ports = str(args.p).split(',')
    port_scan(args.tgt_host, args.tgt_ports)
