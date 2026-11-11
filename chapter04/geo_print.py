import argparse
import os
import socket
import sys
import dpkt
import geoip2.database

DEFAULT_DB = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                          'geolite2_city.mmdb')
DB_HELP = (
    "MaxMind's licence does not allow redistributing the GeoLite2 database, so it "
    "is no longer bundled with this repository. Create a free licence key at "
    "https://www.maxmind.com/en/geolite2/signup and download GeoLite2-City.mmdb "
    "with geoipupdate (https://github.com/maxmind/geoipupdate), then pass its path "
    "with --db or place it next to this script as 'geolite2_city.mmdb'."
)


def ret_geo_str(ip, db_path=DEFAULT_DB):
    """ This function is not part of the original code of Violent
    Python. It used the deprecated 'pygeoip' library to perform
    the same task. A new solution using the API to the database
    provided by the MaxMind service has been implemented here by
    EONRaider. https://github.com/EONRaider"""

    try:
        with geoip2.database.Reader(db_path) as gi:
            rec = gi.city(ip)
            city = rec.city.name
            country = rec.country.name
            return f'{city}, {country}' if city else country

    except Exception as e:
        print(f'{"":>3}[-] Exception: {e.__class__.__name__}')
        return 'Unregistered'


def print_pcap(pcap_file, db_path=DEFAULT_DB):
    for ts, buf in pcap_file:
        try:
            eth = dpkt.ethernet.Ethernet(buf)
            ip = eth.data
            src = socket.inet_ntoa(ip.src)
            dst = socket.inet_ntoa(ip.dst)
            print(f'[+] Src: {ret_geo_str(src, db_path)} '
                  f'--> Dst: {ret_geo_str(dst, db_path)}')
        except Exception as e:
            print(f'{"":>3}[-] Exception: {e.__class__.__name__}')
            pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser(usage='python3 geo_print PCAP_FILE')
    parser.add_argument('pcap', type=str, metavar='PCAP_FILE',
                        help='specify the name of the PCAP file')
    parser.add_argument('--db', type=str, default=DEFAULT_DB, metavar='MMDB',
                        help=f'path to a GeoLite2 City database. {DB_HELP}')
    args = parser.parse_args()

    if not os.path.isfile(args.db):
        sys.exit(f"[-] GeoLite2 City database not found at '{args.db}'.\n    {DB_HELP}")

    with open(args.pcap, 'rb') as file:
        pcap = dpkt.pcap.Reader(file)
        print_pcap(pcap, args.db)
