import argparse
import geoip2.database


def print_record(target_ip):
    with geoip2.database.Reader('geolite2_city.mmdb') as gi:
        rec = gi.city(target_ip)

        city = rec.city.name
        region = rec.subdivisions.most_specific.name
        country = rec.country.name
        lat = rec.location.latitude
        long = rec.location.longitude

        print(f'[*] Target: {target_ip} Geo-located.')
        print(f'   [+] {city}, {region}, {country}')
        print(f'   [+] Latitude: {lat}, Longitude: {long}')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        usage='python3 geo_ip.py TARGET_IP')
    parser.add_argument('tgt_ip', type=str, metavar='TARGET_IP',
                        help='IP address of the target to geolocate')

    print_record(parser.parse_args().tgt_ip)
