import argparse
import os
import sys
import geoip2.database

DEFAULT_DB = 'geolite2_city.mmdb'
DB_HELP = (
    "MaxMind's licence does not allow redistributing the GeoLite2 database, so it "
    "is no longer bundled with this repository. Create a free licence key at "
    "https://www.maxmind.com/en/geolite2/signup and download GeoLite2-City.mmdb "
    "with geoipupdate (https://github.com/maxmind/geoipupdate), then pass its path "
    "with --db or place it next to this script as 'geolite2_city.mmdb'."
)


def print_record(target_ip, db_path=DEFAULT_DB):
    """ This function is not part of the original code of Violent
    Python. It used the deprecated 'pygeoip' library to perform
    the same task. A new solution using the API to the database
    provided by the MaxMind service has been implemented here by
    EONRaider. https://github.com/EONRaider"""

    with geoip2.database.Reader(db_path) as gi:
        rec = gi.city(target_ip)

        city = rec.city.name
        region = rec.subdivisions.most_specific.name
        country = rec.country.name
        lat = rec.location.latitude
        long = rec.location.longitude

        print(f'[*] Target: {target_ip} Geo-located.')
        print(f'{"":>3}[+] {city}, {region}, {country}')
        print(f'{"":>3}[+] Latitude: {lat}, Longitude: {long}')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        usage='python3 geo_ip.py TARGET_IP')
    parser.add_argument('tgt_ip', type=str, metavar='TARGET_IP',
                        help='IP address of the target to geolocate')
    parser.add_argument('--db', type=str, default=DEFAULT_DB, metavar='MMDB',
                        help=f'path to a GeoLite2 City database. {DB_HELP}')
    args = parser.parse_args()

    if not os.path.isfile(args.db):
        sys.exit(f"[-] GeoLite2 City database not found at '{args.db}'.\n    {DB_HELP}")

    print_record(args.tgt_ip, args.db)
