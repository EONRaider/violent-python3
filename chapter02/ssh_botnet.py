from pexpect import pxssh


class Client:
    def __init__(self, host, user, password):
        self.host = host
        self.user = user
        self.password = password
        self.session = self.connect()

    def connect(self):
        try:
            session = pxssh.pxssh()
            session.login(self.host, self.user, self.password)
            return session
        except Exception as e:
            print(f'[-] Error Connecting: {e}')

    def send_command(self, cmd):
        self.session.sendline(cmd)
        self.session.prompt()
        return self.session.before


def botnet_command(command):
    for client in botnet:
        output = client.send_command(command).decode('utf-8')
        print(f'[*] Output from {client.host}')
        print(f'[+] {output}')


def add_client(host, user, password):
    client = Client(host, user, password)
    botnet.append(client)


if __name__ == '__main__':
    botnet = []
    add_client('127.0.0.1', 'root', 'toor')
    add_client('127.0.0.1', 'root', 'toor')
    add_client('127.0.0.1', 'root', 'toor')

    botnet_command('uname -v && cat /etc/issue')
