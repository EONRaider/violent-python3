import sqlite3
import argparse
import os


def print_profile(skype_db):
    with sqlite3.connect(skype_db) as conn:
        c = conn.cursor()
        c.execute("SELECT fullname, skypename, city, country, \
          datetime(profile_timestamp,'unixepoch') FROM Accounts;")

        for row in c:
            print('[*] -- Found Account --')
            print(f'   [+] User           : {str(row[0])}')
            print(f'   [+] Skype Username : {str(row[1])}')
            print(f'   [+] Location       : {str(row[2])}, {str(row[3])}')
            print(f'   [+] Profile Date   : {str(row[4])}')


def print_contacts(skype_db):
    with sqlite3.connect(skype_db) as conn:
        c = conn.cursor()
        c.execute("SELECT displayname, skypename, city, country,\
          phone_mobile, birthday FROM Contacts;")

        for row in c:
            print('\n[*] -- Found Contact --')
            print(f'   [+] User           : {str(row[0])}')
            print(f'   [+] Skype Username : {str(row[1])}')

            if str(row[2]) != '' and str(row[2]) != 'None':
                print(f'   [+] Location       : {str(row[2])}, {str(row[3])}')
            if str(row[4]) != 'None':
                print(f'   [+] Mobile Number  : {str(row[4])}')
            if str(row[5]) != 'None':
                print(f'   [+] Birthday       : {str(row[5])}')


def print_call_log(skype_db):
    with sqlite3.connect(skype_db) as conn:
        c = conn.cursor()
        c.execute("SELECT datetime(begin_timestamp,'unixepoch'), \
          identity FROM calls, conversations WHERE \
          calls.conv_dbid = conversations.id;")

        print('\n[*] -- Found Calls --')

        for row in c:
            print(f'   [+] Time: {str(row[0])} | Partner: {str(row[1])}')


def print_messages(skype_db):
    with sqlite3.connect(skype_db) as conn:
        c = conn.cursor()
        c.execute("SELECT datetime(timestamp,'unixepoch'), \
                  dialog_partner, author, body_xml FROM Messages;")
        print('\n[*] -- Found Messages --')

        for row in c:
            try:
                if 'partlist' not in str(row[3]):
                    if str(row[1]) != str(row[2]):
                        msg_direction = f'To {str(row[1])}: '
                    else:
                        msg_direction = f'From {str(row[2])}: '
                    print(f'Time: {str(row[0])} {msg_direction} {str(row[3])}')
            except Exception as e:
                print(f'[-] Exception: {e.__class__.__name__}')
                pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        usage='python3 skype_parse.py SKYPE_PROFILE')
    parser.add_argument('skype_prof', type=str, metavar='SKYPE_PROFILE',
                        help='specify path to the directory containing '
                             'the skype profile database file')

    args = parser.parse_args()
    skype_dbase = os.path.join(args.skype_prof, 'main.db')

    if os.path.isfile(skype_dbase):
        print_profile(skype_dbase)
        print_contacts(skype_dbase)
        print_call_log(skype_dbase)
        print_messages(skype_dbase)
    else:
        print(f'[!] Skype Database does not exist: {skype_dbase}')
