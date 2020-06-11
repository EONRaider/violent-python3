from anon_browser import AnonBrowser
from bs4 import BeautifulSoup
import argparse
import os


def mirror_images(tgt_url, dest_dir):
    ab = AnonBrowser()
    ab.anonymize()
    ab.open(tgt_url)
    html = str(ab.get_current_page())
    soup = BeautifulSoup(html, 'html.parser')
    image_tags = soup.find_all('img')

    for image in image_tags:
        filename = image['src'].lstrip('http://')
        filename = os.path.join(dest_dir, filename.replace('/', '_'))
        data = ab.open(image['src']).read()
        with open(filename, 'wb') as save:
            print(f'[+] Saving {str(filename)}')
            save.write(data)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        usage='python3 image_mirror.py TARGET_URL DESTINATION_DIR')
    parser.add_argument('tgt_url', type=str, metavar='TARGET_URL',
                        help='specify the target url')
    parser.add_argument('-d', type=str, metavar='DESTINATION_DIR',
                        required=True, help='specify the destination directory')
    args = parser.parse_args()

    _tgt_url = args.tgt_url
    _dest_dir = args.d

    try:
        mirror_images(_tgt_url, _dest_dir)
    except Exception as e:
        print(f'[!] Error Mirroring Images.\n'
              f'{"":>3}[-] {str(e)}')
