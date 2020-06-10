from bluetooth import *


def rfcomm_con(addr, port):
    with BluetoothSocket(RFCOMM) as sock:
        try:
            sock.connect((addr, port))
            print(f'[+] RFCOMM Port {str(port)} open')
        except Exception as e:
            print(f'{"":>3}[-] Exception: {e.__class__.__name__}')
            print(f'{"":>3}[-] RFCOMM Port {str(port)} closed')


if __name__ == '__main__':
    for _port in range(1, 30):
        rfcomm_con('00:16:38:DE:AD:11', _port)
