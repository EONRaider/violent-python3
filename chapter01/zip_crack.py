import zipfile
import argparse
from threading import Thread


def extract_file(zfile, password):
    try:
        zfile.extractall(pwd=password.encode('utf-8'))
        print(f'[+] Found password: {password}\n')
    except RuntimeError:
        pass


def main(zname, dname):
    z_file = zipfile.ZipFile(zname)
    with open(dname) as pass_file:
        for line in pass_file.readlines():
            password = line.strip('\n')
            t = Thread(target=extract_file, args=(z_file, password))
            t.start()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(usage='zip_crack.py ZIPFILE DICTFILE')
    parser.add_argument('zipfile', type=str, metavar='ZIPFILE',
                        help='specify zip file')
    parser.add_argument('dictfile', type=str, metavar='DICTFILE',
                        help='specify dictionary file')
    args = parser.parse_args()
    main(args.zipfile, args.dictfile)
