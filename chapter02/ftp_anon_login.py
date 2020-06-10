import ftplib


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


if __name__ == "__main__":
    host = '192.168.95.179'
    anon_login(host)
