import argparse
import urllib.error
import urllib.parse
import urllib.request
from urllib.parse import urlsplit
from os.path import basename
from bs4 import BeautifulSoup
from PIL import Image
from PIL.ExifTags import TAGS


def find_images(url):
    print(f'[+] Finding images on {url}')
    url_content = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(url_content, features="html.parser")
    img_tags = soup.findAll('img')
    return img_tags


def download_image(tag):
    try:
        print('[+] Downloading image...')
        img_src = tag['src']
        img_content = urllib.request.urlopen(img_src).read()
        img_filename = basename(urlsplit(img_src)[2])
        with open(img_filename, 'wb') as file:
            file.write(img_content)
        return img_filename
    except OSError:
        return ''


def test_for_exif(img_filename):
    try:
        exif_data = {}
        img_file = Image.open(img_filename)
        info = img_file._getexif()
        if info:
            for tag, value in list(info.items()):
                decoded = TAGS.get(tag, tag)
                exif_data[decoded] = value
            exif_gps = exif_data['GPSInfo']
            if exif_gps:
                print(f'[*] {img_filename} contains GPS MetaData')
    except Exception as e:
        print(f'{"":>3}[-] No {e} found')
        pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        usage='python3 exif_fetch.py TARGET_URL')
    parser.add_argument('tgt_url', type=str, metavar='TARGET_URL',
                        help='specify URL of the target')

    args = parser.parse_args()
    tags = find_images(args.tgt_url)
    for img_tag in tags:
        test_for_exif(download_image(img_tag))
