import argparse
import os
import socket
import sys
import dpkt
import geoip2.database

DEFAULT_DB = 'geolite2_city.mmdb'
DB_HELP = (
    "MaxMind's licence does not allow redistributing the GeoLite2 database, so it "
    "is no longer bundled with this repository. Create a free licence key at "
    "https://www.maxmind.com/en/geolite2/signup and download GeoLite2-City.mmdb "
    "with geoipupdate (https://github.com/maxmind/geoipupdate), then pass its path "
    "with --db or place it next to this script as 'geolite2_city.mmdb'."
)


def ret_KML(ip, db_path=DEFAULT_DB):
    """ This function is not part of the original code of Violent
    Python. It used the deprecated 'pygeoip' library to perform
    the same task. A new solution using the API to the database
    provided by the MaxMind service has been implemented here by
    EONRaider. https://github.com/EONRaider"""

    with geoip2.database.Reader(db_path) as gi:
        rec = gi.city(ip)

        try:
            latitude = rec.location.latitude
            longitude = rec.location.longitude
            kml = (
                      f'<Placemark>\n'
                      f'<name>{ip}</name>\n'
                      f'<Point>\n'
                      f'<coordinates>{latitude:f},{longitude:f}</coordinates>\n'
                      f'</Point>\n'
                      f'</Placemark>\n'
                  )
            return kml

        except Exception as e:
            print(f'{"":>3}[-] Exception: {e.__class__.__name__}')
            return ''


def plot_IPs(pcap, db_path=DEFAULT_DB):
    kml_pts = ''

    for ts, buf in pcap:
        try:
            eth = dpkt.ethernet.Ethernet(buf)
            ip = eth.data
            src = socket.inet_ntoa(ip.src)
            dst = socket.inet_ntoa(ip.dst)

            src_kml = ret_KML(src, db_path)
            dst_kml = ret_KML(dst, db_path)

            kml_pts = kml_pts + src_kml + dst_kml

        except Exception as e:
            print(f'[-] Exception: {e.__class__.__name__}')
            pass

    return kml_pts


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        usage='python3 google_earth_pcap.py PCAP_FILE')
    parser.add_argument('pcap_file', type=str, metavar='PCAP_FILE',
                        help='specify the name of the pcap file')
    parser.add_argument('--db', type=str, default=DEFAULT_DB, metavar='MMDB',
                        help=f'path to a GeoLite2 City database. {DB_HELP}')

    args = parser.parse_args()
    pcap_file = args.pcap_file

    if not os.path.isfile(args.db):
        sys.exit(f"[-] GeoLite2 City database not found at '{args.db}'.\n    {DB_HELP}")

    with open(pcap_file, 'rb') as file:
        _pcap = dpkt.pcap.Reader(file)

        kmlheader = '<?xml version="1.0" encoding="UTF-8"?>' \
                    '\n<kml xmlns="http://www.opengis.net/kml/2.2">' \
                    '\n<Document>\n'
        kmlfooter = '</Document>\n</kml>\n'
        kmldoc = kmlheader + plot_IPs(_pcap, args.db) + kmlfooter

        print(kmldoc)
