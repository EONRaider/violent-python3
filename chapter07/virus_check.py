import re
import http.client
import time
import os
import argparse
from urllib.parse import urlparse


def print_results(url):
    status = 200
    host = urlparse(url)[1]
    path = urlparse(url)[2]

    if 'analysis' not in path:
        while status != 302:
            with http.client.HTTPConnection(host) as conn:
                conn.request('GET', path)
                resp = conn.getresponse()
                status = resp.status
                print('[+] Scanning file...')
            time.sleep(15)

    print('[+] Scan Complete.')
    path = path.replace('file', 'analysis')

    with http.client.HTTPConnection(host) as conn:
        conn.request('GET', path)
        resp = conn.getresponse()
        data = resp.read()

    re_results = re.findall(r'Detection rate:.*\)', data)
    html_strip_res = re_results[1].replace('&lt;font color=\'red\'&gt;', ''). \
        replace('&lt;/font&gt;', '')
    print(f'[+] {str(html_strip_res)}')


def upload_file(filename):
    print("[+] Uploading file to NoVirusThanks...")
    file_contents = open(filename, 'rb').read()

    header = {'Content-Type': 'multipart/form-data; '
                              'boundary=----WebKitFormBoundaryF17rwCZdGuPNPT9U'
              }

    params = "------WebKitFormBoundaryF17rwCZdGuPNPT9U"
    params += f"\r\nContent-Disposition: form-data; name=\"upfile\"; " \
              f"filename=\"{str(filename)}\""
    params += "\r\nContent-Type: application/octet stream\r\n\r\n"
    params += file_contents
    params += "\r\n------WebKitFormBoundaryF17rwCZdGuPNPT9U"
    params += "\r\nContent-Disposition: form-data; name=\"submitfile\"\r\n"
    params += "\r\nSubmit File\r\n"
    params += "------WebKitFormBoundaryF17rwCZdGuPNPT9U--\r\n"

    with http.client.HTTPConnection('vscan.novirusthanks.org') as conn:
        conn.request("POST", "/", params, header)
        response = conn.getresponse()
        location = response.getheader('location')

    return location


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        usage='python3 virus_check.py FILENAME')
    parser.add_argument('filename', type=str, metavar='FILENAME',
                        help='specify the name of the file')

    args = parser.parse_args()
    _filename = args.filename

    if not os.path.isfile(_filename):
        print(f'[+] {_filename} does not exist.')
        exit(0)
    else:
        loc = upload_file(_filename)
        print_results(loc)
